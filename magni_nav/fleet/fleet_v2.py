#!/usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import threading
import multiprocessing
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped

import socket

main_loop_running = False
mission = []
pending = []
movable_threshold = 1.5

table_1_x = 0
table_1_y = 0
table_2_x = 0
table_2_y = 0


#define all robots 
available_robots = []
unavailable_robots = []
pending_table = []

lookup_robot_from_table = {1:"magni_1", 2: "magni_2"}

pending_table_handler_running = False

available_robots = ["magni_1", "magni_2"]

class robot:
	def __init__(self, name):
		self.name = name
		self.curr_point = tuple()
		self.force_stop = False
		self.client = actionlib.SimpleActionClient(self.name+'/move_base',MoveBaseAction)

	def go_to_goal(self, to_start_point = False):	
		self.client.wait_for_server()
		self.goal = MoveBaseGoal()
		self.goal.target_pose.header.frame_id = "map"
		self.goal.target_pose.header.stamp = rospy.Time.now()
		self.goal.target_pose.pose.orientation.w = 1.0
		if to_start_point:
			self.goal.target_pose.pose.position.x = self.start_point[0]
			self.goal.target_pose.pose.position.y = self.start_point[1]

		else:
			self.goal.target_pose.pose.position.x = self.goal_point[0]
			self.goal.target_pose.pose.position.y = self.goal_point[1]
		

		self.client.send_goal(self.goal)
		print("start waiting result")
		wait = self.client.wait_for_result()
		if not self.force_stop:
			remove_from_list(mission, self.name)
			
			if to_start_point:
				available_robots.append(self.name)

			print("arrived mission is:", mission, "pending is: ", pending, "available is: ", available_robots)

		else:
			self.force_stop = False

	def stop(self):
		self.client.cancel_all_goals()

	def set_goal_point (self, goal_point):
		self.goal_point = goal_point

	def set_start_point (self, start_point):
		self.start_point = start_point


magni_1 = robot("magni_1")
magni_2 = robot("magni_2")

def define_robots():
	magni_1.set_start_point((-7.5, -2.5))
	magni_2.set_start_point((-7.5, -3.5))

def update_robot_state():
	global table_1_x 
	global table_1_y 
	global table_2_x 
	global table_2_y 
	HOST = '0.0.0.0'
	PORT = 9998
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(5)
	s.settimeout(None)
	while True:
		conn, addr =s.accept()
		indata = conn.recv(1024)
		message = str(indata.decode())
		array = message.split()
		print("message is ", type(message), array)
		request_type = array[0]
		x = float(array[1])
		y = float(array[2])
		if request_type == "1":
			magni_1.set_start_point((x, y))
		elif request_type == "2":
			magni_2.set_start_point((x, y))
		elif request_type == "3":
			table_1_x = x
			table_1_y = y
		elif request_type == "4":
			table_2_x = x
			table_2_y = y


def tcp_connection():
	global pending_table_handler_running
	HOST = '0.0.0.0'
	PORT = 9999
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(5)
	s.settimeout(None)
	while True:
		conn, addr =s.accept()
		indata = conn.recv(1024)
		table_number = int(indata.decode())
		
		if table_number <0:
			table_number *=-1
			curr_robot = lookup_robot_from_table[table_number]
			#globals()[curr_robot].go_to_goal(to_start_point = True)
			to_start_point_thread = threading.Thread(target = globals()[curr_robot].go_to_goal, args =  [True])
			to_start_point_thread.start()
			
		else:
			pending_table.append(table_number)
			if not pending_table_handler_running:
				table_handler_thread = threading.Thread(target = pending_table_handler)
				table_handler_thread.start()
		conn.close()

def pending_table_handler():
	print("here,", pending_table)
	global table_1_x 
	global table_1_y 
	global table_2_x 
	global table_2_y 
	global pending_table_handler_running
	global lookup_robot_from_table
	pending_table_handler_running = True
	rate = rospy.Rate(1)
	while pending_table:
		if available_robots:
			print("available robot is ", bool(available_robots))
			curr_table = pending_table.pop()
			curr_robot = available_robots.pop(0)
			lookup_robot_from_table[curr_table] = curr_robot
			if int(curr_table) == 1:
				x = table_1_x 
				y = table_1_y
			elif int(curr_table) ==2:
				x = table_2_x 
				y = table_2_y
			else:
				x = 1
				y = 1

			globals()[curr_robot].set_goal_point((x, y))
			pending.append(globals()[curr_robot].name)
			unavailable_robots.append(curr_robot)
			global main_loop_running
			if not main_loop_running:
				main_loop_running = True
				main_loop_thread = threading.Thread(target = main_loop)
				main_loop_thread.start()
		rate.sleep()
	pending_table_handler_running = False


def new_command_listener():
	rospy.Subscriber("robot_command", String, callback)
	rospy.spin()

def callback(data):
	data = data.data
	name, x, y = data.split()	
	globals()[name] = robot(name, (float(x), float(y)))

	print(globals()[name].name)
	remove_from_list(mission, name)
	remove_from_list(pending, name)
	pending.append(name)
	print(data)
	print(pending)
	global main_loop_running
	if not main_loop_running:
		main_loop_running = True
		main_loop_thread = threading.Thread(target = main_loop)
		main_loop_thread.start()


def distance (r1, r2):
	try:
		return ((r1[0]-r2[0])**2+(r1[1]-r2[1])**2)**0.5
	except:
		return None

def find_mission(mission_list, robot):
	for i in range (len(mission_list)):
		if mission_list[i] == robot:
			return i
	return None

def remove_from_list (mission_list, robot):
	if find_mission(mission_list, robot) is None:
		return
	
	else:
		mission.pop(find_mission(mission_list, robot))
		return

def add_mission(mission_list, robot, goal_point):
	remove_from_list(mission_list, robot)
	mission_list.append([robot, goal_point])


def robot_movable (robot_state_list, robot, threshold):
	robot_state = globals()[robot].curr_point
	for i in range (len(robot_state_list)):
		if distance(globals()[robot_state_list[i]].curr_point, robot_state) < threshold:
			
			return False
	
	return True



def update_robot_status(): 
	rate = rospy.Rate(10)
	for robots in pending:
			curr_pos = rospy.wait_for_message(robots+"/amcl_pose", PoseWithCovarianceStamped)
			globals()[robots].curr_point = (curr_pos.pose.pose.position.x, curr_pos.pose.pose.position.y)
			rate.sleep()

	for robots in mission:
			curr_pos = rospy.wait_for_message(robots+"/amcl_pose", PoseWithCovarianceStamped)
			globals()[robots].curr_point = (curr_pos.pose.pose.position.x, curr_pos.pose.pose.position.y)
			rate.sleep()


def check_robot_distance():
	popped = 0
	for  i in range (len(mission)-1, -1, -1):
		for j in range(i-1, -1, -1):
			if (distance(globals()[mission[i+popped]].curr_point, globals()[mission[j+popped]].curr_point)) is None:
				break
			if (distance(globals()[mission[i+popped]].curr_point, globals()[mission[j+popped]].curr_point)) < movable_threshold:
				globals()[mission[i+popped]].force_stop = True
				globals()[mission[i+popped]].stop()
				print("stopping the robot ", mission[i+popped], ", waiting robot ", mission[j+popped], " to move away")	

				pending.append(mission.pop(i+popped))
		
				popped += 1 



def pending_robot_handler():
	popped = 0
	for i in range (len(pending)):
		print("len pending with len", len(pending))
		curr_robot = pending[i-popped]
		curr_state = globals()[curr_robot].curr_point
		#add pending robot status update here 
		if robot_movable(mission, curr_robot, movable_threshold):
			mission.append(pending.pop(i-popped))
			popped +=1
			#start moving the robot
			print("moving robot ", curr_robot)
			t = "thread" + str(i)
			globals()[t] = threading.Thread(target = globals()[curr_robot].go_to_goal)
			globals()[t].start()
	
def main_loop():
	while mission or pending:
			update_robot_status()
			check_robot_distance()
			pending_robot_handler()

	global main_loop_running
	main_loop_running = False

	return
			

if __name__ == "__main__":
	
	rospy.init_node("command_listener", anonymous = True)
	define_robots()

	tcp_thread = threading.Thread(target=tcp_connection)
	tcp_thread.start()

	robot_state_thread = threading.Thread(target = update_robot_state)
	robot_state_thread.start()

