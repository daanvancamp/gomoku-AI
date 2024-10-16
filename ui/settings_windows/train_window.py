#todo: deze window werkt nog niet

import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
from configuration.config import *
import controllers.human_vs_AI_training_controller
from model_management.modelmanager import ModelManager
import ui.main_window
import controllers

distance_from_left_side = int(config["OTHER VARIABLES"]["distance_from_left_side"])
WIDTH = int(config["OTHER VARIABLES"]["WIDTH"])
HEIGHT = int(config["OTHER VARIABLES"]["HEIGHT"])
modelmanager_instance = ModelManager()
class TrainWindow(tk.Toplevel):
	def __init__(self, master):
		super().__init__(master,width=WIDTH, height=HEIGHT)

		self.title("Training")
		self.geometry(f"{WIDTH}x{HEIGHT}")
		
		self.master: "ui.main_window.GomokuApp" = master
		
		self.button_new_training = Button(self, text="Train", command=self.start_new_training)
		self.button_new_training.grid(row=0, column=0, sticky="w", padx=10)

		self.label_info=Label(self, text="red begins always")
		self.label_info.grid(row=1, column=0, sticky="w", padx=10)

		self.label_p1 = Label(self, text="Player 1(Human)")
		self.label_p1.grid(row=2, column=1, sticky="w", padx=10)

		self.label_p2 = Label(self, text="Player 2(?)")
		self.label_p2.grid(row=2, column=2, sticky="w", padx=10)
		
		self.var_p1_type = StringVar()
		self.var_p1_type.set("Human")
		self.var_color_p1 = StringVar()
		self.var_color_p1.set("red")
		self.var_p2_type = StringVar()
		self.var_p2_type.set("AI-Model")

		self.var_allow_overrule=BooleanVar()
		self.var_allow_overrule.set(False)

		self.cb_choose_color=ttk.Combobox(self, state="readonly",values=["red","blue"],textvariable=self.var_color_p1)
		self.cb_choose_color.grid(row=3, column=1, sticky="w", padx=10)


		self.radiobutton_7 = Radiobutton(self, text="Human", variable=self.var_p2_type, value="Human")
		self.radiobutton_7.grid(row=3, column=2, sticky="w")
		self.radiobutton_8 = Radiobutton(self, text="Test Algorithm", variable=self.var_p2_type, value="Test Algorithm")
		self.radiobutton_8.grid(row=4, column=2, sticky="w")
		self.radiobutton_9 = Radiobutton(self, text="AI-Model", variable=self.var_p2_type, value="AI-Model")
		self.radiobutton_9.grid(row=5, column=2, sticky="w")

		self.checkbox_allow_overrule = Checkbutton(self, text="Allow overrule", variable=self.var_allow_overrule)
		self.checkbox_allow_overrule.grid(row=6, column=2, sticky="w")


		# #column 0
		# self.label_model=Label(self, text="AI-Model: ")
		# self.label_model.grid(row=1, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		# self.CbModelTrain1 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player1.var_model)
		# self.CbModelTrain1.grid(row=2, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		# self.label_value_number_of_training_loops_tab2_p1 =Label(self, textvariable=gomoku.player1.var_number_of_training_loops_comboboxes)
		# self.label_value_number_of_training_loops_tab2_p1.grid(row=3, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		# self.overrule_button_player_1_tab2=Checkbutton(self, text="Allow overrule", variable=gomoku.player1.var_allow_overrule)
		# self.overrule_button_player_1_tab2.grid(row=7, column=0, sticky="w",padx=distance_from_left_side)


		# self.train_opponent_label = Label(self, text="Train model against:")
		# self.train_opponent_label.grid(row=1, column=1, sticky="w")

		# self.human_training_button=Radiobutton(self, text="Human", variable=gomoku.player2.var_playerType, value="Human")
		# self.human_training_button.grid(row=2, column=1,sticky="w")
		# self.radiobutton7 = Radiobutton(self, text="Test Algorithm", variable=gomoku.player2.var_playerType, value="Test Algorithm")
		# self.radiobutton7.grid(row=3, column=1, sticky="w")
		# self.radiobutton8 = Radiobutton(self, text="AI-Model", variable=gomoku.player2.var_playerType, value="AI-Model")
		# self.radiobutton8.grid(row=4, column=1, sticky="w")

		# self.CbModelTrain2 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player2.var_model)
		# self.CbModelTrain2.grid(row=5, column=1, sticky="w")
		# self.label_value_number_of_training_loops_tab2_p2 = Label(self, textvariable=gomoku.player2.var_number_of_training_loops_comboboxes)
		# self.label_value_number_of_training_loops_tab2_p2.grid(row=6, column=1, sticky="w")
		# self.overrule_button_player_2_tab2=Checkbutton(self, text="Allow overrule", variable=gomoku.player2.var_allow_overrule)
		# self.overrule_button_player_2_tab2.grid(row=7, column=1, sticky="w")

		# self.gamerunslabel = Label(self, text="Number of games: ")
		# self.gamerunslabel.grid(row=8, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		# self.gamerunsentry2 = Entry(self, textvariable=Gamesettings.var_game_runs)
		# self.gamerunsentry2.grid(row=9, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		# self.replaybutton2 = Checkbutton(self, text="Save replays", variable=Gamesettings.var_rep)
		# self.replaybutton2.grid(row=10, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		# self.show_graphs_checkbutton=Checkbutton(self, text="Show graphs*", variable=Gamesettings.var_show_graphs)
		# self.show_graphs_checkbutton.grid(row=11, column=0, sticky="w",pady=2,padx=distance_from_left_side)

		self.train_description = Label(self, text="It is recommended to run at least 3 000 games per training session.", wraplength=WIDTH-15)
		self.train_description.grid(row=12, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

		self.info_show_graphs=Label(self, text="*Don't forget to MANUALLY close the graphs at the end of each training session if you enable it.",foreground="red",wraplength=WIDTH-15)
		self.info_show_graphs.grid(row=13, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

	def start_new_training(self):
		from time import time
		self.master.clear_canvas()

		match self.var_p2_type.get():
			case "Human":
				self.master.controller = ...
			case "Test Algorithm":
				start=time()
				self.master.controller = ...
				print("time",time()-start)

			case "AI-Model":
				self.master.controller = controllers.human_vs_AI_training_controller.Human_vs_AI_Training_Controller(self.master,"blue")
				self.master.controller.AI_player.set_allow_overrule(self.var_allow_overrule.get())
