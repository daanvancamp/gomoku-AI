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

	def start_new_physical_game(self):
		#p1=Human, p2=AI
		self.master.controller = controllers.human_vs_AI_recognition_controller.Human_vs_AI_RecognitionController(self.master,self.var_color_p1.get(),self.var_p2_model.get(),self.var_allow_overrule.get())