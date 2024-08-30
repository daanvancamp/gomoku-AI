#todo dit window werkt nog niet

import tkinter as tk
from tkinter import *
from tkinter.ttk import *
class TrainWindow(tk.Toplevel):
	def __init__(self, master):
		super().__init__(master,width=WIDTH, height=HEIGHT)
		#row 0
		self.button_2 = Button(self, text="Train", command=lambda: self.start_new_training())
		self.button_2.grid(row=0, column=1, sticky="e")

		#column 0
		self.label_model=Label(self, text="AI-Model: ")
		self.label_model.grid(row=1, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		self.CbModelTrain1 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player1.var_model)
		self.CbModelTrain1.grid(row=2, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		self.label_value_number_of_training_loops_tab2_p1 =Label(self, textvariable=gomoku.player1.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_tab2_p1.grid(row=3, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		self.overrule_button_player_1_tab2=Checkbutton(self, text="Allow overrule", variable=gomoku.player1.var_allow_overrule)
		self.overrule_button_player_1_tab2.grid(row=7, column=0, sticky="w",padx=distance_from_left_side)


		self.train_opponent_label = Label(self, text="Train model against:")
		self.train_opponent_label.grid(row=1, column=1, sticky="w")

		self.human_training_button=Radiobutton(self, text="Human", variable=gomoku.player2.var_playerType, value="Human")
		self.human_training_button.grid(row=2, column=1,sticky="w")
		self.radiobutton7 = Radiobutton(self, text="Test Algorithm", variable=gomoku.player2.var_playerType, value="Test Algorithm")
		self.radiobutton7.grid(row=3, column=1, sticky="w")
		self.radiobutton8 = Radiobutton(self, text="AI-Model", variable=gomoku.player2.var_playerType, value="AI-Model")
		self.radiobutton8.grid(row=4, column=1, sticky="w")

		self.CbModelTrain2 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player2.var_model)
		self.CbModelTrain2.grid(row=5, column=1, sticky="w")
		self.label_value_number_of_training_loops_tab2_p2 = Label(self, textvariable=gomoku.player2.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_tab2_p2.grid(row=6, column=1, sticky="w")
		self.overrule_button_player_2_tab2=Checkbutton(self, text="Allow overrule", variable=gomoku.player2.var_allow_overrule)
		self.overrule_button_player_2_tab2.grid(row=7, column=1, sticky="w")

		self.gamerunslabel = Label(self, text="Number of games: ")
		self.gamerunslabel.grid(row=8, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.gamerunsentry2 = Entry(self, textvariable=Gamesettings.var_game_runs)
		self.gamerunsentry2.grid(row=9, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.replaybutton2 = Checkbutton(self, text="Save replays", variable=Gamesettings.var_rep)
		self.replaybutton2.grid(row=10, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.show_graphs_checkbutton=Checkbutton(self, text="Show graphs*", variable=Gamesettings.var_show_graphs)
		self.show_graphs_checkbutton.grid(row=11, column=0, sticky="w",pady=2,padx=distance_from_left_side)

		self.train_description = Label(self, text="It is recommended to run at least 3 000 games per training session.", font=(style_numbers[0], style_numbers[1]), wraplength=WIDTH-15)
		self.train_description.grid(row=12, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

		self.info_show_graphs=Label(self, text="*Don't forget to MANUALLY close the graphs at the end of each training session if you enable it.",foreground="red",wraplength=WIDTH-15)
		self.info_show_graphs.grid(row=13, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)