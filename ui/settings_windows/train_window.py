#todo: deze window werkt nog niet volledig
from time import sleep
from tkinter import ttk
from tkinter import *
from configuration.config import *
from model_management.modelmanager import ModelManager
from controllers.training import human_vs_AI_training_controller,test_algorithm_vs_AI_training_controller,AI_vs_AI_training_controller
from ui.settings_windows import window

distance_from_left_side = int(config["OTHER VARIABLES"]["distance_from_left_side"])
WIDTH = int(config["OTHER VARIABLES"]["WIDTH"])
HEIGHT = int(config["OTHER VARIABLES"]["HEIGHT"])
modelmanager_instance = ModelManager()
class TrainWindow(window.BaseWindow):
	def __init__(self, master):
		super().__init__(master, WIDTH, HEIGHT, "Training")

		
		self.button_new_training = Button(self, text="Train", command=self.start_new_training)
		self.button_new_training.grid(row=0, column=0, sticky="w", padx=10)

		self.label_info=Label(self, text="red begins always")
		self.label_info.grid(row=0, column=1, sticky="w", padx=10)

		self.label_p1 = Label(self, text="Player 1(AI)")
		self.label_p1.grid(row=2, column=0, sticky="w", padx=10)

		self.label_p2 = Label(self, text="Player 2(?)")
		self.label_p2.grid(row=2, column=1, sticky="w", padx=10)
		
		self.var_p1_type = StringVar()
		self.var_p1_type.set("AI-Model")
		self.var_color_p1 = StringVar()
		self.var_color_p1.set("red") #red begins always
		self.var_p2_type = StringVar()
		self.var_p2_type.set("Human")

		self.var_allow_overrule=BooleanVar()
		self.var_allow_overrule.set(False)
		
		self.var_show_graphs= BooleanVar()
		self.var_show_graphs.set(False)

		self.var_p1_model= StringVar()
		self.var_p1_model.set("standaard+3000")
		self.var_p2_model= StringVar()
		self.var_p2_model.set("standaard+3000")
		self.var_game_runs = IntVar()
		self.var_game_runs.set(10)

		self.cb_choose_color=ttk.Combobox(self, state="readonly",values=["red","blue"],textvariable=self.var_color_p1)
		self.cb_choose_color.grid(row=3, column=0, sticky="w", padx=10)


		self.radiobutton_7 = Radiobutton(self, text="Human", variable=self.var_p2_type, value="Human")
		self.radiobutton_7.grid(row=3, column=1, sticky="w")
		self.radiobutton_8 = Radiobutton(self, text="Test Algorithm", variable=self.var_p2_type, value="Test Algorithm")
		self.radiobutton_8.grid(row=4, column=1, sticky="w")
		self.radiobutton_9 = Radiobutton(self, text="AI-Model", variable=self.var_p2_type, value="AI-Model")
		self.radiobutton_9.grid(row=5, column=1, sticky="w")

		self.checkbox_allow_overrule = Checkbutton(self, text="Allow overrule", variable=self.var_allow_overrule)
		self.checkbox_allow_overrule.grid(row=7, column=0,columnspan=2)


		# #column 0
		# self.label_model=Label(self, text="AI-Model: ")
		# self.label_model.grid(row=1, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		self.CbModelTrain1 = ttk.Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=self.var_p1_model)
		self.CbModelTrain1.grid(row=6, column=0, sticky="w",padx=distance_from_left_side,pady=1)
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

		self.CbModelTrain2 = ttk.Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=self.var_p2_model)
		self.CbModelTrain2.grid(row=6, column=1, sticky="w")
		# self.label_value_number_of_training_loops_tab2_p2 = Label(self, textvariable=gomoku.player2.var_number_of_training_loops_comboboxes)
		# self.label_value_number_of_training_loops_tab2_p2.grid(row=6, column=1, sticky="w")
		# self.overrule_button_player_2_tab2=Checkbutton(self, text="Allow overrule", variable=gomoku.player2.var_allow_overrule)
		# self.overrule_button_player_2_tab2.grid(row=7, column=1, sticky="w")

		# self.gamerunslabel = Label(self, text="Number of games: ")
		# self.gamerunslabel.grid(row=8, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.gamerunsentry2 = Entry(self, textvariable=self.var_game_runs)
		self.gamerunsentry2.grid(row=9, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		# self.replaybutton2 = Checkbutton(self, text="Save replays", variable=Gamesettings.var_rep)
		# self.replaybutton2.grid(row=10, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.show_graphs_checkbutton=Checkbutton(self, text="Show graphs*", variable=self.var_show_graphs)
		self.show_graphs_checkbutton.grid(row=11, column=0, sticky="w",pady=2,padx=distance_from_left_side)

		self.train_description = Label(self, text="It is recommended to run at least 3 000 games per training session. If you select human vs AI, then the number of games is one.", wraplength=WIDTH-15)
		self.train_description.grid(row=12, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

		self.info_show_graphs=Label(self, text="*Don't forget to MANUALLY close the graphs at the end of each training session if you enable it.",foreground="red",wraplength=WIDTH-15)
		self.info_show_graphs.grid(row=13, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

	def start_new_training(self):
		# The first move never needs to be overruled.
		#p1=AI, p2=...
		match self.var_p2_type.get():
			case "Human":
				self.master.controller = human_vs_AI_training_controller.Human_vs_AI_TrainingController(self.master,self.var_color_p1.get(),self.var_p2_model.get()) #todo finish this
				self.master.controller.AI_player.set_allow_overrule(self.var_allow_overrule.get())
				self.master.controller.show_graphs = self.var_show_graphs.get()

			case "Test Algorithm":
				print(f"run{i+1} started")
				for i in range(self.var_game_runs.get()):
					self.master.controller = test_algorithm_vs_AI_training_controller.TestAlgorithm_vs_AI_TrainingController(self.master,self.var_color_p1.get(),self.var_p2_model.get())

			case "AI-Model":
				for i in range(self.var_game_runs.get()):
					print(f"run{i+1} started")
					self.master.controller = AI_vs_AI_training_controller.AI_vs_AI_TrainingController(self.master,self.var_color_p1.get(),self.var_p1_model.get(),self.var_p2_model.get())

