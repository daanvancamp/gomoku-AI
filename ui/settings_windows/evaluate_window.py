import tkinter as tk
from tkinter import ttk

from ui.settings_windows import window
from model_management.modelmanager import ModelManager
from controllers.evaluation import AI_vs_AI_evaluation_controller, test_algorithm_vs_AI_evaluation_controller

modelmanager_instance = ModelManager()
class EvaluateWindow(window.BaseWindow): # player 1 is AI, player 2 is AI/Test Algorithm
	def __init__(self, master):
		super().__init__(master,350,200,"Evaluate Window")
		self.var_color_p1 = tk.StringVar()
		self.var_color_p1.set("red")
		self.var_p2_type = tk.StringVar()
		self.var_p2_type.set("AI-Model")

		self.var_p1_model = tk.StringVar()
		self.var_p1_model.set("standaard+3000")
		self.var_p2_model = tk.StringVar()
		self.var_p2_model.set("standaard+3000")

		self.var_allow_overrule = tk.BooleanVar()
		self.var_allow_overrule.set(True)

		self.button_new_evaluation = tk.Button(self, text="New Game", command=self.start_new_evaluation)
		self.button_new_evaluation.grid(row=0, column=0, sticky="w", padx=10)

		self.label_p1 = tk.Label(self, text="Player 1 (AI)")
		self.label_p1.grid(row=1, column=0, sticky="w", padx=10)

		self.label_p2 = tk.Label(self, text="Player 2 (AI/Test Algorithm)")
		self.label_p2.grid(row=1, column=1, sticky="w", padx=10)

		self.cb_choose_color = ttk.Combobox(self, state="readonly",values=["red","blue"],textvariable=self.var_color_p1)
		self.cb_choose_color.grid(row=2, column=0, sticky="w", padx=10)

		self.Cb_p2 = ttk.Combobox(self, state="readonly", values=["AI-Model","Test Algorithm"],textvariable=self.var_p2_type)
		self.Cb_p2.grid(row=2, column=1,sticky="w",padx=10)

		self.CbModel1 = ttk.Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=self.var_p1_model)
		self.CbModel1.grid(row=3, column=0,sticky="w",padx=10)
		self.CbModel2 = ttk.Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=self.var_p2_model)
		self.CbModel2.grid(row=3, column=1,sticky="w",padx=10)

		self.checkbox_allow_overrule = tk.Checkbutton(self, text="Allow overrule", variable=self.var_allow_overrule)
		self.checkbox_allow_overrule.grid(row=7, column=0,columnspan=2)

	def start_new_evaluation(self):
		#p1=AI, p2=AI/Test Algorithm
		match self.var_p2_type.get():
			case "AI-Model":
				self.master.controller = AI_vs_AI_evaluation_controller.AI_vs_AI_EvaluationController(self.master,self.var_p1_model.get(),self.var_p2_model.get(),self.var_allow_overrule.get())
			case "Test Algorithm":
				self.master.controller = test_algorithm_vs_AI_evaluation_controller.TestAlgorithm_vs_AI_EvaluationController(self.master,self.var_color_p1.get(),self.var_p1_model.get(),self.var_allow_overrule.get())
	
	def on_AI_p_type_selection(self):
		self.cb_choose_color.set("red") # selecting blue doesn't make sense, because you have 2 equal players, AI vs AI, this would make the code in the controller(AI_vs_AI_TrainingController) more difficult

	def on_color_selection(self):
		if self.var_p2_type.get() == "AI-Model" and self.var_color_p1.get() == "blue":
			self.cb_choose_color.set("red") # see previous comment