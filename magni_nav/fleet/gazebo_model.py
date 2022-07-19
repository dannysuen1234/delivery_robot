#!/usr/bin/env python3
from gazebo_msgs.msg import ModelStates
import rospy 
import yaml
import rospkg
rospack = rospkg.RosPack()

file_path = rospack.get_path("magni_nav")
file_name="/fleet/yaml/testing2.yaml"
full_path = file_path + file_name

model_dict = {}


def sub():
	rospy.init_node('subs', anonymous = True)

	data = rospy.wait_for_message("/gazebo/model_states", ModelStates)
	model_name = data.name
	model_pose = data.pose

	for i in range (len(model_name)):
		if "w311" in model_name[i]:
			model_dict[model_name[i]] = [model_pose[i].position.x,model_pose[i].position.y, model_pose[i].position.z]
	print(model_dict["w311_desk1_3"])

if __name__ == '__main__':

	sub()

	
	with open(full_path, 'w') as file:
    		documents = yaml.dump(model_dict, file)

