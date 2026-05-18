import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')
        
        # Subscriptions and Publishers
        self.odom_sub = self.create_subscription(Odometry, '/model/simple_drone/odometry', self.odom_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/model/simple_drone/cmd_vel', 10)
        
        # Define our target destination [X, Y, Z]
        self.target_x = 3.0
        self.target_y = 3.0
        self.target_z = 2.0
        
        # Control gains (proportional scaling factors)
        self.kp = 0.5
        
        # Internal state variables
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_z = 0.0
        
        # 10Hz control loop timer
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info(f'Target Position set to: [{self.target_x}, {self.target_y}, {self.target_z}]')

    def odom_callback(self, msg):
        # Extract current coordinates from the Gazebo telemetry feedback
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        self.current_z = msg.pose.pose.position.z

    def control_loop(self):
        # Compute positional distance errors
        error_x = self.target_x - self.current_x
        error_y = self.target_y - self.current_y
        error_z = self.target_z - self.current_z
        
        distance_to_target = math.sqrt(error_x**2 + error_y**2 + error_z**2)
        
        cmd = Twist()
        
        # Goal Threshold check (Within 15 centimeters)
        if distance_to_target < 0.15:
            self.get_logger().info('Target Waypoint Reached! Holding position...', throttle_duration_sec=3.0)
            # Send zero velocity commands to hover in place
            cmd.linear.x = 0.0
            cmd.linear.y = 0.0
            cmd.linear.z = 0.0
        else:
            # P-Controller: Velocity = Error * Gain
            cmd.linear.x = error_x * self.kp
            cmd.linear.y = error_y * self.kp
            cmd.linear.z = error_z * self.kp
            
            # Clamp maximum speeds so the proxy model doesn't fly out of control
            cmd.linear.x = max(min(cmd.linear.x, 1.0), -1.0)
            cmd.linear.y = max(min(cmd.linear.y, 1.0), -1.0)
            cmd.linear.z = max(min(cmd.linear.z, 0.8), -0.8)
            
            # FIXED: Changed :.2m to :.2f}m
            self.get_logger().info(
                f'Moving to Target... Dist: {distance_to_target:.2f}m | Pos: [{self.current_x:.2f}m, {self.current_y:.2f}m, {self.current_z:.2f}m]', 
                throttle_duration_sec=1.5
            )
            
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = WaypointNavigator()
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