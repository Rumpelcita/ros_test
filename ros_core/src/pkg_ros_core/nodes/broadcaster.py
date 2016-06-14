#!/usr/bin/env python  
import roslib
roslib.load_manifest('pkg_ros_core')
import rospy

from math import fabs, fmod, cos, sin, pi

import std_srvs.srv
import turtlesim.msg
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import String

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

State = enum(
    'FORWARD',
    'STOP_FORWARD',
    'TURN',
    'STOP_TURN')
    
global g_pose
g_pose = Pose()
global g_goal
g_goal = Pose()

g_state = State.FORWARD;
g_last_state = State.FORWARD;
g_first_goal_set = False;

def pose_callback(pose):
    global g_pose
    g_pose = pose
    
def has_reached_goal():
    reached = fabs(g_pose.x - g_goal.x) < 0.1 and fabs(g_pose.y - g_goal.y) < 0.1 and fabs(g_pose.theta - g_goal.theta) < 0.01
    return reached

def has_stopped():
    stopped = g_pose.angular_velocity < 0.0001 and g_pose.linear_velocity < 0.0001
    return stopped
  
def print_goal():
    printed_str = "New goal %s %s, %s" % (g_goal.x, g_goal.y, g_goal.theta)
    rospy.loginfo(printed_str)
    
def command_turtle(twist_pub, velocity_linear, velocity_angular):
    twist = Twist(Vector3((velocity_linear),0,0), Vector3(0,0,(velocity_angular)))
    twist_pub.publish(twist)
    
def stop_forward(twist_pub):
    global g_goal
    global g_state
    if has_stopped():
        rospy.loginfo("Stopped")
        g_state = State.TURN
        g_goal.x = g_pose.x
        g_goal.y = g_pose.y
        g_goal.theta = fmod(g_pose.theta + (4*pi)/5.0, 2*pi)
        rospy.loginfo("theta: %r" % g_goal.theta)
        print_goal()
    else:
        command_turtle(twist_pub, 0, 0)

def stop_turn(twist_pub):
    global g_goal
    global g_state
    if has_stopped():
        rospy.loginfo("Stopped")
        g_state = State.FORWARD
        g_goal.x = cos(g_pose.theta) * 2 + g_pose.x
        g_goal.y = sin(g_pose.theta) * 2 + g_pose.y
        g_goal.theta = g_pose.theta
        print_goal()
    else:
        command_turtle(twist_pub, 0, 0)
        
def forward(twist_pub):
    global g_state
    if has_reached_goal():
        g_state = State.STOP_FORWARD
        command_turtle(twist_pub, 0, 0)
    else:
        command_turtle(twist_pub, 1.0, 0.0)
        
def turn(twist_pub):
    global g_state
    if has_reached_goal():
        g_state = State.STOP_TURN
        command_turtle(twist_pub, 0, 0)
    else:
        command_turtle(twist_pub, 0.0, 0.3)

def timer_callback(timer):
    global g_goal
    global g_state
    global g_first_goal_set
    if not g_pose:
        return

    if not g_first_goal_set:
        g_first_goal_set = True
        g_state = State.FORWARD
        g_goal.x = cos(g_pose.theta) * 2 + g_pose.x
        g_goal.y = sin(g_pose.theta) * 2 + g_pose.y
        g_goal.theta = g_pose.theta
        print_goal()
        
    if g_state == State.FORWARD:
        forward(twist_pub);
    elif g_state == State.STOP_FORWARD:
        stop_forward(twist_pub)
    elif g_state == State.TURN:
        turn(twist_pub)
    elif g_state == State.STOP_TURN:
        stop_turn(twist_pub)

if __name__ == '__main__':
    rospy.init_node('turtle_broadcaster')
    pose_sub = rospy.Subscriber('turtle1/pose', Pose, pose_callback)
    twist_pub = rospy.Publisher('turtle1/cmd_vel',Twist, queue_size = 10)
    empty = std_srvs.srv.Empty
    timer = rospy.Timer(rospy.Duration(0.016), timer_callback)
    rospy.spin()
