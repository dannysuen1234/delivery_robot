#!/usr/bin/env python

import socket
import rospy
from std_msgs.msg import String
import threading

HOST = '0.0.0.0'
PORT = 7000

available_robots = ["1", "2"]
robot_in_mission = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)


def new_command(table_number):
	if table_number == 1:
		x = 2
		y = -3
	pub = rospy.Publisher("robot_command", String, queue_size= 10)
	rospy.init_node("robot_commander", anonymous = True)
	command = "magni_1 " + " " + str(x)  + " " + str(y)
	print(command)
	pub.publish(command)

while True:
	conn, addr =s.accept()
	indata = conn.recv(1024)
	table_number = int(indata.decode())
	print(table_number)
	conn.close()
	new_command(table_number)
