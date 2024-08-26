from tkinter import *
from tkinter.ttk import Combobox
from model_management import modelmanager
from Game_window import FrameGameWindow

WIDTH = 540
HEIGHT = 500


distance_from_left_side=10
style_numbers = ["georgia", 10, "white", 12, 2]#font, size, color, bold, underline

modelmanager_instance = modelmanager.ModelManager()


class GomokuApp(Tk):
	def __init__(self):        
		Tk.__init__(self)
		self.title("Gomoku -- Main Menu")
		self.configure(background="#357EC7")
		self.attributes("-topmost", True)
		self.bind("<Escape>", lambda event: self.quit_program())
		self.bind("<q>", lambda event: self.quit_program())
		
		self.frames={}
		for F in (FramePlay, FrameTrain,FrameReplay,FrameGameWindow):
			page_name = F.__name__
			frame = F(parent=self, controller=self)
			self.frames[page_name] = frame
			
			# All frames are stacked on top of each other
			
		
		self.show_frame("StartPage")
	
	# Method to show a frame for the given page name
	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()




class FramePlay (Frame):#the methods of gomokuapp need to be callable from the frame
	def __init__(self, master):
		super().__init__(master,width=WIDTH,height=HEIGHT)
		self.controller=master

		self.button_1 = Button(self, text="New Game", command=self.start_new_game)
		self.button_1.grid(row=0, column=0, sticky="w", padx=distance_from_left_side)
		self.checkbox_show_dialog=Checkbutton(self, text="Show dialog before starting next game", variable=Gamesettings.var_show_dialog)
		self.checkbox_show_dialog.grid(row=0, column=1, sticky="w")

		self.player1typelabel = Label(self, text="Player 1(black)")
		self.player1typelabel.grid(row=2, column=0, sticky="w", padx=distance_from_left_side)
		self.player2typelabel = Label(self, text="Player 2(white)")
		self.player2typelabel.grid(row=2, column=1, sticky="w", padx=distance_from_left_side)

		self.radiobutton1 = Radiobutton(self, text="Human", variable=gomoku.player1.var_playerType, value="Human", command=lambda: self.set_player_type(0))
		self.radiobutton1.grid(row=3, column=0, sticky="w", padx=distance_from_left_side)
		self.radiobutton2 = Radiobutton(self, text="Test Algorithm", variable=gomoku.player1.var_playerType, value="Test Algorithm", command=lambda: self.set_player_type(0))
		self.radiobutton2.grid(row=4, column=0, sticky="w", padx=distance_from_left_side)
		self.radiobutton3 = Radiobutton(self, text="AI-Model", variable=gomoku.player1.var_playerType, value="AI-Model", command=lambda: self.set_player_type(0))
		self.radiobutton3.grid(row=5, column=0, sticky="w", padx=distance_from_left_side)

		self.radiobutton4 = Radiobutton(self, text="Human", variable=gomoku.player2.var_playerType, value="Human", command=lambda: self.set_player_type(1))
		self.radiobutton4.grid(row=3, column=1, sticky="w")
		self.radiobutton5 = Radiobutton(self, text="Test Algorithm", variable=gomoku.player2.var_playerType, value="Test Algorithm", command=lambda: self.set_player_type(1))
		self.radiobutton5.grid(row=4, column=1, sticky="w")
		self.radiobutton6 = Radiobutton(self, text="AI-Model", variable=gomoku.player2.var_playerType, value="AI-Model", command=lambda: self.set_player_type(1))
		self.radiobutton6.grid(row=5, column=1, sticky="w")

		self.CbModel1 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player1.var_model)
		self.CbModel2 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player2.var_model)

		self.CbModel1.grid(row=6, column=0, sticky="w",padx=distance_from_left_side)
		self.CbModel2.grid(row=6, column=1,sticky="w",padx=distance_from_left_side)

		self.label_value_number_of_training_loops_p1 = Label(self, textvariable=gomoku.player1.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_p1.grid(row=8, column=0, sticky="w",padx=distance_from_left_side)

		self.label_value_number_of_training_loops_p2 = Label(self, textvariable=gomoku.player2.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_p2.grid(row=8, column=1, sticky="w")


		self.overrule_button_player_1=Checkbutton(self, text="Allow overrule", variable=gomoku.player1.var_allow_overrule)
		self.overrule_button_player_1.grid(row=9, column=0, sticky="w",padx=distance_from_left_side)

		self.overrule_button_player_2=Checkbutton(self, text="Allow overrule", variable=gomoku.player2.var_allow_overrule)
		self.overrule_button_player_2.grid(row=9, column=1, sticky="w")


		self.gamerunslabel = Label(self, text="Number of games: ")
		self.gamerunslabel.grid(row=10, column=0, sticky="w",padx=distance_from_left_side)
		self.gamerunsentry = Entry(self, textvariable=Gamesettings.var_game_runs)
		self.gamerunsentry.grid(row=10, column=1, sticky="w")


		self.playerstartLabel = Label(self, text="Player to start: ")
		self.playerstartLabel.grid(row=11, column=0, sticky="w", padx=distance_from_left_side)
		self.CbStartingPlayer = Combobox(self, state="readonly", values=["Player 1", "Player 2"], textvariable=Gamesettings.var_startingPlayer)
		self.CbStartingPlayer.current(0)
		self.CbStartingPlayer.grid(row=11, column=1, sticky="w")

		#column 0
		self.logbutton = Checkbutton(self, text="Create log file", variable=Gamesettings.var_log) 
		self.logbutton.grid(row=12, column=0, sticky="w",padx=distance_from_left_side)
		self.replaybutton = Checkbutton(self, text="Save replays(1)", variable=Gamesettings.var_rep) 
		self.replaybutton.grid(row=13, column=0, sticky="w",padx=distance_from_left_side)
		self.delaybutton = Checkbutton(self, text="Use AI Delay", variable=Gamesettings.var_delay)
		self.delaybutton.grid(row=14, column=0, sticky="w",padx=distance_from_left_side)

		#column1
		self.music_button=Checkbutton(self, text="Play music", variable=Gamesettings.var_play_music)
		self.music_button.grid(row=12, column=1, sticky="w")
		self.button_show_overruling=Checkbutton(self, text="Show overruling", variable=Gamesettings.var_show_overruling)
		self.button_show_overruling.grid(row=13, column=1, sticky="w")
		self.use_recognition_button=Checkbutton(self, text="use recognition(in development)*", variable=Gamesettings.var_use_recognition)
		self.use_recognition_button.grid(row=14, column=1, sticky="w")


		self.label_recognition=Label(self, text="*only turn on when you have a physical board, a webcam and the other repository.",wraplength=WIDTH-15)
		self.label_recognition.grid(row=15, column=0, sticky="w",columnspan=2, padx=distance_from_left_side)


		self.bottomframe = Frame(self, highlightbackground="blue", highlightthickness=3, borderwidth=1)
		self.bottomframe.grid(row=16, column=0, sticky="w",columnspan=3, padx=distance_from_left_side, pady=15)

		self.start_from_file_button=Checkbutton(self.bottomframe, text="Load game situation(2)", variable=Gamesettings.var_start_from_file)
		self.start_from_file_button.grid(row=0, column=0, sticky="w")
		self.label_unvalid_file=Label(self.bottomframe, text="")
		self.label_unvalid_file.grid(row=0, column=1, sticky="e",columnspan=2)

		self.label_load_state=Label(self.bottomframe, text="Choose file board state: ")
		self.label_load_state.grid(row=1, column=0, sticky="w")
		self.load_state_entry = Entry(self.bottomframe, textvariable=Gamesettings.state_board_path, width=50)
		self.load_state_entry.grid(row=2, column=0, sticky="w",columnspan=2)
		self.button_browse_state_file = Button(self.bottomframe, text="...", command=lambda: self.browse_state_files())
		self.button_browse_state_file.grid(row=2, column=2, sticky="w")
		
		self.label_info_load_save_replay=Label(self,wraplength=WIDTH-15, text="(1)(2)The save replay function can't be used when loading a board, because that would create a wrong replay file.")
		self.label_info_load_save_replay.grid(row=17, column=0, sticky="w",columnspan=2,pady=5,padx=distance_from_left_side)

class FrameTrain(Frame):
	def __init__(self, master):
		super().__init__(master,width=WIDTH, height=HEIGHT)
		self.controller=master
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

class FrameReplay(Frame,GomokuApp):
	def __init__(self, master):
		super().__init__(master,width=WIDTH,height=HEIGHT)
		self.controller=master

		self.replaylabel = Label(self, text="Choose the replay file: ")
		self.replaylabel.grid(row=0, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.replayentry = Entry(self, textvariable=Gamesettings.replay_path, width=30)
		self.replayentry.grid(row=1, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.button_4 = Button(self, text="...", command=lambda: self.browse_files())
		self.button_4.grid(row=1, column=1, sticky="w")
		self.delaybutton2 = Checkbutton(self, text="Use AI Delay", variable=Gamesettings.var_delay)
		self.delaybutton2.grid(row=2, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.button_5 = Button(self, text="Play", command=lambda: self.start_new_replay())
		self.button_5.grid(row=3, column=0, sticky="w",pady=2,padx=distance_from_left_side)

		self.label_info_replay_file_loaded=Label(self, text="",foreground="red",wraplength=WIDTH-20,font=(style_numbers[0],style_numbers[1]))
		self.label_info_replay_file_loaded.grid(row=4, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

class FrameModels(Frame):
	def __init__(self,master):
		super().__init__(master,width=WIDTH,height=HEIGHT)
		self.controller=master
		#todo: the values aren't displayed correctly, fix this

		self.var_losses=IntVar()
		self.var_losses.set(0)
		self.var_wins=IntVar()
		self.var_wins.set(0)
		self.var_ties=IntVar()
		self.var_ties.set(0)

		self.var_relative_value_losses = StringVar()
		self.var_relative_value_losses.set("0%")

		self.var_relative_value_wins = StringVar()
		self.var_relative_value_wins.set("0%")

		self.var_relative_value_ties = StringVar()
		self.var_relative_value_ties.set("0%")

		self.var_choose_stats = StringVar()

		self.var_name_model = StringVar()

		self.var_number_of_training_loops=StringVar()
		self.var_number_of_training_loops.set("0 (against H:0,T'A':0, AI:0 )")


		self.Lb1 = Listbox(self)

		models = modelmanager_instance.get_list_models()
		i  = 0
		for model in models:
			self.Lb1.insert(i, model.split('\\')[-1])
			i+=1
		self.Lb1.grid(row=0, column=2,padx=distance_from_left_side)

		if "standaard" in models or "Standaard" in models:
			for item in models:
				if item=="standaard"or item=="Standaard":
					self.Lb1.selection_set(models.index(item))
					self.Lb1.activate(models.index(item))
					last_selected_model=item
		else:
			self.Lb1.selection_set(0)
			self.Lb1.activate(0)
			last_selected_model=models[0]

		self.frame_buttons=Frame(self)
		self.frame_buttons.grid(row=0, column=0, columnspan=2,sticky='e')

		self.button_NewModel = Button(self.frame_buttons, text="Make New Model",  command=lambda: self.create_new_model())
		self.button_NewModel.grid(row=0, column=1,sticky="n",pady=2,padx=distance_from_left_side)
		self.nameModelLabel = Label(self.frame_buttons, text="Name of model: ")
		self.nameModelLabel.grid(row=1, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.nameModelEntry = Entry(self.frame_buttons, textvariable=self.var_name_model)
		self.nameModelEntry.grid(row=1, column=1, sticky="w",pady=2,padx=distance_from_left_side)
		self.nameModelEntry.bind("<Return>",lambda event: self.create_new_model())#push enter to create a new model (easier)

		self.button_DeleteModel = Button(self.frame_buttons, text="Delete Model",  command=lambda: self.delete_model())
		self.button_DeleteModel.grid(row=0, column=0,sticky="n")

		self.label_number_of_training_loops = Label(self, text="Training loops: ")
		self.label_number_of_training_loops.grid(row=4, column=0, sticky="w",padx=(distance_from_left_side,0),pady=(30,10))
		self.label_value_number_of_training_loops_tab4 = Label(self, textvariable=self.var_number_of_training_loops)
		self.label_value_number_of_training_loops_tab4.grid(row=4, column=1, sticky="w",pady=(30,10))

		self.stats_list=["Total","Games","Training"]
		self.Cb_choose_stats= Combobox(self, state="readonly", values=self.stats_list, textvariable=self.var_choose_stats)
		self.Cb_choose_stats.current(0)
		self.Cb_choose_stats.grid(row=5, column=0, sticky="w",pady=2,padx=distance_from_left_side)


		self.label_losses=Label(self, text="Losses: ")
		self.label_losses.grid(row=6, column=0, sticky="w")
		self.label_value_losses_tab4 = Label(self, textvariable=self.var_losses)
		self.label_value_losses_tab4.grid(row=6, column=1, sticky="w")
		self.label_relative_value_losses=Label(self, textvariable=self.var_relative_value_losses)
		self.label_relative_value_losses.grid(row=6, column=2, sticky="w")

		self.label_wins=Label(self, text="Wins: ")
		self.label_wins.grid(row=7, column=0, sticky="w",padx=distance_from_left_side)
		self.label_value_wins_tab4 = Label(self, textvariable=self.var_wins)
		self.label_value_wins_tab4.grid(row=7, column=1, sticky="w")
		self.label_relative_value_wins=Label(self, textvariable=self.var_relative_value_wins)
		self.label_relative_value_wins.grid(row=7, column=2, sticky="w")

		self.label_ties=Label(self, text="Ties: ")
		self.label_ties.grid(row=8, column=0, sticky="w",padx=distance_from_left_side)
		self.label_value_ties_tab4 = Label(self, textvariable=self.var_ties)
		self.label_value_ties_tab4.grid(row=8, column=1, sticky="w")
		self.label_relative_value_ties=Label(self, textvariable=self.var_relative_value_ties)
		self.label_relative_value_ties.grid(row=8, column=2, sticky="w")

		self.frame_stats_buttons=Frame(self)
		self.frame_stats_buttons.grid(row=9, column=0, columnspan=3,pady=15)
		self.button_reset_stats=Button(self.frame_stats_buttons, text="Reset Stats", command=lambda: self.reset_all_stats())
		self.button_reset_stats.grid(row=0, column=0)
		self.button_reset_end_states=Button(self.frame_stats_buttons, text="Reset End States", command=lambda: self.reset_end_states())
		self.button_reset_end_states.grid(row=0, column=1)
