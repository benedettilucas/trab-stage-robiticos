#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import random
import math

class Publisher(Node):
    def __init__(self):
        super().__init__("benedetti_nav_robot")
        self.velocity = self.create_publisher(Twist, "cmd_vel", 10)
        self.odometry = self.create_subscription(Odometry, "odom", self.callback_odom, 10)
        self.laserScan = self.create_subscription(LaserScan, "base_scan", self.callback_scan, 10)

        self.timer = self.create_timer(0.1, self.publish_msg)
        self.get_logger().info("Publisher started")
        
        self.px = 0.0
        self.py = 0.0
        self.pz = 0.0
        self.ox = 0.0
        self.oy = 0.0
        self.oz = 0.0
        self.scan_data = 0.0
        self.step = 0.0
        self.final = 0.0

    def publish_msg(self):
    	#0.1914 - 45 graus 0.382669
    	#0.3827 - 90 graus
        msg = Twist()
        
        if self.step == 0.0 and self.oz <= 0.3826 and self.px == 0:
        	msg.angular.z = 0.392
        elif self.step == 0.0 and  self.oz >= -0.3826 and self.px <= 9.5:
        	msg.linear.x = 1.0
        elif self.step == 0.0 and self.oz >= -0.3826 and self.px >= 9.5 and self.px < 13:
        	msg.angular.z = -0.392
        elif self.step == 0.0 and self.oz <= -0.3826 and self.px <= 13:
        	msg.linear.x = 1.0
        elif self.step == 0.0 and self.oz <= 0.3826 and self.px >= 13 and self.px < 14:
        	msg.angular.z = 0.392
        elif self.step == 0.0 and self.oz >= 0.3826 and self.px <= 14:
        	msg.linear.x = 1.0
        elif self.step == 0.0 and self.oz >= -0.3826 and self.px >= 14 and self.px < 17:
        	msg.angular.z = -0.392
        elif self.step == 0.0 and self.oz <= -0.3826 and self.px <= 19.3:
        	msg.linear.x = 1.0
        elif self.step == 0.0 and self.oz >= -0.92 and self.px >= 19.3:
        	msg.angular.z = -0.392
        	
        elif self.oz <= -0.92 and self.px >= 17 and self.scan_data > 0.5:
        	self.step = 1.0
        	msg.linear.x = 1.0
#INDO PARA O SEGUNDO PONTO
        elif self.final == 0 and self.step == 2.0 and self.oz <= 0.92 and self.px <= 18 and self.px >= 17:
        	msg.angular.z = 0.392
        elif self.final == 0 and self.step == 2.0 and self.scan_data > 0.6 and self.px >= 16:
        	msg.linear.x = 1.0
        elif self.final == 0 and self.step == 2.0 and self.oz >= -0.92 and self.px < 16 and self.px >= 15:
        	msg.angular.z = -0.392
        elif self.final == 0 and self.step == 2.0 and self.oz <= -0.92 and self.scan_data > 1.0 and self.px >= 14.6:
        	msg.linear.x = 1.0
        elif self.final == 0 and self.step == 2.0 and self.oz <= 0.92 and self.px < 14.6 and self.px >= 12:
        	msg.angular.z = 0.392
        elif self.final == 0 and self.step == 2.0 and self.oz >= 0.92 and self.px >= 11 and self.px <= 14.6 and self.scan_data > 0.8:
        	msg.linear.x = 1.0
        elif self.final == 0 and self.step == 2.0 and self.oz >= -0.92 and self.px < 11 and self.px > 8:
        	msg.angular.z = -0.392
        elif self.final == 0 and self.step == 2.0 and self.oz <= -0.92 and self.px >= 5.0 and self.px <= 12.0:
        	msg.linear.x = 1.0
        elif self.final == 0 and self.step == 2.0 and self.oz <= -0.3826 and self.px <= 5.0:
        	msg.angular.z = 0.392
        elif self.final != 2 and self.step == 2.0 and self.oz <= 0.3826 and self.scan_data > 4.5:
        	msg.linear.x = 1.0
        	self.final = 1.0
        elif  (self.final == 2.0 and self.oz <= 0.1914)or (self.final == 1.0 and self.px >= 9.0 and self.oz <= 0.1914 and self.scan_data > 0.5):
        	msg.angular.z = 0.392
        	self.final = 2.0
        elif self.final == 2.0 and self.px >= 9 and self.oz >= 0.1914 and self.scan_data > 0.35:
        	msg.linear.x = 0.5
        else:
        	if self.step == 1.0 and self.scan_data < 0.6:
        		self.step = 2.0
        	msg.linear.x = 0.0
        	msg.angular.z = 0.0

        self.velocity.publish(msg)

    def callback_odom(self, data):
        self.px = data.pose.pose.position.x
        self.py = data.pose.pose.position.y
        self.pz = data.pose.pose.position.z
        self.ox = data.pose.pose.orientation.x
        self.oy = data.pose.pose.orientation.y
        self.oz = data.pose.pose.orientation.z
#        self.get_logger().info(f"step: {self.step}")
        self.get_logger().info(f"translacao em x:{self.px}")
        self.get_logger().info(f"angulos em z:{self.oz}")

    def callback_scan(self, data):
        self.scan_data = data.ranges[len(data.ranges)//2]
        self.get_logger().info(f'sensor frente: {data.ranges[len(data.ranges)//2]}')
#        self.get_logger().info(f'Min range: {min(data.ranges)}')
#        self.get_logger().info(f'Max range: {max(data.ranges)}')
#        self.get_logger().info(f'Angles: {data.angle_min} to {data.angle_max} with increment {data.angle_increment}')



def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
