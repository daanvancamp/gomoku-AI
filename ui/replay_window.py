class ReplayWinodow(tk.Toplevel):
	def __init__(self, master):
		super().__init__(master,width=WIDTH,height=HEIGHT)

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