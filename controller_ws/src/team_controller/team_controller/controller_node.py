"""Simulator practice controller; stops on stale scans and on shutdown."""
import time
import signal
import csv
import math
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.signals import SignalHandlerOptions
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ament_index_python.packages import get_package_share_directory
from ackermann_msgs.msg import AckermannDriveStamped

from .steering import command
from .route import follow


class Controller(Node):
    def __init__(self):
        super().__init__('team_controller')
        self.declare_parameter('max_speed', 1.0)
        self.max_speed = float(self.get_parameter('max_speed').value)
        if not 0 < self.max_speed <= 1.5:
            raise ValueError('max_speed must be between 0 and 1.5 m/s')
        self.publisher = self.create_publisher(AckermannDriveStamped, '/drive', 10)
        self.last_scan = 0.0
        self.target = (0.0, 0.0)
        self.last_odom = 0.0
        self.front_clearance = 0.0
        self.declare_parameter('mode', 'centerline')
        self.mode = self.get_parameter('mode').value
        if self.mode not in ('centerline', 'gap'):
            raise ValueError('mode must be centerline or gap')
        if self.mode == 'centerline':
            route = Path(get_package_share_directory('f1tenth_gym_ros')) / 'maps/levine_centerline.csv'
            with route.open() as stream:
                self.points = [tuple(map(float, row[:2])) for row in csv.reader(
                    line for line in stream if line.strip() and not line.lstrip().startswith('#'))]
            if len(self.points) < 3:
                raise ValueError('Centerline requires at least three points')
            self.create_subscription(Odometry, '/ego_racecar/odom', self.odom, 10)
        self.create_subscription(LaserScan, '/scan', self.scan, qos_profile_sensor_data)
        self.create_timer(0.05, self.tick)
        self.get_logger().info(f'Autonomous {self.mode} controller active; speed limit {self.max_speed} m/s')

    def scan(self, msg):
        if self.mode == 'gap':
            self.target = command(msg.ranges, msg.angle_min, msg.angle_increment,
                                  msg.range_min, msg.range_max, self.max_speed)
        front = [value if math.isfinite(value) and value >= msg.range_min else 0.0
                 for i, value in enumerate(msg.ranges)
                 if abs(msg.angle_min+i*msg.angle_increment) < math.radians(12)]
        self.front_clearance = min(front, default=0.0)
        self.last_scan = time.monotonic()

    def odom(self, msg):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = math.atan2(2*(q.w*q.z+q.x*q.y), 1-2*(q.y*q.y+q.z*q.z))
        self.target = follow(self.points, p.x, p.y, yaw, self.max_speed)
        self.last_odom = time.monotonic()

    def publish(self, steering, speed):
        msg = AckermannDriveStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'ego_racecar/base_link'
        msg.drive.steering_angle = steering
        msg.drive.speed = speed
        self.publisher.publish(msg)

    def tick(self):
        fresh = time.monotonic()-self.last_scan < 0.5
        if self.mode == 'centerline':
            fresh = fresh and time.monotonic()-self.last_odom < 0.5
        steering, speed = self.target if fresh else (0.0, 0.0)
        speed = min(speed, max(0.0, (self.front_clearance-0.45)*0.8))
        self.publish(steering, speed)


def main(args=None):
    # Keep ROS alive long enough to publish a stop on Ctrl+C or SIGTERM.
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    def interrupt(_signum, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, interrupt)
    node = Controller()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publish(0.0, 0.0)
            time.sleep(0.1)
        node.destroy_node()
        rclpy.try_shutdown()
