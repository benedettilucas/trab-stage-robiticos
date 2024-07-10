#!/usr/bin/env python3
import rclpy

from rclpy.node import Node

from example_interfaces.msg import String

from sensor_msgs.msg import LaserScan #base_scan
from geometry_msgs.msg import Twist   #cmd_vel
from nav_msgs.msg import Odometry     #odom

#ex: ros2 interface show geometry_msgs_msg_Twist

class Publisher(Node):
	def __init__(self):
	    super().__init__("benedetti_nav_robot")
	    self.velocity = self.create_publisher(Twist, "cmd_vel", 10)
	    self.odometry = self.create_subscription(Odometry, "odom", self.callback_odom, 10)
	    self.laserScan= self.create_subscription(LaserScan, "base_scan", self.callback_scan, 10)

	    self.timer = self.create_timer(2, self.publish_msg)
	    #self.pubO =  self.create_timer(2, self.publish_msg)
	    #self.pubL =  self.create_timer(2, self.publish_msg)

	    self.get_logger().info("Publisher started")

	def publish_msg(self):
	    msg = Twist()
	    msg.linear.x = 0.2
	    self.velocity.publish(msg)

	def callback_odom(self, data):
	    self.px = data.pose.pose.position.x
	    self.py = data.pose.pose.position.y
	    self.pz = data.pose.pose.position.z
           # self.ox = data.pose.pose.orientation.x
	   #self.oy = data.pose.pose.orientation.y
           #self.oz = data.pose.pose.orientation.z
	    self.get_logger().info(f"x:{self.px}, y{self.py}, z{self.pz}")
	   #self.get_logger().info(f"ox:{self.ox}, oy{self.oy}, oz{self.oz}")

	def callback_scan(self, data):
        	self.get_logger().info(f'Ranges: {len(data.ranges)}')
        	self.get_logger().info(f'Min range: {min(data.ranges)}')
        	self.get_logger().info(f'Max range: {max(data.ranges)}')
        	self.get_logger().info(f'Angles: {data.angle_min} to {data.angle_max} with increment {data.angle_increment}')

def main(args=None):
	rclpy.init(args=None)
	node = Publisher()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == "__main__":
        main()

