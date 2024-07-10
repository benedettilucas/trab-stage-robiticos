#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import random
import math

class RRTNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

class Publisher(Node):
    def __init__(self):
        super().__init__("benedetti_nav_robot")
        self.velocity = self.create_publisher(Twist, "cmd_vel", 10)
        self.odometry = self.create_subscription(Odometry, "odom", self.callback_odom, 10)
        self.laserScan = self.create_subscription(LaserScan, "base_scan", self.callback_scan, 10)

        self.timer = self.create_timer(2, self.publish_msg)
        self.get_logger().info("Publisher started")

        # RRT related attributes
        self.tree = [RRTNode(-7.0, -7.0)]  # Starting point (0, 0)
        self.goal = RRTNode(5.0, 4.0)  # Example goal
        self.delta = 0.5  # Step size
        self.scan_data = None

    def publish_msg(self):
        if len(self.tree) < 100:  # Number of iterations
            self.expand_tree()
        else:
            self.get_logger().info("RRT complete, goal should be reached soon.")

        if self.tree[-1].x == self.goal.x and self.tree[-1].y == self.goal.y:
            self.get_logger().info("Goal Reached!")
            return

        nearest_node = self.tree[-1]
        theta = math.atan2(self.goal.y - nearest_node.y, self.goal.x - nearest_node.x)
        msg = Twist()
        msg.linear.x = 0.2 * math.cos(theta)
        msg.linear.y = 0.2 * math.sin(theta)
        self.velocity.publish(msg)

    def callback_odom(self, data):
        self.px = data.pose.pose.position.x
        self.py = data.pose.pose.position.y
        self.pz = data.pose.pose.position.z
        self.get_logger().info(f"x:{self.px}, y:{self.py}, z:{self.pz}")

    def callback_scan(self, data):
        self.scan_data = data
        self.get_logger().info(f'Ranges: {len(data.ranges)}')
        self.get_logger().info(f'Min range: {min(data.ranges)}')
        self.get_logger().info(f'Max range: {max(data.ranges)}')
        self.get_logger().info(f'Angles: {data.angle_min} to {data.angle_max} with increment {data.angle_increment}')

    def is_collision(self, x, y):
        if self.scan_data is None:
            return False
        # Simplified collision check for example purposes
        for angle in range(len(self.scan_data.ranges)):
            dist = self.scan_data.ranges[angle]
            angle_rad = self.scan_data.angle_min + angle * self.scan_data.angle_increment
            obs_x = dist * math.cos(angle_rad)
            obs_y = dist * math.sin(angle_rad)
            if math.sqrt((x - obs_x)**2 + (y - obs_y)**2) < self.delta:
                return True
        return False

    def get_nearest_node(self, x, y):
        nearest_node = self.tree[0]
        min_dist = float('inf')
        for node in self.tree:
            dist = math.sqrt((node.x - x)**2 + (node.y - y)**2)
            if dist < min_dist:
                nearest_node = node
                min_dist = dist
        return nearest_node

    def expand_tree(self):
        rand_x = random.uniform(-8.0, 8.0)
        rand_y = random.uniform(-8.0, 8.0)
        nearest_node = self.get_nearest_node(rand_x, rand_y)
        theta = math.atan2(rand_y - nearest_node.y, rand_x - nearest_node.x)
        new_x = nearest_node.x + self.delta * math.cos(theta)
        new_y = nearest_node.y + self.delta * math.sin(theta)

        if not self.is_collision(new_x, new_y):
            new_node = RRTNode(new_x, new_y)
            new_node.parent = nearest_node
            self.tree.append(new_node)

def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
