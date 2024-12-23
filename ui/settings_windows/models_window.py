from tkinter import *
from tkinter import ttk
from model_management.modelmanager import ModelManager
from configuration.config import config
from ui.settings_windows import window


WIDTH = int(config["UI"]["width"])
HEIGHT = int(config["UI"]["height"])
modelmanager_instance = ModelManager()

class ModelsWindow(window.BaseWindow):
	def __init__(self,master):
		super().__init__(master,WIDTH,HEIGHT,"Models")

		self.master.after(0, self.refresh_stats)

		self.var_losses = IntVar()
		self.var_losses.set(0)
		self.var_wins = IntVar()
		self.var_wins.set(0)
		self.var_ties = IntVar()
		self.var_ties.set(0)

		self.var_relative_value_losses = StringVar()
		self.var_relative_value_losses.set("0%")

		self.var_relative_value_wins = StringVar()
		self.var_relative_value_wins.set("0%")

		self.var_relative_value_ties = StringVar()
		self.var_relative_value_ties.set("0%")

		self.var_choose_stats = StringVar()

		self.var_name_model = StringVar()

		self.var_number_of_training_loops = StringVar()
		self.var_number_of_training_loops.set("0 (against H:0,T'A':0, AI:0 )")


		self.Lb1 = Listbox(self)

		models = modelmanager_instance.get_list_models()
		i  = 0
		for model in models:
			self.Lb1.insert(i, model.split('\\')[-1])
			i+=1
		self.Lb1.grid(row=0, column=2,padx=10)

		standard_item = [item for item in models if item.lower() == "standaard"]
		index = models.index(standard_item[0]) if standard_item else 0

		self.Lb1.selection_set(index)
		self.Lb1.activate(index)
		self.last_selected_model = models[index]

		self.frame_buttons = Frame(self)
		self.frame_buttons.grid(row=0, column=0, columnspan=2,sticky='e')

		self.button_NewModel = Button(self.frame_buttons, text="Make New Model",  command=lambda: self.create_new_model(self.var_name_model.get()))
		self.button_NewModel.grid(row=0, column=1,sticky="n",pady=2,padx=10)
		self.nameModelLabel = Label(self.frame_buttons, text="Name of model: ")
		self.nameModelLabel.grid(row=1, column=0, sticky="w",pady=2,padx=10)
		self.nameModelEntry = Entry(self.frame_buttons, textvariable=self.var_name_model)
		self.nameModelEntry.grid(row=1, column=1, sticky="w",pady=2,padx=10)
		self.nameModelEntry.bind("<Return>",lambda event: self.create_new_model(self.var_name_model.get()))#push enter to create a new model (easier)

		self.button_DeleteModel = Button(self.frame_buttons, text="Delete Model",  command=lambda: self.delete_model(self.Lb1.get(self.Lb1.curselection()[0])))
		self.button_DeleteModel.grid(row=0, column=0,sticky="n")

		self.label_number_of_training_loops = Label(self, text="Training loops: ")
		self.label_number_of_training_loops.grid(row=4, column=0, sticky="w",padx=(10,0),pady=(30,10))
		self.label_value_number_of_training_loops_tab4 = Label(self, textvariable=self.var_number_of_training_loops)
		self.label_value_number_of_training_loops_tab4.grid(row=4, column=1, sticky="w",pady=(30,10))

		self.stats_list = ["Total","Games","Training"]
		self.Cb_choose_stats = ttk.Combobox(self, state="readonly", values=self.stats_list, textvariable=self.var_choose_stats)
		self.Cb_choose_stats.current(0)
		self.Cb_choose_stats.grid(row=5, column=0, sticky="w",pady=2,padx=10)


		self.label_losses = Label(self, text="Losses: ")
		self.label_losses.grid(row=6, column=0, sticky="w")
		self.label_value_losses_tab4 = Label(self, textvariable=self.var_losses)
		self.label_value_losses_tab4.grid(row=6, column=1, sticky="w")
		self.label_relative_value_losses = Label(self, textvariable=self.var_relative_value_losses)
		self.label_relative_value_losses.grid(row=6, column=2, sticky="w")

		self.label_wins = Label(self, text="Wins: ")
		self.label_wins.grid(row=7, column=0, sticky="w",padx=10)
		self.label_value_wins_tab4 = Label(self, textvariable=self.var_wins)
		self.label_value_wins_tab4.grid(row=7, column=1, sticky="w")
		self.label_relative_value_wins = Label(self, textvariable=self.var_relative_value_wins)
		self.label_relative_value_wins.grid(row=7, column=2, sticky="w")

		self.label_ties = Label(self, text="Ties: ")
		self.label_ties.grid(row=8, column=0, sticky="w",padx=10)
		self.label_value_ties_tab4 = Label(self, textvariable=self.var_ties)
		self.label_value_ties_tab4.grid(row=8, column=1, sticky="w")
		self.label_relative_value_ties = Label(self, textvariable=self.var_relative_value_ties)
		self.label_relative_value_ties.grid(row=8, column=2, sticky="w")

	def refresh_stats(self):
		if not self.Lb1.winfo_exists(): return
		try:
			self.last_selected_model = self.Lb1.get(self.Lb1.curselection()[0])
		except IndexError:
			pass

		AI_model = modelmanager_instance.get_model(self.last_selected_model)
		stats_category = self.get_stats_category(self.Cb_choose_stats.get())

		losses = AI_model.get_number_of_losses(stats_category)
		wins = AI_model.get_number_of_wins(stats_category)
		ties = AI_model.get_number_of_ties(stats_category)
		
		if losses is None or wins is None or ties is None: # a model can be deleted while the program is running
			return

		self.var_losses.set(losses)
		self.var_wins.set(wins)
		self.var_ties.set(ties)

		if sum((losses,wins,ties))>0:
			self.var_relative_value_losses.set(str(round(losses/(losses+wins+ties)*100,1))+"%")
			self.var_relative_value_wins.set(str(round(wins/(losses+wins+ties)*100,1))+"%")
			self.var_relative_value_ties.set(str(round(ties/(losses+wins+ties)*100,1))+"%")
		else:
			self.var_relative_value_losses.set("N/A")
			self.var_relative_value_wins.set("N/A")
			self.var_relative_value_ties.set("N/A")

		self.var_number_of_training_loops.set(str(AI_model.get_number_of_training_loops("training loops")))

		self.master.after(100,self.refresh_stats)
		
	def get_stats_category(self,stats_category):
		match stats_category: #the names are abbreviated to improve the user experience, so they need to be converted
			case "Total":
				stats_category = "total end stats"
			case "Games":
				stats_category = "games end stats"
			case "Training":
				stats_category = "training loops end stats"
		return stats_category

	def create_new_model(self, modelname):
		modelmanager_instance.create_new_model(modelname)
		self.refresh_models()

	def delete_model(self, modelname):
		modelmanager_instance.delete_model(modelname)
		self.refresh_models()

	def refresh_models(self):
		self.Lb1.delete(0,END)
		i = 0
		models = modelmanager_instance.get_list_models()
		for model in models:
			self.Lb1.insert(i, model)
			i+=1
		
