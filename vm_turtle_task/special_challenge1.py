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

def normalize_angle(angle):
    """Normalize angle to [-pi, pi]"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

def angle_difference(target, current):
    """Calculate the smallest difference between two angles"""
    diff = normalize_angle(target - current)
    return abs(diff)

def main():
    global cmd_vel_, turtle_pose_
    rospy.init_node('turtle_square')
    rate = rospy.Rate(10)
    
    rospy.loginfo('Waiting for turtlesim')
    rospy.wait_for_message('/turtle1/pose', Pose)
    rospy.Subscriber('/turtle1/pose', Pose, turtlePose)
    cmd_vel_pub_ = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    # Square parameters
    side_length = 3.0  # Length of each side
    linear_speed = 1.0
    angular_speed = 1.0
    repeat_square = False  # Set to True if you want continuous squares
    
    # States: 0 = move forward, 1 = turn, 2 = finished
    state = 0
    side_count = 0
    start_x = None
    start_y = None
    start_theta = None
    
    while not rospy.is_shutdown():
        if state == 2:  # Finished state
            # Stop the turtle
            cmd_vel_.linear.x = 0.0
            cmd_vel_.angular.z = 0.0
            cmd_vel_pub_.publish(cmd_vel_)
            rospy.loginfo('Turtle stopped. Square completed!')
            break  # Exit the loop
            
        elif state == 0:  # Moving forward
            if start_x is None:
                start_x = turtle_pose_.x
                start_y = turtle_pose_.y
            
            # Calculate distance traveled (works for all directions)
            distance = math.sqrt((turtle_pose_.x - start_x)**2 + 
                               (turtle_pose_.y - start_y)**2)
            
            rospy.loginfo(f'Distance: {distance:.2f}, x: {turtle_pose_.x:.2f}, y: {turtle_pose_.y:.2f}')
            
            if distance < side_length:
                # Keep moving forward
                cmd_vel_.linear.x = linear_speed
                cmd_vel_.angular.z = 0.0
            else:
                # Stop and prepare to turn
                cmd_vel_.linear.x = 0.0
                cmd_vel_.angular.z = 0.0
                state = 1
                start_x = None
                start_y = None
                side_count += 1
                rospy.loginfo(f'Completed side {side_count}')
        
        elif state == 1:  # Turning 90 degrees
            if start_theta is None:
                start_theta = turtle_pose_.theta
                rospy.loginfo(f'Start turning from angle: {start_theta:.2f}')
            
            # Calculate angle turned (handles wraparound correctly)
            angle_turned = angle_difference(turtle_pose_.theta, start_theta)
            
            rospy.loginfo(f'Angle turned: {angle_turned:.2f} rad ({math.degrees(angle_turned):.2f} deg)')
            
            if angle_turned < math.pi / 2 - 0.05:  # 90 degrees minus tolerance
                # Keep turning
                cmd_vel_.linear.x = 0.0
                cmd_vel_.angular.z = angular_speed
            else:
                # Stop turning and prepare to move forward
                cmd_vel_.linear.x = 0.0
                cmd_vel_.angular.z = 0.0
                start_theta = None
                rospy.loginfo(f'Turn completed. Current angle: {turtle_pose_.theta:.2f}')
                
                # Check if square is completed
                if side_count > 4:
                    rospy.loginfo('Square completed!')
                    if repeat_square:
                        side_count = 0  # Reset and continue
                        state = 0
                    else:
                        state = 2  # Go to finished state
                else:
                    state = 0  # Continue to next side
        
        cmd_vel_pub_.publish(cmd_vel_)
        rate.sleep()
        
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass