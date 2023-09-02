#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64, String

left_wheel_pub = None
right_wheel_pub = None

def commands_callback(msg):
    left_speed = 0.0
    right_speed = 0.0

    m=1
    t=.1
    command = msg.data

    if command == "GO":
        left_speed = m
        right_speed = m
    elif command == "GO_REALLY_FAST":
        left_speed = 10.0  # radians per second
        right_speed = 10.0
    elif command == "BACK":
        left_speed = -0.5
        right_speed = -0.5
    elif command == "LEFT":
        left_speed = t
        right_speed =m
    elif command == "RIGHT":
        left_speed = m
        right_speed = t
    else:
        left_speed = 0.0  # Stop the robot
        right_speed = 0.0

    # send messages
    msg_left = Float64()
    msg_left.data = left_speed

    msg_right = Float64()
    msg_right.data = right_speed

    left_wheel_pub.publish(msg_left)
    right_wheel_pub.publish(msg_right)

def main():
    rospy.init_node("motorController")
    rospy.Subscriber("motor_commands", String, commands_callback)

    global left_wheel_pub, right_wheel_pub
    left_wheel_pub = rospy.Publisher("/left_wheel_controller/command", Float64, queue_size=1000)
    right_wheel_pub = rospy.Publisher("/right_wheel_controller/command", Float64, queue_size=1000)

    rospy.spin()

if __name__ == "__main__":
    main()
