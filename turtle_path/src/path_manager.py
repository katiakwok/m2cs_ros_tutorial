#!/usr/bin/env python
import rospy
from math import pi, fmod, sin, cos, sqrt
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_path.srv import SetOrientation,WalkDistance

# hint: some imports are missing

cur_pos = Pose()

def cb_pose(data): # get the current position from subscribing the turtle position
    global cur_pos
    cur_pos = data

def cb_walk(req):
    if (req.distance < 0):
        return False

    # hint: calculate the projected (x, y) after walking the distance,
    # and return false if it is outside the boundary
    projected_x = cur_pos.x + req.distance * cos(cur_pos.theta)
    projected_y = cur_pos.y + req.distance * sin(cur_pos.theta)
    if (projected_x<0 or projected_x>11):
        return False
    if (projected_y<0 or projected_y>11):
        return False

    rate = rospy.Rate(100) # 100Hz control loop

    distance = sqrt((projected_x-cur_pos.x)**2 + (projected_y-cur_pos.y)**2)
    while (distance > 0.05): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: you need to use the formula for distance between two points
        vel = Twist()
        vel.linear.x = distance
        pub.publish(vel)
        
        rate.sleep()
    
    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    vel.linear.x = 0
    pub.publish(vel)

    return True

def cb_orientation(req):

    rate = rospy.Rate(100) # 100Hz control loop
    
    angles_distance = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
    while (angles_distance > 0.05): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: signed smallest distance between two angles: 
        # see https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
        #     dist = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
        vel = Twist()
        vel.angular.z = angles_distance
        pub.publish(vel)
        
        rate.sleep()
    
    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    vel.angular.z = 0
    pub.publish(vel)

    return True

if __name__ == '__main__':
    rospy.init_node('path_manager')
    
    pub = rospy.Publisher('turtle1/cmd_vel',Twist, queue_size = 1) # publisher of the turtle velocity
    sub = rospy.Subscriber('turtle1/pose',Pose,cb_pose)# subscriber of the turtle position, callback to cb_pose
    
    ## init each service server here:
    rospy.Service('set_orientation',SetOrientation,cb_orientation)		# callback to cb_orientation
    rospy.Service('walk_distance',WalkDistance,cb_walk)		# callback to cb_walk
    
    rospy.spin()
