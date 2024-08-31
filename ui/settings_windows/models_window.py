#todo dit window werkt nog niet
from tkinter import *
from tkinter import ttk
class ModelsWindow(Toplevel):
	def __init__(self,master):
		super().__init__(master,width=WIDTH,height=HEIGHT)

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
		self.Lb1.grid(row=0, column=2,padx=10)

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
		self.button_NewModel.grid(row=0, column=1,sticky="n",pady=2,padx=10)
		self.nameModelLabel = Label(self.frame_buttons, text="Name of model: ")
		self.nameModelLabel.grid(row=1, column=0, sticky="w",pady=2,padx=10)
		self.nameModelEntry = Entry(self.frame_buttons, textvariable=self.var_name_model)
		self.nameModelEntry.grid(row=1, column=1, sticky="w",pady=2,padx=10)
		self.nameModelEntry.bind("<Return>",lambda event: self.create_new_model())#push enter to create a new model (easier)

		self.button_DeleteModel = Button(self.frame_buttons, text="Delete Model",  command=lambda: self.delete_model())
		self.button_DeleteModel.grid(row=0, column=0,sticky="n")

		self.label_number_of_training_loops = Label(self, text="Training loops: ")
		self.label_number_of_training_loops.grid(row=4, column=0, sticky="w",padx=(10,0),pady=(30,10))
		self.label_value_number_of_training_loops_tab4 = Label(self, textvariable=self.var_number_of_training_loops)
		self.label_value_number_of_training_loops_tab4.grid(row=4, column=1, sticky="w",pady=(30,10))

		self.stats_list=["Total","Games","Training"]
		self.Cb_choose_stats= ttk.Combobox(self, state="readonly", values=self.stats_list, textvariable=self.var_choose_stats)
		self.Cb_choose_stats.current(0)
		self.Cb_choose_stats.grid(row=5, column=0, sticky="w",pady=2,padx=10)


		self.label_losses=Label(self, text="Losses: ")
		self.label_losses.grid(row=6, column=0, sticky="w")
		self.label_value_losses_tab4 = Label(self, textvariable=self.var_losses)
		self.label_value_losses_tab4.grid(row=6, column=1, sticky="w")
		self.label_relative_value_losses=Label(self, textvariable=self.var_relative_value_losses)
		self.label_relative_value_losses.grid(row=6, column=2, sticky="w")

		self.label_wins=Label(self, text="Wins: ")
		self.label_wins.grid(row=7, column=0, sticky="w",padx=10)
		self.label_value_wins_tab4 = Label(self, textvariable=self.var_wins)
		self.label_value_wins_tab4.grid(row=7, column=1, sticky="w")
		self.label_relative_value_wins=Label(self, textvariable=self.var_relative_value_wins)
		self.label_relative_value_wins.grid(row=7, column=2, sticky="w")

		self.label_ties=Label(self, text="Ties: ")
		self.label_ties.grid(row=8, column=0, sticky="w",padx=10)
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