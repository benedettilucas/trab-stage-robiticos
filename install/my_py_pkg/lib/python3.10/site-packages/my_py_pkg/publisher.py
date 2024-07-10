#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class Publisher(Node):
	def __init__(self):
	    super().__init__("publisher")
	    self.publisher = self.create_publisher(String, "hello_world", 10)
	    self.timer = self.create_timer(2, self.publish_msg)
	    self.get_logger().info("Publisher started")

	def publish_msg(self):
		msg = String()
		msg.data = "Minha mensagem personalizada"
		self.publisher.publish(msg)

def main(args=None):
	rclpy.init(args=None)
	node = Publisher()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == "__main__":
        main()

