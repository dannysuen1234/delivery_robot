#!/usr/bin/env python3
import tkinter 
import tkinter.messagebox
import customtkinter
import rospkg
import os
import threading
import webbrowser

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")  

rospack = rospkg.RosPack()

#define all package variables here
gazebo_package = "magni_gazebo"
navigation_package = "magni_nav"
frontend_started = False
backend_started = False
fleet_started = False

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
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Ordering system setting",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Simulation",
                                                command=self.button_event_tasks)
        self.button_1.grid(row=1, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Website",
                                                command=self.button_website)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Robot initial location",
                                                command=self.button_event_robot)
        self.button_3.grid(row=3, column=0, pady=10, padx=20)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Table location",
                                                command=self.button_event_table)
        self.button_4.grid(row=4, column=0, pady=10, padx=20)

        self.load_tasks_page()

    def load_tasks_page(self):
	#define right part for robot initial location ===========


        #==============define task 1 buttons
        self.task_1_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Task 1", 
                                                 text_font = ("Roboto Medium", -16))

        self.task_1_label.grid(row=1, column=0, pady=20, padx=10)

        self.tasks_button_1_world = customtkinter.CTkButton(master=self.frame_right,
                                                text="Start world",
                                                command=self.single_world_button)
	
        self.tasks_button_1_world.grid(row=2, column=0, pady=20, padx=20)

        self.tasks_button_1_nav = customtkinter.CTkButton(master=self.frame_right,
                                                text="Start mapping",
                                                command=self.mapping_button)
	
        self.tasks_button_1_nav.grid(row=2, column=1, pady=20, padx=40)


        #define task 2 buttons

        self.task_2_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Task 2", 
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

        self.tasks_button_2_robot_2_x = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="robot 2 x")
        self.tasks_button_2_robot_2_x.grid(row=6, column=0, pady=20, padx=20)


        self.tasks_button_2_robot_2_y = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="robot 2 y")
        self.tasks_button_2_robot_2_y.grid(row=6, column=1, pady=20, padx=20)


        self.tasks_button_2_map = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="map name")
        self.tasks_button_2_map.grid(row=5, column=2, pady=20, padx=20)


        self.tasks_button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Start delivery Robot",
                                                command=self.delivery_robot_button)
        self.tasks_button_2.grid(row=6, column=2, pady=20, padx=20)

        self.tasks_button_3 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Exit",
                                                command=self.exit_button)
        self.tasks_button_3.grid(row=7, column=0, pady=20, padx=20)

        self.tasks_button_4 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Save map",
                                                command=self.save_map_button)
        self.tasks_button_4.grid(row=3, column=1, pady=10, padx=0)

        self.map_name = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="map name")
        self.map_name.grid(row=3, column=0, pady=10, padx=0)

        self.fleet_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Start fleet management", 
                                                 text_font = ("Roboto Medium", -16))

        self.fleet_label.grid(row=8, column=0, pady=20, padx=10)

        self.tasks_button_fleet = customtkinter.CTkButton(master=self.frame_right,
                                                text="Start",
                                                command=self.fleet_button)
        self.tasks_button_fleet.grid(row=9, column=0, pady=0, padx=20)

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
                                                command=self.update_button_event)

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
                                                command=self.update_button_event)

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
           robot_1_x = self.tasks_button_2_robot_1_x.get()
           robot_1_y = self.tasks_button_2_robot_1_y.get()
           robot_2_x = self.tasks_button_2_robot_2_x.get()
           robot_2_y = self.tasks_button_2_robot_2_y.get()
           navigation_map = self.tasks_button_2_map.get()
           if robot_1_x == "": robot_1_x = "-8.0"
           if robot_1_y == "": robot_1_y = "-7.0"
           if robot_2_x =="": robot_2_x = "-8.0"
           if robot_2_y == "": robot_2_y = "-8.0"
           if navigation_map == "": navigation_map = "w311_virtual_world"
           map_path = rospack.get_path(navigation_package)
           map_full_path = map_path+"/maps/" + navigation_map +".yaml"
           
           command = "roslaunch magni_gazebo multi_magni_nav.launch robot_1_x:=" + str(robot_1_x) +" robot_1_y:=" + str(robot_1_y) + " robot_2_x:=" + str(robot_2_x) + " robot_2_y:=" + str(robot_2_y) + " map_file:=" + map_full_path
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
                                                command=self.front_end_button)

                self.front_end_button.grid(row=1, column=0, pady=10, padx=20)

                self.back_end_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Back end",
                                                command=self.back_end_button)

                self.back_end_button.grid(row=1, column=1, pady=0, padx=10)


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

    def single_world_button(self):
        path = rospack.get_path(navigation_package)
        mapping_world_thread = threading.Thread(target = os.system, args = [path + "/fleet/start_single_robot.bash"])
        mapping_world_thread.start()
       
    def mapping_button(self):
        path = rospack.get_path(navigation_package)
        mapping_world_thread = threading.Thread(target = os.system, args = [path + "/fleet/start_mapping.bash"])
        mapping_world_thread.start()

    def exit_button(self):
        global fleet_started
        fleet_started = False
        cmd_1 = "pkill -f ros"
        cmd_2 = "pkill -f rviz"
        cmd_3 = "pkill -f fleet"
        cmd_4 = "pkill -f OrderSystem/frontend"
        x = threading.Thread(target = os.system, args=[cmd_1])
        x.start()
        y = threading.Thread(target = os.system, args=[cmd_2])
        y.start()
        z = threading.Thread(target = os.system, args=[cmd_3])
        z.start()
        o = threading.Thread(target = os.system, args=[cmd_4])
        o.start()
    def front_end_button(self):
        global frontend_started
        if frontend_started == False:
            frontend_started = True
            map_path = rospack.get_path(navigation_package)
            whole_path = map_path + "/fleet/" + "start_front_end.bash"
            front_end_thread = threading.Thread(target = os.system, args = [whole_path])
            front_end_thread.start() 

    def back_end_button(self):
        global backend_started
        if backend_started == False:
            backend_started = True
            map_path = rospack.get_path(navigation_package)
            whole_path = map_path + "/fleet/" + "start_back_end.bash"
            back_end_thread = threading.Thread(target = os.system, args = [whole_path])
            back_end_thread.start() 

    def start_ordering_button(self):
        table_no = self.website_table_number.get()
        webbrowser.open('http://127.0.0.1:3000/scanTable?table=' + table_no)

    def save_map_button(self):
        map_name = self.map_name.get()
        map_path = rospack.get_path(navigation_package)
        whole_path = map_path + "/maps/" + map_name
        try:
            command = 'rosrun map_server map_saver -f ' + whole_path
            os.system(command)
            tkinter.messagebox.showinfo("Map saved!")
            
        except:
            tkinter.messagebox.showinfo("Failed! Please try again.")
        print(command)
    
    def fleet_button(self):
        global fleet_started
        if fleet_started == False:
            fleet_started = True
            command = "rosrun magni_nav " +"fleet_v2.py"
            fleet_thread = threading.Thread(target = os.system, args = [command])
            fleet_thread.start()

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
                                                command=self.update_button_event)

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
                                                command=self.update_button_event)

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

if __name__ == "__main__":
    app = App()
    app.mainloop()