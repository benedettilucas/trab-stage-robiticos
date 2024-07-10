import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
import random
import math

class RRTNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

class RRTRobot(Node):
    def __init__(self):
        super().__init__('rrt_robot')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        self.marker_publisher = self.create_publisher(MarkerArray, '/rrt_markers', 10)
        self.scan_data = None
        self.tree = [RRTNode(-7.0, -7.0)]  # Starting point (0, 0)
        self.goal = RRTNode(5.0, 4.0)  # Example goal, this would be dynamic in practice
        self.iterations = 1000
        self.delta = 0.5  # Step size
        self.timer = self.create_timer(1.0, self.expand_tree)

    def scan_callback(self, msg):
        self.scan_data = msg

    def is_collision(self, x, y):
        if self.scan_data is None:
            return False
        # Check if the point (x, y) is in collision with any obstacle
        # Simplified for example purposes, should be expanded for actual collision detection
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
        for _ in range(self.iterations):
            rand_x = random.uniform(-10.0, 10.0)
            rand_y = random.uniform(-10.0, 10.0)
            nearest_node = self.get_nearest_node(rand_x, rand_y)
            theta = math.atan2(rand_y - nearest_node.y, rand_x - nearest_node.x)
            new_x = nearest_node.x + self.delta * math.cos(theta)
            new_y = nearest_node.y + self.delta * math.sin(theta)

            if not self.is_collision(new_x, new_y):
                new_node = RRTNode(new_x, new_y)
                new_node.parent = nearest_node
                self.tree.append(new_node)

                if math.sqrt((new_x - self.goal.x)**2 + (new_y - self.goal.y)**2) < self.delta:
                    self.get_logger().info("Goal Reached!")
                    break

        self.publish_tree()

    def publish_tree(self):
        marker_array = MarkerArray()
        for node in self.tree:
            marker = Marker()
            marker.header.frame_id = "map"
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = node.x
            marker.pose.position.y = node.y
            marker.pose.position.z = 0
            marker.scale.x = 0.1
            marker.scale.y = 0.1
            marker.scale.z = 0.1
            marker.color.a = 1.0
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker_array.markers.append(marker)

        self.marker_publisher.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    rrt_robot = RRTRobot()
    rclpy.spin(rrt_robot)
    rrt_robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
