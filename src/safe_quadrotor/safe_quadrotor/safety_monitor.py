import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
# Import the built-in sensor data QoS profile
from rclpy.qos import qos_profile_sensor_data

class SafetyMonitor(Node):
    def __init__(self):
        super().__init__('safety_monitor')
        
        # Subscribe to /scan using the matching Best Effort sensor profile
        self.scan_sub = self.create_subscription(
            LaserScan, 
            '/scan', 
            self.scan_callback, 
            qos_profile_sensor_data
        )
        
        self.safe_distance_threshold = 1.5 
        self.get_logger().info('Safety Monitor Active with Sensor QoS. Listening for data...')

    def scan_callback(self, msg):
        # Filter out invalid, zero, or out-of-range readings safely
        valid_ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        
        if not valid_ranges:
            self.get_logger().info('Receiving scan messages, but no valid objects within range limits.', throttle_duration_sec=5.0)
            return

        # Locate the closest object distance detected
        min_distance = min(valid_ranges)
        
        if min_distance < self.safe_distance_threshold:
            self.get_logger().warn(
                f'⚠️ CRITICAL SAFETY BREACH! Obstacle detected at only {min_distance:.2f}m! (Limit: {self.safe_distance_threshold}m)',
                throttle_duration_sec=1.0
            )
        else:
            self.get_logger().info(
                f'Status: Safe. Nearest obstacle distance: {min_distance:.2f}m',
                throttle_duration_sec=2.0
            )

def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitor()
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