#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

cmd_vel_ = Twist()
turtle_pose_ = Pose()

def turtlePose(msg):
    global turtle_pose_
    turtle_pose_ = msg
    
def main():
    global cmd_vel_, turtle_pose_
    rospy.init_node('turtle_pubsub')
    rate = rospy.Rate(10)
    
    rospy.loginfo('Waiting for turtlesim')
    rospy.wait_for_message('/turtle1/pose', Pose)
    rospy.Subscriber('/turtle1/pose', Pose, turtlePose)
    cmd_vel_pub_ = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    while not rospy.is_shutdown():
        if (turtle_pose_.x > 10):
            cmd_vel_.linear.x = 0
        else:
            cmd_vel_.linear.x = 1.0
        cmd_vel_pub_.publish(cmd_vel_)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass