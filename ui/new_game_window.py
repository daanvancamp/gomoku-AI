class NewGameWindow (tk.Toplevel):#the methods of gomokuapp need to be callable from the frame
	def __init__(self, master):
		super().__init__(master,width=WIDTH,height=HEIGHT)

		self.title("Second Window")
		self.geometry("250x150")

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