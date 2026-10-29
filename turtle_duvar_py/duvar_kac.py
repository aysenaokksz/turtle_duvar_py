import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class DuvarKac(Node):

    def __init__(self):
        super().__init__('duvar_kac')

        # ROS 2 parametreleri
        self.declare_parameter('hiz', 2.0)
        self.declare_parameter('alt_sinir', 1.0)
        self.declare_parameter('ust_sinir', 10.0)

        self.pose = None
        self.donuyor = False
        self.hedef_aci = 0.0

        # Konum bilgisini dinle
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Hareket komutlarini yayinla
        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.timer = self.create_timer(0.1, self.hareket_et)

        self.get_logger().info(
            'Version 1.0 - Duvardan Kacan Kaplumbaga'
        )

    def pose_callback(self, msg):
        self.pose = msg

    def aci_farki(self, hedef, mevcut):
        return math.atan2(
            math.sin(hedef - mevcut),
            math.cos(hedef - mevcut)
        )

    def hareket_et(self):
        if self.pose is None:
            return

        hiz = float(self.get_parameter('hiz').value)
        alt_sinir = float(self.get_parameter('alt_sinir').value)
        ust_sinir = float(self.get_parameter('ust_sinir').value)

        x = self.pose.x
        y = self.pose.y
        theta = self.pose.theta

        msg = Twist()

        # Guvenli bolgenin merkezi
        merkez = (alt_sinir + ust_sinir) / 2.0

        # Duvar kontrolu
        duvara_yakin = (
            x < alt_sinir or
            x > ust_sinir or
            y < alt_sinir or
            y > ust_sinir
        )

        if duvara_yakin and not self.donuyor:
            self.donuyor = True

            # Merkeze dogru don
            self.hedef_aci = math.atan2(
                merkez - y,
                merkez - x
            )

            self.get_logger().info(
                f'Duvara yaklasildi! x={x:.2f}, y={y:.2f}'
            )

        if self.donuyor:
            fark = self.aci_farki(self.hedef_aci, theta)

            if abs(fark) > 0.05:
                msg.linear.x = 0.0
                msg.angular.z = max(
                    -1.5,
                    min(1.5, 3.0 * fark)
                )
            else:
                self.donuyor = False
                msg.linear.x = hiz
                msg.angular.z = 0.0
        else:
            msg.linear.x = hiz
            msg.angular.z = 0.0

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DuvarKac()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publisher.publish(Twist())

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
