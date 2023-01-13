#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, SetPenRequest
from m2_ps4.msg import Ps4Data
from std_srvs.srv import Empty, EmptyRequest
# hint: some imports are missing

old_data = Ps4Data()
k=0
def callback(data):
    global old_data
    global k
    # you should publish the velocity here!

    cmd_vel = Twist()
 
    # hint: to detect a button being pressed, you can use the following pseudocode:
    # if ((data.button is pressed) and (old_data.button not pressed)),
    # then do something...

    if (data.dpad_y > 0 and old_data.dpad_y != data.dpad_y):
        k+=1
    if (data.dpad_y < 0 and old_data.dpad_y != data.dpad_y):
        k-=1
    if k < 1:
        k = 1
    if k > 5:
        k = 5
    
    
    cmd_vel.linear.x = data.hat_ly * k
    
    cmd_vel.angular.z = data.hat_rx * k
    
    
    pub.publish(cmd_vel)


    if (data.ps == True and data.ps != old_data.ps):
        srv_col1(EmptyRequest())

    pen = SetPenRequest()

    if (data.triangle == True and data.triangle != old_data.triangle):
        pen.r = 0
        pen.g = 255
        pen.b = 0
        srv_col(pen)
    elif (data.circle == True and data.circle != old_data.circle):
        pen.r = 255
        pen.g = 0
        pen.b = 0
        srv_col(pen)
    elif (data.cross == True and data.cross != old_data.cross):
        pen.r = 0
        pen.g = 0
        pen.b = 255
        srv_col(pen)
    elif (data.square == True and data.square != old_data.square):
        pen.r = 255
        pen.g = 0
        pen.b = 255
        srv_col(pen)
    
    old_data = data

if name == 'main':
    rospy.init_node('ps4_controller')
    
    pub = rospy.Publisher('turtle1/cmd_vel',Twist,queue_size=1)# publisher object goes here... hint: the topic type is Twist
    sub = rospy.Subscriber('input/ps4_data',Ps4Data,callback)# subscriber object goes here
    
    # one service object is needed for each service called!
    srv_col = rospy.ServiceProxy('turtle1/set_pen',SetPen)# service client object goes here... hint: the srv type is SetPen
    # fill in the other service client object...
    srv_col1 = rospy.ServiceProxy('clear', Empty)
    rospy.spin()
