import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np
import cvxpy as cp

class CBFQPController(Node):
    def __init__(self):
        super().__init__('cbf_qp_controller')
        
        # Publisher for flight commands and Subscriber for current position
        self.cmd_pub = self.create_publisher(Twist, '/model/simple_drone/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/model/simple_drone/odometry', self.odom_callback, 10)
        
        # Control Loop running at 20 Hz (0.05 seconds)
        self.timer = self.create_timer(0.05, self.control_loop)
        
        # System Parameters
        # Target is the visual beacon at x=15 in obstacle_world.sdf
        self.target = np.array([15.0, 0.0, 2.0])

        # Obstacle coordinates (must match obstacle_world.sdf)
        self.obstacles = [
            # Center slalom (red)
            np.array([3.0, 0.5]),
            np.array([6.0, -0.5]),
            np.array([9.0, 0.5]),
            np.array([12.0, -0.5]),
            # Left guardrail (blue)
            np.array([3.0, 4.0]),
            np.array([6.0, 4.0]),
            np.array([9.0, 4.0]),
            np.array([12.0, 4.0]),
            # Right guardrail (blue)
            np.array([3.0, -4.0]),
            np.array([6.0, -4.0]),
            np.array([9.0, -4.0]),
            np.array([12.0, -4.0]),
        ]
        
        # CBF and CLF Parameters
        self.D_s = 1.5       # Safe distance boundary (meters)
        self.alpha = 1.5     # CBF aggression (how hard it pushes back)
        self.Kp = 1.2        # CLF proportional gain (speed to target)
        self.max_vel = 1.5   # Maximum allowed speed
        
        self.current_pos = None
        self.get_logger().info('CBF-QP Controller Initialized. Waiting for Odometry...')

    def odom_callback(self, msg):
        self.current_pos = np.array([
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            msg.pose.pose.position.z
        ])

    def control_loop(self):
        if self.current_pos is None:
            return

        # 1. CLF: Calculate Nominal Control (Vector straight to target)
        dist_to_target = np.linalg.norm(self.target - self.current_pos)
        
        if dist_to_target < 0.1:
            self.get_logger().info('Target Reached! Hovering.', throttle_duration_sec=2.0)
            self.cmd_pub.publish(Twist()) # Send zero velocity
            return

        u_nom = self.Kp * (self.target - self.current_pos)
        
        # --- PERMANENT DEADLOCK RESOLUTION (Tangential Escape) ---
        for obs in self.obstacles:
            # 3D Vector from drone to obstacle (ignoring Z height)
            vec_to_obs = np.array([obs[0] - self.current_pos[0], obs[1] - self.current_pos[1], 0.0])
            dist_to_obs = np.linalg.norm(vec_to_obs)
            
            # If obstacle is within an influence radius (Safety D_s + 1.5m buffer)
            if dist_to_obs < self.D_s + 1.5:
                dir_to_obs = vec_to_obs / dist_to_obs
                dir_u_nom = u_nom / (np.linalg.norm(u_nom) + 1e-6)
                
                # Check if u_nom is pointing directly AT the obstacle (dot product > 0.9)
                if np.dot(dir_to_obs, dir_u_nom) > 0.9:
                    self.get_logger().info('Deadlock risk detected! Injecting tangential escape vector.', throttle_duration_sec=1.0)
                    # Create a 2D tangent vector (rotate 90 degrees: [-y, x, 0])
                    tangent = np.array([-dir_to_obs[1], dir_to_obs[0], 0.0])
                    
                    # Force a side-step by aggressively blending the tangent into u_nom
                    u_nom += tangent * self.max_vel
        # ---------------------------------------------------------

        # Cap nominal velocity
        if np.linalg.norm(u_nom) > self.max_vel:
            u_nom = (u_nom / np.linalg.norm(u_nom)) * self.max_vel

        # 2. Setup the Quadratic Program (QP)
        u = cp.Variable(3)
        objective = cp.Minimize(cp.sum_squares(u - u_nom))
        constraints = []
        
        # 3. CBF: Apply Safety Constraints for each obstacle
        for obs in self.obstacles:
            dx = self.current_pos[0] - obs[0]
            dy = self.current_pos[1] - obs[1]
            
            h = (dx**2 + dy**2) - self.D_s**2
            grad_h = np.array([2*dx, 2*dy, 0.0])
            
            constraints.append(grad_h @ u >= -self.alpha * h)
            
        prob = cp.Problem(objective, constraints)
        
        # 4. Solve the QP
        try:
            prob.solve(solver=cp.OSQP)
            if u.value is not None:
                u_safe = u.value
            else:
                self.get_logger().warn('QP Infeasible! Hovering to prevent crash.')
                u_safe = np.zeros(3)
        except Exception as e:
            self.get_logger().error(f'Solver Error: {e}')
            u_safe = np.zeros(3)
            
        # 5. Publish Safe Control Commands
        twist = Twist()
        twist.linear.x = u_safe[0]
        twist.linear.y = u_safe[1]
        twist.linear.z = u_safe[2]
        self.cmd_pub.publish(twist)
        
        nearest_obs_dist = min(
            [np.sqrt((self.current_pos[0] - obs[0])**2 + (self.current_pos[1] - obs[1])**2) for obs in self.obstacles]
        )
        self.get_logger().info(
            f'Navigating... Target Dist: {dist_to_target:.2f}m | Nearest Obs Dist: {nearest_obs_dist:.2f}m',
            throttle_duration_sec=0.5
        )


def main(args=None):
    rclpy.init(args=args)
    node = CBFQPController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()