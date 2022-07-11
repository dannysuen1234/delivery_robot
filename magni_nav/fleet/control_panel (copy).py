#!/usr/bin/env python3
import tkinter 
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")  


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

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
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Tasks",
                                                command=self.button_event_tasks)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Robot initial location",
                                                command=self.button_event_robot)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Table location",
                                                command=self.button_event_table)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.load_tasks_page()

    def load_tasks_page(self):
	#define right part for robot initial location ===========
        self.initial_robot_label = customtkinter.CTkLabel(master = self.frame_right,
                                                 text = "Tasks", 
                                                 text_font = ("Roboto Medium", -16))

        self.initial_robot_label.grid(row=1, column=0, pady=10, padx=10)


        self.tasks_button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Map creation",
                                                command=self.button_event_table)
	
        self.tasks_button_1.grid(row=2, column=0, pady=20, padx=20)

        self.tasks_button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Delivery Robot",
                                                command=self.button_event_table)

        self.tasks_button_2.grid(row=3, column=0, pady=20, padx=20)


        self.tasks_button_3 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Exit",
                                                command=self.button_event_table)
        self.tasks_button_3.grid(row=4, column=0, pady=20, padx=20)

    def button_event_tasks(self):

                for item in self.frame_right.winfo_children():
                      print(item)
                      item.destroy()

                #self.load_tasks_page()

    def button_event_robot(self):
                for item in self.frame_right.winfo_children():

                      item.destroy()
                print("here1")
                #===================first robot=========================== 
                self.initial_robot_label.grid(row=1, column=0, pady=10, padx=10)

 
                self.robot_1_label = customtkinter.CTkLabel(master = self.frame_right,
												text = "Robot 1 setting", text_font = 
												("Roboto Medium", -16))

                self.robot_1_label.grid(row=2, column=0, pady=10, padx=10)


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

    def button_event_table(self):
                for item in self.frame_right.winfo_children():
                      item.destroy()
                print("here2")
                #===================first table=========================== 
                self.initial_robot_label.grid(row=1, column=0, pady=10, padx=10)

 
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
    def update_button_event(self):
       robot_1_x_result = self.robot_1_x.get()
       robot_1_y_result = self.robot_1_y.get()
       robot_1_z_result = self.robot_1_z.get()


    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
