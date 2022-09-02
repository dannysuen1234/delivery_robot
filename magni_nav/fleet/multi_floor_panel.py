#!/usr/bin/env python3
import multi_floor_nav
import tkinter 
import tkinter.messagebox
import customtkinter
import rospkg
import os
import threading
import webbrowser
import socket
import yaml
from gazebo_msgs.msg import ModelStates
import rospy  
import edit_pgm 
import valid_name
customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")  

rospack = rospkg.RosPack()

#variables for button condition
button_condition = {'task_1_world_started' : False,
'task_1_mapping_started' : False,
'task_2_delivery_robot_started' : False,
'frontend_started': False,
'backend_started' : False,
'fleet_started' : False}

frontend_started = False
backend_started = False
fleet_started = False

#define all package variables here
gazebo_package = "magni_gazebo"
navigation_package = "magni_nav"

HOST = "0.0.0.0"
PORT = 9998

class App(customtkinter.CTk):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Ordering system control panel")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")


        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # em'task_1_world_started'pty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Ordering system setting",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Multi floor simulation",
                                                command=self.button_event_tasks)
        self.button_1.grid(row=1, column=0, pady=10, padx=20)


        self.load_tasks_page()

    def load_tasks_page(self):
	#define right part for robot initial location ===========


        #==============define task 1 buttons
  
        #define task 2 buttons

        self.task_2_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Start simulation", 
                                                 text_font = ("Roboto Medium", -16))

        self.task_2_label.grid(row=4, column=0, pady=20, padx=10)

        self.tasks_button_2_robot_1_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="robot 1 x")
        self.tasks_button_2_robot_1_x.grid(row=5, column=0, pady=20, padx=20)

        self.tasks_button_2_robot_1_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="robot 1 y")
        self.tasks_button_2_robot_1_y.grid(row=5, column=1, pady=20, padx=20)




        self.tasks_button_2_map = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="config/map name")
        self.tasks_button_2_map.grid(row=5, column=2, pady=20, padx=20)


        self.tasks_button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Start delivery Robot",
                                                command=self.delivery_robot_button)
        self.tasks_button_2.grid(row=6, column=0, pady=20, padx=20)

        self.tasks_button_3 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Exit",
                                                command=self.exit_button)
        self.tasks_button_3.grid(row=10, column=0, pady=20, padx=20)

        self.task_3_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Navigation", 
                                                 text_font = ("Roboto Medium", -16))

        self.task_3_label.grid(row=7, column=0, pady=10, padx=10)

       
        self.goal_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="goal x")
        self.goal_x.grid(row=8, column=0, pady=20, padx=20)

        self.goal_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="goal y")
        self.goal_y.grid(row=8, column=1, pady=20, padx=20)

        self.floor = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="floor")
        self.floor.grid(row=8, column=2, pady=20, padx=20)


        self.go_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Go",
                                                command=self.go_button)
        self.go_button.grid(row=9, column=0, pady=20, padx=20)

   

    def go_button(self):
       x = float(self.goal_x.get())
       y = float(self.goal_y.get())
       floor_no = float(self.floor.get())
       multi_floor_nav.go_to_goal([x, y], floor_no)

    def button_event_tasks(self):

                for item in self.frame_right.winfo_children():
                      item.destroy()

                self.load_tasks_page()

    def button_event_robot(self):
                for item in self.frame_right.winfo_children():

                          item.destroy()
                #===================first robot=========================== 
                self.initial_robot_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Robot 1 setting", 
                                                 text_font = ("Roboto Medium", -16))

                self.initial_robot_label.grid(row=1, column=0, pady=10, padx=10)


                self.robot_button_4 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Update robot 1",
                                                command=self.update_robot_1_event)

                self.robot_button_4.grid(row=4, column=2, pady=20, padx=20)

                self.robot_1_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial x")
                self.robot_1_x .grid(row=3, column=0, pady=20, padx=20)

                self.robot_1_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial y")
                self.robot_1_y .grid(row=3, column=1, pady=20, padx=20)

                self.robot_1_z = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial z")
                self.robot_1_z .grid(row=3, column=2, pady=20, padx=20)
                #==========second robot===========================
                self.robot_2_label = customtkinter.CTkLabel(master = self.frame_right,
												text = "Robot 2 setting", text_font = 
												("Roboto Medium", -16))

                self.robot_2_label.grid(row=5, column=0, pady=10, padx=10)


                self.robot_button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Update robot 2",
                                                command=self.update_robot_2_event)

                self.robot_button_5.grid(row=7, column=2, pady=20, padx=20)

                self.robot_2_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial x")
                self.robot_2_x .grid(row=6, column=0, pady=20, padx=20)

                self.robot_2_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial y")
                self.robot_2_y .grid(row=6, column=1, pady=20, padx=20)

                self.robot_2_z = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial z")
                self.robot_2_z .grid(row=6, column=2, pady=20, padx=20)

    def delivery_robot_button(self):
           if button_condition["task_2_delivery_robot_started"] == True or button_condition["task_1_world_started"] == True:
               print("failed")
               return
           button_condition["task_2_delivery_robot_started"] = True
           robot_1_x = self.tasks_button_2_robot_1_x.get()
           robot_1_y = self.tasks_button_2_robot_1_y.get()

           navigation_map = self.tasks_button_2_map.get()
           if robot_1_x == "": robot_1_x = "0"
           if robot_1_y == "": robot_1_y = "0"
           map_path = rospack.get_path(navigation_package)

           if navigation_map == "":
              map_full_path = map_path+"/maps/w311_virtual_world_2.yaml"
           else:
              map_full_path = map_path+"/maps/" + navigation_map +".yaml"
          
           #desk_pose_command = load_yaml_to_command(navigation_map)
           if navigation_map == "":
                      desk_pose_command = ""
           command = "roslaunch magni_gazebo single_magni_nav.launch robot_1_x:=" + str(robot_1_x) +" robot_1_y:=" + str(robot_1_y)  + " map_file:=" + map_full_path 
           delivery_robot_thread = threading.Thread(target = os.system, args=[command])
           delivery_robot_thread.start()


    def button_website(self):
                for item in self.frame_right.winfo_children():

                          item.destroy()

                self.web_label_1 = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Start Website", 
                                                 text_font = ("Roboto Medium", -16))

                self.web_label_1.grid(row=0, column=0, pady=30, padx=20)

                


                self.front_end_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Front end",
                                                command=self.front_end_button_event)

                self.front_end_button.grid(row=1, column=0, pady=10, padx=20)

                #self.back_end_button = customtkinter.CTkButton(master=self.frame_right,
                 #                               text="Back end",
                  #                              command=self.back_end_button_event)

                #self.back_end_button.grid(row=1, column=1, pady=0, padx=10)


                self.web_ordering_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Start ordering", 
                                                 text_font = ("Roboto Medium", -16))

                self.web_ordering_label.grid(row=2, column=0, pady=20, padx=20)

                self.website_table_number = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Table number")
                self.website_table_number .grid(row=3, column=0, pady=0, padx=20)

                self.start_order_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Start ordering",
                                                command=self.start_ordering_button)

                self.start_order_button.grid(row=3, column=1, pady=0, padx=10)

                self.robot_back_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Robot back to origin position", 
                                                 text_font = ("Roboto Medium", -16))

                self.robot_back_label.grid(row=4, column=0, pady=20, padx=20)

                self.robot_1_return_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Return robot 1",
                                                command=self.robot_1_return_function)

                self.robot_1_return_button.grid(row=5, column=0, pady=0, padx=10)

                self.robot_2_return_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Return robot 2",
                                                command=self.robot_2_return_function)

                self.robot_2_return_button.grid(row=5, column=1, pady=0, padx=10)

    def robot_1_return_function (self):
      if button_condition['fleet_started'] == True:
        table_no = 1
        data_to_send = str(int(table_no) *-1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, 9999))
        s.send(data_to_send.encode())
        
        s.close()
      else:
        print("failed")

    def robot_2_return_function (self):
      if button_condition['fleet_started'] == True:
        table_no = 2
        data_to_send = str(int(table_no) *-1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, 9999))
        s.send(data_to_send.encode())
        
        s.close()
      else:
        print("failed")

    def single_world_button(self):
        if button_condition['task_2_delivery_robot_started'] == True or button_condition['task_1_world_started']:
            print("please exit task 1")
            return
        button_condition['task_1_world_started'] = True
        #path = rospack.get_path(navigation_package)
        #mapping_world_thread = threading.Thread(target = os.system, args = [path + "/fleet/start_single_robot.bash"])
        #mapping_world_thread.start()

        map_path = rospack.get_path("magni_nav")
        map_full_path = map_path+"/maps/" + "default.yaml"  
        desk_pose_command = load_yaml_to_command("default")
        command = "roslaunch magni_gazebo single_robot_world.launch map_file:=" + map_full_path #+ desk_pose_command
        mapping_world_thread = threading.Thread(target = os.system, args=[command])
        mapping_world_thread.start()

    def update_robot_1_event(self):
        x = self.robot_1_x.get()
        y = self.robot_1_y.get()
        data_to_send = "1"+" " + str(x) + " " + str(y) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(data_to_send.encode())
        s.close()
       
    def update_robot_2_event(self):
        x = self.robot_2_x.get()
        y = self.robot_2_y.get()
        data_to_send = "2"+" " + str(x) + " " + str(y) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(data_to_send.encode())
        s.close()

    def update_table_1_event(self):
        x = self.table_1_x.get()
        y = self.table_1_y.get()
        data_to_send = "3"+" " + str(x) + " " + str(y) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(data_to_send.encode())
        s.close()

    def update_table_2_event(self):
        x = self.table_2_x.get()
        y = self.table_2_y.get()
        data_to_send = "4"+" " + str(x) + " " + str(y) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(data_to_send.encode())
        s.close()

    def mapping_button(self):
        if button_condition["task_1_mapping_started"] == True or button_condition["task_1_world_started"] == False:
             print("failed")
             return
        button_condition["task_1_mapping_started"] = True
        path = rospack.get_path(navigation_package)
        mapping_world_thread = threading.Thread(target = os.system, args = [path + "/fleet/start_mapping.bash"])
        mapping_world_thread.start()

    def exit_button(self):
        global button_condition
        for item in button_condition:
            button_condition[item] = False

        cmd_1 = "pkill -f ros"
        cmd_2 = "pkill -f rviz"
        cmd_3 = "pkill -9 -f fleet"
        cmd_4 = "pkill -f /OrderSystem/"
        x = threading.Thread(target = os.system, args=[cmd_1])
        x.start()
        y = threading.Thread(target = os.system, args=[cmd_2])
        y.start()
        z = threading.Thread(target = os.system, args=[cmd_3])
        z.start()
        o = threading.Thread(target = os.system, args=[cmd_4])
        o.start()
    def front_end_button_event(self):

        if button_condition['frontend_started'] == False:

            button_condition['frontend_started'] = True
            map_path = rospack.get_path(navigation_package)
            whole_path = map_path + "/fleet/" + "start_front_end.bash"
            front_end_thread = threading.Thread(target = os.system, args = [whole_path])
            front_end_thread.start() 
            map_path = rospack.get_path(navigation_package)
            whole_path = map_path + "/fleet/" + "start_back_end.bash"
            back_end_thread = threading.Thread(target = os.system, args = [whole_path])
            back_end_thread.start() 


    #def back_end_button_event(self):
    #    global backend_started
    #    if backend_started == False:
    #        backend_started = True
    #        map_path = rospack.get_path(navigation_package)
    #        whole_path = map_path + "/fleet/" + "start_back_end.bash"
    #        back_end_thread = threading.Thread(target = os.system, args = [whole_path])
    #        back_end_thread.start() 

    def start_ordering_button(self):
        table_no = self.website_table_number.get()
        webbrowser.open('http://127.0.0.1:3000/scanTable?table=' + table_no)

    def save_map_button(self):
        if button_condition["task_1_mapping_started"] == False:
             print("failed")
             return
        map_name = self.config_name.get()
        map_path = rospack.get_path(navigation_package)
        whole_path = map_path + "/maps/" + map_name
        try:
            command = 'rosrun map_server map_saver -f ' + whole_path
            os.system(command)
            tkinter.messagebox.showinfo("Map saved!")
            
        except:
            tkinter.messagebox.showinfo("Failed! Please try again.")
        print(command)

    def save_config_button(self):
      if button_condition['task_1_world_started'] == True :
        config_name = self.config_name.get()
        path = rospack.get_path(navigation_package) + "/fleet/yaml"
        rospy.init_node('control_panel', anonymous = True)
        if valid_name.valid_name(config_name, path):
           model_dict = {}
           path = rospack.get_path(navigation_package)
           full_path = path + "/fleet/yaml/" + config_name + ".yaml"
           data = rospy.wait_for_message("/gazebo/model_states", ModelStates)
           model_name = data.name
           model_pose = data.pose
           for i in range (len(model_name)):
                if "w311" in model_name[i]:
                        model_dict[model_name[i]] = [model_pose[i].position.x,model_pose[i].position.y, model_pose[i].position.z]

           with open(full_path, 'w') as file:
                   documents = yaml.dump(model_dict, file)
        else:
            print("invalid name")
      else:
        print("failed")

    def auto_update_map_button(self):
         if button_condition['task_1_world_started'] == True:
             map_name = self.config_name.get()
             path = rospack.get_path(navigation_package) +"/maps"
             if valid_name.valid_name(map_name, path):
                edit_pgm.auto_update_map(map_name)
             else:
                print("not valid name")
         else:
             print("failed")
   
    def fleet_button(self):
        if button_condition["fleet_started"] == False and button_condition["task_2_delivery_robot_started"] ==True :
            button_condition["fleet_started"] = True
            print("started fleet management")
            command = "rosrun magni_nav " +"fleet_v2.py"
            fleet_thread = threading.Thread(target = os.system, args = [command])
            fleet_thread.start()
        else:
            print("failed")

    def button_event_table(self):
                for item in self.frame_right.winfo_children():
                      item.destroy()
                #===================first table=========================== 

 
                self.table_1_label = customtkinter.CTkLabel(master = self.frame_right,
												text = "Table 1 position", text_font = 
												("Roboto Medium", -16))

                self.table_1_label.grid(row=2, column=0, pady=10, padx=10)


                self.table_button_4 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Update Table 1",
                                                command=self.update_table_1_event)

                self.table_button_4.grid(row=4, column=2, pady=20, padx=20)

                self.table_1_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial x")
                self.table_1_x .grid(row=3, column=0, pady=20, padx=20)

                self.table_1_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial y")
                self.table_1_y .grid(row=3, column=1, pady=20, padx=20)

                self.table_1_z = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial z")
                self.table_1_z .grid(row=3, column=2, pady=20, padx=20)

                #==========second table===========================
                self.table_2_label = customtkinter.CTkLabel(master = self.frame_right,
												text = "Table 2 position", text_font = 
												("Roboto Medium", -16))

                self.table_2_label.grid(row=5, column=0, pady=10, padx=10)


                self.table_button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Update table 2",
                                                command=self.update_table_2_event)

                self.table_button_5.grid(row=7, column=2, pady=20, padx=20)

                self.table_2_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial x")
                self.table_2_x .grid(row=6, column=0, pady=20, padx=20)

                self.table_2_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial y")
                self.table_2_y .grid(row=6, column=1, pady=20, padx=20)

                self.table_2_z = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial z")
                self.table_2_z .grid(row=6, column=2, pady=20, padx=20)

                # ========= third table ==================
                self.table_3_label = customtkinter.CTkLabel(master = self.frame_right,
												text = "Table 3 position", text_font = 
												("Roboto Medium", -16))

                self.table_3_label.grid(row=8, column=0, pady=10, padx=10)


                self.table_button_6 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Update table 3",
                                                command=self.update_button_event)

                self.table_button_6.grid(row=10, column=2, pady=20, padx=20)

                self.table_3_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial x")
                self.table_3_x .grid(row=9, column=0, pady=20, padx=20)

                self.table_3_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial y")
                self.table_3_y .grid(row=9, column=1, pady=20, padx=20)

                self.table_3_z = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="initial z")
                self.table_3_z .grid(row=9, column=2, pady=20, padx=20)
   

    def update_button_event(self):
       robot_1_x_result = self.robot_1_x.get()
       robot_1_y_result = self.robot_1_y.get()
       robot_1_z_result = self.robot_1_z.get()


    def on_closing(self, event=0):
        self.destroy()

def load_yaml_to_command(config_name):
   path = rospack.get_path(navigation_package)
   full_path = path + "/fleet/yaml/" + config_name + ".yaml"
   with open(full_path) as file:

      desk_list = yaml.load(file, Loader=yaml.FullLoader)
      command =""
      for item in desk_list:
         command += " "+ item +"_pose:=" + "'-x " + str(desk_list[item][0]) + " -y " + str(desk_list[item][1]) +"'"
      return command 

if __name__ == "__main__":
    app = App()
    app.mainloop()
