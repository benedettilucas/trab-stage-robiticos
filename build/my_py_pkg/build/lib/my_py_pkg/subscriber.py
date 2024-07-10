#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class Subscriber(Node):
	def __init__(self):
	    super().__init__("subscriber")
	    self.publisher = self.create_subscription(String, "hello_word", self.callback_subscriber, 10)
	    self.get_logger().info("Subscription started")

	def callback_subscriber(self, msg):
		self.get_logger().info(msg.data)

def main(args=None):
	rclpy.init(args=None)
	node = Subscriber()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == "__main__":
        main()
