#!/usr/bin/env python3
import rospy
from turtlesim.srv import SetPen, TeleportAbsolute, TeleportAbsoluteResponse

def gotoPose(req):
    pose_x_ = req.x
    pose_y_ = req.y
    theta_ = req.theta
    rospy.loginfo(f'Service => x: {pose_x_} y: {pose_y_} theta: {theta_}')
    
    # Actually teleport the turtle
    try:
        teleport_service = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        teleport_service(pose_x_, pose_y_, theta_)
        rospy.loginfo("Turtle teleported successfully!")
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
    
    return TeleportAbsoluteResponse()

def turtleSetPen(r, g, b, width, off):
    try:
        turtle_setpen_ = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
        resp_ = turtle_setpen_(r, g, b, width, off)
        return resp_
    except rospy.ServiceException as e:
        rospy.logerr(f"SetPen service call failed: {e}")
        return None
    
def main():
    rospy.init_node('lab2_service')
    
    rospy.loginfo("Waiting for turtlesim services...")
    rospy.wait_for_service('/turtle1/set_pen')
    rospy.wait_for_service('/turtle1/teleport_absolute')
    rospy.loginfo("Turtlesim services found!")
    
    # Set pen to blue, width 5
    turtleSetPen(0, 0, 255, 5, 0)
    rospy.loginfo("Pen set to blue")
    
    # Create the service
    service = rospy.Service('/turtle1/gotoPose', TeleportAbsolute, gotoPose)
    rospy.loginfo("gotoPose service is now available at /turtle1/gotoPose")
    
    # Keep the node running
    rospy.loginfo("Node is spinning... Press Ctrl+C to exit")
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node shutdown")