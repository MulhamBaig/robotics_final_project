import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class FlightController(Node):
    def __init__(self):
        super().__init__('flight_controller')
        # Publish directly to the bridged Gazebo velocity topic
        self.publisher_ = self.create_publisher(Twist, '/model/simple_drone/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback) # 10Hz loop rate
        self.counter = 0
        self.get_logger().info('Flight Controller Active. Beginning Autonomous Test...')

    def timer_callback(self):
        msg = Twist()
        self.counter += 1

        # Phase 1: Takeoff (0 to 4 seconds) -> Move upwards
        if self.counter < 40:
            msg.linear.z = 0.5
            self.get_logger().info('Action: Taking Off...', throttle_duration_sec=1.0)
            
        # Phase 2: Stable Hover (4 to 10 seconds) -> Zero vertical velocity
        elif self.counter < 100:
            msg.linear.z = 0.0
            self.get_logger().info('Action: Hovering Steady...', throttle_duration_sec=1.0)
            
        # Phase 3: Descent and Land (10 to 14 seconds) -> Move downwards
        elif self.counter < 140:
            msg.linear.z = -0.5
            self.get_logger().info('Action: Landing...', throttle_duration_sec=1.0)
            
        # Phase 4: Complete Stop
        else:
            msg.linear.z = 0.0
            self.get_logger().info('Test Routine Complete.', throttle_duration_sec=5.0)

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FlightController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Avoid double-shutdown error in ROS 2 Jazzy
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()