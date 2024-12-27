from tkinter import *
from tkinter import ttk

from configuration.config import config
import controllers.human_vs_AI_controller
import controllers.human_vs_AI_recognition_controller
import controllers.human_vs_human_controller 
import controllers.human_vs_test_algorithm_controller
from model_management.modelmanager import ModelManager
import ui.main_window
from ui.settings_windows import window


modelmanager_instance = ModelManager()
WIDTH = int(config["UI"]["width"])
HEIGHT = int(config["UI"]["height"])

class PhysicalPlayWindow (window.BaseWindow):
	def __init__(self, master: "ui.main_window.GomokuApp"):
		super().__init__(master,WIDTH,HEIGHT,"New Physical Game")

		self.button_new_physical_game = Button(self, text="New Physical Game", command=self.start_new_physical_game)
		self.button_new_physical_game.grid(row=0, column=0, sticky="w", padx=10)

		self.label_info = Label(self, text="red begins always")
		self.label_info.grid(row=1, column=0, sticky="w", padx=10)

		self.label_p1 = Label(self, text="Player 1(Human)")
		self.label_p1.grid(row=2, column=0, sticky="w", padx=10)

		self.label_p2 = Label(self, text="Player 2(AI)")
		self.label_p2.grid(row=2, column=1, sticky="w", padx=10)
		
		self.var_color_p1 = StringVar()
		self.var_color_p1.set("red")
		self.var_p2_type = StringVar()
		self.var_p2_type.set("AI-Model")

		self.var_p2_model = StringVar()
		self.var_p2_model.set("standaard+3000")

		self.var_allow_overrule=BooleanVar()
		self.var_allow_overrule.set(True)

		self.cb_choose_color = ttk.Combobox(self, state="readonly",values=["red","blue"],textvariable=self.var_color_p1)
		self.cb_choose_color.grid(row=3, column=0, sticky="w", padx=10)

		self.checkbox_allow_overrule = Checkbutton(self, text="Allow overrule", variable=self.var_allow_overrule)
		self.checkbox_allow_overrule.grid(row=7, column=0,columnspan=2)

		self.CbModel2 = ttk.Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=self.var_p2_model)

		self.CbModel2.grid(row=6, column=1,sticky="w",padx=10)

		# self.label_value_number_of_training_loops_p1 = tk.Label(self, textvariable=gomoku.player1.var_number_of_training_loops_comboboxes)
		# self.label_value_number_of_training_loops_p1.grid(row=8, column=0, sticky="w",padx=10)

		# self.label_value_number_of_training_loops_p2 = tk.Label(self, textvariable=gomoku.player2.var_number_of_training_loops_comboboxes)
		# self.label_value_number_of_training_loops_p2.grid(row=8, column=1, sticky="w")

	def start_new_physical_game(self):
		#p1=Human, p2=AI
		self.master.controller = controllers.human_vs_AI_recognition_controller.Human_vs_AI_RecognitionController(self.master,self.var_color_p1.get(),self.var_p2_model.get())
		self.master.controller.AI_player.set_allow_overrule(self.var_allow_overrule.get())# The first move never needs to be overruled.
			





















		


		# self.overrule_button_player_1=tk.Checkbutton(self, text="Allow overrule", variable=gomoku.player1.var_allow_overrule)
		# self.overrule_button_player_1.grid(row=9, column=0, sticky="w",padx=10)

		# self.overrule_button_player_2=tk.Checkbutton(self, text="Allow overrule", variable=gomoku.player2.var_allow_overrule)
		# self.overrule_button_player_2.grid(row=9, column=1, sticky="w")


		# self.gamerunslabel = tk.Label(self, text="Number of games: ")
		# self.gamerunslabel.grid(row=10, column=0, sticky="w",padx=10)
		# self.gamerunsentry = tk.Entry(self, textvariable=Gamesettings.var_game_runs)
		# self.gamerunsentry.grid(row=10, column=1, sticky="w")


		# self.playerstartLabel = tk.Label(self, text="Player to start: ")
		# self.playerstartLabel.grid(row=11, column=0, sticky="w", padx=10)
		# self.CbStartingPlayer = tk.Combobox(self, state="readonly", values=["Player 1", "Player 2"], textvariable=Gamesettings.var_startingPlayer)
		# self.CbStartingPlayer.current(0)
		# self.CbStartingPlayer.grid(row=11, column=1, sticky="w")

		# #column 0
		# self.logbutton = tk.Checkbutton(self, text="Create log file", variable=Gamesettings.var_log) 
		# self.logbutton.grid(row=12, column=0, sticky="w",padx=10)
		# self.replaybutton = tk.Checkbutton(self, text="Save replays(1)", variable=Gamesettings.var_rep) 
		# self.replaybutton.grid(row=13, column=0, sticky="w",padx=10)
		# self.delaybutton = tk.Checkbutton(self, text="Use AI Delay", variable=Gamesettings.var_delay)
		# self.delaybutton.grid(row=14, column=0, sticky="w",padx=10)

		# #column1
		# self.music_button=tk.Checkbutton(self, text="Play music", variable=Gamesettings.var_play_music)
		# self.music_button.grid(row=12, column=1, sticky="w")
		# self.button_show_overruling=tk.Checkbutton(self, text="Show overruling", variable=Gamesettings.var_show_overruling)
		# self.button_show_overruling.grid(row=13, column=1, sticky="w")
		# self.use_recognition_button=tk.Checkbutton(self, text="use recognition(in development)*", variable=Gamesettings.var_use_recognition)
		# self.use_recognition_button.grid(row=14, column=1, sticky="w")


		# self.label_recognition=tk.Label(self, text="*only turn on when you have a physical board, a webcam and the other repository.",wraplength=WIDTH-15)
		# self.label_recognition.grid(row=15, column=0, sticky="w",columnspan=2, padx=10)


		# self.bottomframe = tk.Frame(self, highlightbackground="blue", highlightthickness=3, borderwidth=1)
		# self.bottomframe.grid(row=16, column=0, sticky="w",columnspan=3, padx=10, pady=15)

		# self.start_from_file_button=tk.Checkbutton(self.bottomframe, text="Load game situation(2)", variable=Gamesettings.var_start_from_file)
		# self.start_from_file_button.grid(row=0, column=0, sticky="w")
		# self.label_unvalid_file=tk.Label(self.bottomframe, text="")
		# self.label_unvalid_file.grid(row=0, column=1, sticky="e",columnspan=2)

		# self.label_load_state=tk.Label(self.bottomframe, text="Choose file board state: ")
		# self.label_load_state.grid(row=1, column=0, sticky="w")
		# self.load_state_entry = tk.Entry(self.bottomframe, textvariable=Gamesettings.state_board_path, width=50)
		# self.load_state_entry.grid(row=2, column=0, sticky="w",columnspan=2)
		# self.button_browse_state_file = tk.Button(self.bottomframe, text="...", command=lambda: self.browse_state_files())
		# self.button_browse_state_file.grid(row=2, column=2, sticky="w")
		
		# self.label_info_load_save_replay=tk.Label(self,wraplength=WIDTH-15, text="(1)(2)The save replay function can't be used when loading a board, because that would create a wrong replay file.")
		# self.label_info_load_save_replay.grid(row=17, column=0, sticky="w",columnspan=2,pady=5,padx=10)