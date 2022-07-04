#!/usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import threading
import multiprocessing
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped

main_loop_running = False
mission = []
pending = []
movable_threshold = 1.5

class robot:
	def __init__(self, name, goal_point):
		self.name = name
		self.goal_point = goal_point
		self.curr_point = tuple()
		self.force_stop = False
		self.client = client = actionlib.SimpleActionClient(self.name+'/move_base',MoveBaseAction)

	def go_to_goal(self):	
		self.client.wait_for_server()
		self.goal = MoveBaseGoal()
		self.goal.target_pose.header.frame_id = "map"
		self.goal.target_pose.header.stamp = rospy.Time.now()
		self.goal.target_pose.pose.position.x = self.goal_point[0]
		self.goal.target_pose.pose.position.y = self.goal_point[1]
		self.goal.target_pose.pose.orientation.w = 1.0

		self.client.send_goal(self.goal)
		print("start waiting result")
		wait = self.client.wait_for_result()
		if not self.force_stop:
			remove_from_list(mission, self.name)
			print(mission, pending)
		else:
			self.force_stop = False

	def stop(self):
		self.client.cancel_all_goals()

	def set_goal_point (goal_point):
		self.goal_point = goal_point

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
	for robots in pending:
			curr_pos = rospy.wait_for_message(robots+"/amcl_pose", PoseWithCovarianceStamped)
			globals()[robots].curr_point = (curr_pos.pose.pose.position.x, curr_pos.pose.pose.position.y)

	for robots in mission:
			curr_pos = rospy.wait_for_message(robots+"/amcl_pose", PoseWithCovarianceStamped)
			globals()[robots].curr_point = (curr_pos.pose.pose.position.x, curr_pos.pose.pose.position.y)


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
	command_listener_thread = threading.Thread(target = new_command_listener)
	command_listener_thread.start()


