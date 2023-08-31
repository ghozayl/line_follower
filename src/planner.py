#!/usr/bin/env python3

import sys
import rospy
import cv2
from cv_bridge import *
from sensor_msgs.msg import Image
from std_msgs.msg import *

bridge = CvBridge()
direction = "GO"  # Initialize the direction variable with a default value.

def is_y(vel):
    return vel > 100

def plan(left, right):
    global direction
    print(left, right)

    if is_y(left) and not is_y(right):
        direction = "LEFT"
    elif  is_y(left) and  is_y(right):
        direction = "GO"
    elif not is_y(left) and is_y(right):
        direction = "RIGHT"

def pub(go_pub, direction):
    message = String()
    message.data = direction
    go_pub.publish(message)

def imgcallback(data):
    global gray, direction
    xl=320
    xr=480
    y=550
    l_point=(xl, y)
    r_point=(xr, y)

    img = bridge.imgmsg_to_cv2(data, "bgr8")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plan(gray[y][xl], gray[y][xr])

    gray = cv2.line(gray, l_point, r_point, 0,5)
    #cv2.imshow("image", gray)
    #cv2.waitKey(3)
    
    if direction =="GO":
     gray=cv2.circle(gray,(int((xl+xr)/2),y),10,255,5)
    if direction =="LEFT":
     gray=cv2.circle(gray,l_point,10,255,5)
    if direction =="RIGHT":
     gray=cv2.circle(gray,r_point,10,255,5)

    cv2.imshow("image", gray)
    cv2.waitKey(3)
    # Pass the publisher and direction to the pub() function
    pub(go_pub, direction)
    print(direction)
def main():
    global image_sub, go_pub

    print("Hey Universe!")
    rospy.init_node("my_planner", anonymous=True)

    # Create the publisher once in the main function
    go_pub = rospy.Publisher("/motor_commands", String, queue_size=10)

    #image_sub = rospy.Subscriber("/camera/image_raw", Image, imgcallback)
    image_sub = rospy.Subscriber("/spcbot/camera/image_raw", Image, imgcallback)
    print(direction)


    rospy.spin()

if __name__ == "__main__":
    main()
