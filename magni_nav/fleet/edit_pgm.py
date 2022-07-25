from PIL import Image
from gazebo_msgs.msg import ModelStates
import rospy 

img = Image.open('/home/vtl/magni_ws/src/magni_nav/maps/w311_virtual_world.pgm')
pixels = img.load()



#img.putpixel((835, 1214), 250)

#[x1, x2, y1, y2]
#define tables
#table 1
table_set_11 = [[914, 934, 1124, 1130],[917, 931, 1131, 1137]]
table_set_12 = [[936, 950, 1124, 1130],[933, 953, 1130, 1137]]
table_set_13 = [[916, 931, 1111, 1118], [914, 935, 1118, 1124]]
table_set_14 = [[932, 954, 1111, 1117], [936, 950, 1118, 1124]]

#table 2
table_set_21 = [[998, 1020, 1124, 1129], [1002, 1016, 1130, 1136]]
table_set_22 = [[1021, 1035, 1124, 1130], [1019, 1038, 1130, 1136]]
table_set_23 = [[1001, 1017, 1110, 1117], [999, 1019, 1117, 1123]]
table_set_24 = [[1018, 1038, 1110, 1117], [1020, 1035, 1118, 1123]]

#table 3
table_set_31 = [[1084, 1104, 1123, 1129], [1087, 1101, 1130, 1135]]
table_set_32 = [[1106, 1120, 1123, 1128], [1103, 1123, 1130, 1135]]
table_set_33 = [[1087, 1101, 1110, 1115], [1084, 1104, 1117, 1122]]
table_set_34 = [[1103, 1123, 1110, 1116], [1106, 1120, 1118, 1122]]

#table 4
table_set_41 =[[914, 934, 1045, 1050], [916, 931, 1051, 1057]]
table_set_42 =[[936, 951, 1044, 1050], [932, 953, 1051, 1057]]
table_set_43 = [[915, 930, 1030, 1038], [914, 935, 1038, 1044]]
table_set_44 = [[932, 952, 1031, 1038], [936, 949, 1039, 1043]]

#table 5
table_set_51 =[[981, 1002, 1044, 1050], [984, 1000, 1051, 1056]]
table_set_52 =[[983, 999, 1031, 1036], [979, 1002, 1038, 1044]]


#table 6
table_set_61 = [[1025, 1045, 1044, 1050], [1028, 1042, 1050, 1056]]
table_set_62 = [[1047, 1062, 1044, 1049], [1045, 1064, 1050, 1055]]
table_set_63 = [[1028, 1042, 1030, 1036], [1025, 1046, 1037, 1043]]
table_set_64 = [[1043, 1064, 1029, 1036], [1047, 1061, 1037, 1043]]

#table 7
table_set_71 = [[1084, 1105, 1043, 1050], [1088, 1102, 1049, 1056]]
table_set_72 = [[1088, 1103, 1030, 1036], [1085, 1105, 1037, 1042]]

#define table original coordinate [x, y]
#desk 1
w311_desk1_1 = [-5.2, -5.5]
w311_desk1_2 = [-3.9, -5.156]
w311_desk1_3 = [-4.84, -4.53]
w311_desk1_4 = [-4.27, -4.87]

#desk 2
w311_desk2_1 = [-0.95, -5.5]
w311_desk2_2 = [0.35, -5.156]
w311_desk2_3 = [-0.59, -4.53]
w311_desk2_4 = [-0.02, -4.87]

#desk 3
w311_desk3_1 = [3.28, -5.5]
w311_desk3_2 = [4.58, -5.156]
w311_desk3_3 = [3.64, -4.53]
w311_desk3_4 = [4.21, -4.87]

#desk 4
w311_desk4_1 = [-5.2, -1.5]
w311_desk4_2 = [-3.9, -1.156]
w311_desk4_3 = [-4.84, -0.53]
w311_desk4_4 = [-4.27, -0.87]

#desk 5
w311_desk5_1 = [-1.83, -1.5]
w311_desk5_2 = [-1.47, -0.53]

#desk 6
w311_desk6_1 = [0.36, -1.5]
w311_desk6_2 = [1.66, -1.156]
w311_desk6_3 = [0.72, -0.53]
w311_desk6_4 = [1.29, -0.87]

#desk 7
w311_desk7_1 = [3.36, -1.5]
w311_desk7_2 = [3.72, -0.53]

desk_name = ['w311_desk1_1', 'w311_desk1_2', 'w311_desk1_3', 'w311_desk1_4', 'w311_desk2_1', 'w311_desk2_2', 'w311_desk2_3', 'w311_desk2_4', 'w311_desk3_1', 'w311_desk3_2', 'w311_desk3_3', 'w311_desk3_4', 'w311_desk4_1', 'w311_desk4_2', 'w311_desk4_3', 'w311_desk4_4', 'w311_desk5_1', 'w311_desk5_2', 'w311_desk6_1', 'w311_desk6_2', 'w311_desk6_3', 'w311_desk6_4', 'w311_desk7_1', 'w311_desk7_2']

desk_name_to_set_name = {'w311_desk1_1': 'table_set_11', 
'w311_desk1_2': 'table_set_12', 
'w311_desk1_3': 'table_set_13', 
'w311_desk1_4': 'table_set_14', 

'w311_desk2_1': 'table_set_21',
'w311_desk2_2': 'table_set_22', 
'w311_desk2_3': 'table_set_23', 
'w311_desk2_4': 'table_set_24', 

'w311_desk3_1': 'table_set_31',
'w311_desk3_2': 'table_set_32', 
'w311_desk3_3': 'table_set_33', 
'w311_desk3_4': 'table_set_34', 

'w311_desk4_1': 'table_set_41',
'w311_desk4_2': 'table_set_42', 
'w311_desk4_3': 'table_set_43', 
'w311_desk4_4': 'table_set_44', 

'w311_desk5_1': 'table_set_51',
'w311_desk5_2': 'table_set_52', 

'w311_desk6_1': 'table_set_61',
'w311_desk6_2': 'table_set_62', 
'w311_desk6_3': 'table_set_63', 
'w311_desk6_4': 'table_set_64',

'w311_desk7_1': 'table_set_71',
'w311_desk7_2': 'table_set_72'
}



def curr_model_state():
	rospy.init_node('control_panel', anonymous = True)
	model_dict = {}
	data = rospy.wait_for_message("/gazebo/model_states", ModelStates)
	model_name = data.name
	model_pose = data.pose
	for i in range (len(model_name)):
		if "w311" in model_name[i]:
			model_dict[model_name[i]] = [model_pose[i].position.x,model_pose[i].position.y]

	return model_dict

def get_pose_diff(origin_pose, new_pose, table_name):
	delta_x = origin_pose[0] - new_pose[0]
	delta_y = origin_pose[1] - new_pose[1]
	obstacle_set = globals()[desk_name_to_set_name[table_name]]
	return delta_x, delta_y, obstacle_set

def update_obstacle(delta_x, delta_y, obstacle_set):
	
	delta_x_pixel = int(delta_x*20)
	delta_y_pixel = -int(delta_y*20)

	for i in range (obstacle_set[0][0], obstacle_set[0][1]):
		for j in range (obstacle_set[0][2], obstacle_set[0][3]):	
			pixel_color = pixels[i, j]
			if [i, j] not in occupied_position:
				img.putpixel((i, j), 250)

			if pixel_color <100:
				img.putpixel((i+delta_x_pixel, j+delta_y_pixel), 0)
				occupied_position.append([i+delta_x_pixel, j+delta_y_pixel])

		
	for i in range (obstacle_set[1][0], obstacle_set[1][1]):
		for j in range (obstacle_set[1][2], obstacle_set[1][3]):
			pixel_color = pixels[i, j]
			if [i, j] not in occupied_position:
				img.putpixel((i, j), 250)

			if pixel_color <100:
				img.putpixel((i+delta_x_pixel, j+delta_y_pixel), 0)
				occupied_position.append([i+delta_x_pixel, j+delta_y_pixel])
occupied_position = []
def auto_update_map(map_name):
	global img
	global pixels
	global occupied_position
	img = Image.open('/home/vtl/magni_ws/src/magni_nav/maps/w311_virtual_world.pgm')
	pixels = img.load()
	occupied_position = []
	for item in desk_name:
		model_state = curr_model_state()
		x, y, z = get_pose_diff(model_state[item], globals()[item], item)
		update_obstacle(x, y, z)
	img.save("/home/vtl/magni_ws/src/magni_nav/maps/" + map_name + ".pgm")
	yaml_data = "image: " +  "/home/vtl/magni_ws/src/magni_nav/maps/" + map_name +".pgm\nresolution: 0.050000\norigin: [-51.224998, -51.224998, 0.000000]\nnegate: 0\noccupied_thresh: 0.65\nfree_thresh: 0.196"
	yaml_file = open("/home/vtl/magni_ws/src/magni_nav/maps/" +map_name + ".yaml", 'w' )
	yaml_file.write(yaml_data)
	yaml_file.close()
	print(yaml_file)
	print("saved")

