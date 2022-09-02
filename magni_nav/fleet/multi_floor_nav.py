#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import threading
from geometry_msgs.msg import PoseWithCovarianceStamped
import os 

current_floor = 0
floor_to_height = {0:0.2, 1: 12.2, 2:24.2, 3: 36.2}
floor_to_map ={0: "ground_v1", 1: "1f_v1", 2: "2f_v1", 3: "3f_v1"}



def go_to_goal(point, floor):
	rospy.init_node("multi_floor_listener", anonymous = True)
	client = actionlib.SimpleActionClient('/move_base',MoveBaseAction)
	global current_floor
	if current_floor != floor:
		#robot go to 0 0
		client.wait_for_server()
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.orientation.w = 1.0
		goal.target_pose.pose.orientation.x = 0.0
		goal.target_pose.pose.orientation.y = 0.0
		client.send_goal_and_wait(goal)
		print(1)
		current_floor = floor
		#robot move to current floor
		robot_floor_command = "rostopic pub -1 /gazebo/set_model_state gazebo_msgs/ModelState \"model_name: 'magni' \n"\
		"pose:\n"\
		"  position:\n"\
		"    x: 0.0\n"\
		"    y: 0.0\n"\
		"    z: " + str(floor_to_height[floor]) + "\n"\
		"  orientation: \n"\
		"    x: 0.0\n"\
		"    y: 0.0\n"\
		"    z: 0.0\n"\
		"    w: 1.0\""
		os.system(robot_floor_command)

		#change map
		map_name = floor_to_map[floor]
		change_map_command = "rosrun map_server map_server /home/vtl/multi_floor_nav/src/magni_nav/maps/" + map_name + ".yaml"
		map_thread = threading.Thread(target=os.system, args = [change_map_command])
		map_thread.start()
		
		#wait a little
		rospy.sleep(5)
		#robot go to goal
		client.wait_for_server()
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.position.x = point[0]
		goal.target_pose.pose.position.y = point[1]
		goal.target_pose.pose.orientation.w = 1.0
		client.send_goal_and_wait(goal)
	else:
		client.wait_for_server()
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.position.x = point[0]
		goal.target_pose.pose.position.y = point[1]
		goal.target_pose.pose.orientation.w = 1.0
		client.send_goal_and_wait(goal)

