from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os

from configuration.config import config
from controllers import human_vs_AI_controller, human_vs_human_controller, human_vs_test_algorithm_controller
from model_management.modelmanager import ModelManager
import ui.main_window
from ui.settings_windows import window

modelmanager_instance = ModelManager()
WIDTH = int(config["UI"]["width"])
HEIGHT = int(config["UI"]["height"])

class NewGameWindow (window.BaseWindow):
	def __init__(self, master: "ui.main_window.GomokuApp"):
		super().__init__(master,WIDTH,HEIGHT,"New Game")

		self.button_new_game = Button(self, text="New Game", command=self.start_new_game)
		self.button_new_game.grid(row=0, column=0, sticky="w", padx=10)

		self.label_info = Label(self, text="red begins always")
		self.label_info.grid(row=1, column=0, sticky="w", padx=10)

		self.label_p1 = Label(self, text="Player 1 (Human)")
		self.label_p1.grid(row=2, column=0, sticky="w", padx=10)

		self.label_p2 = Label(self, text="Player 2 (?)")
		self.label_p2.grid(row=2, column=1, sticky="w", padx=10)
		
		self.var_color_p1 = StringVar()
		self.var_color_p1.set("red")
		self.var_p2_type = StringVar()
		self.var_p2_type.set("AI-Model")

		self.var_p2_model = StringVar()
		self.var_p2_model.set("standaard+3000")

		self.var_allow_overrule = BooleanVar()
		self.var_allow_overrule.set(True)

		self.var_state_board_path = StringVar()
		self.var_state_board_path.set("")

		self.cb_choose_color = ttk.Combobox(self, state="readonly",values=["red","blue"],textvariable=self.var_color_p1)
		self.cb_choose_color.grid(row=3, column=0, sticky="w", padx=10)

		self.radiobutton_7 = Radiobutton(self, text="Human", variable=self.var_p2_type, value="Human")
		self.radiobutton_7.grid(row=3, column=1, sticky="w")
		self.radiobutton_8 = Radiobutton(self, text="Test Algorithm", variable=self.var_p2_type, value="Test Algorithm")
		self.radiobutton_8.grid(row=4, column=1, sticky="w")
		self.radiobutton_9 = Radiobutton(self, text="AI-Model", variable=self.var_p2_type, value="AI-Model")
		self.radiobutton_9.grid(row=5, column=1, sticky="w")

		self.CbModel2 = ttk.Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=self.var_p2_model)
		self.CbModel2.grid(row=6, column=1,sticky="w",padx=10)

		self.checkbox_allow_overrule = Checkbutton(self, text="Allow overrule", variable=self.var_allow_overrule)
		self.checkbox_allow_overrule.grid(row=7, column=0,columnspan=2)

		self.bottomframe = Frame(self, highlightbackground="blue", highlightthickness=3, borderwidth=1)
		self.bottomframe.grid(row=8, column=0, sticky="w",columnspan=2, padx=10, pady=15)

		self.label_load_state = Label(self.bottomframe, text="Choose file board state: ")
		self.label_load_state.grid(row=0, column=0, sticky="w")
		self.load_state_entry = Entry(self.bottomframe, textvariable=self.var_state_board_path, width=50)
		self.load_state_entry.grid(row=1, column=0, sticky="w",columnspan=2)
		self.button_browse_state_file = Button(self.bottomframe, text="...", command=lambda: self.browse_state_files())
		self.button_browse_state_file.grid(row=1, column=2, sticky="w")

	def browse_state_files(self):
		file_path = filedialog.askopenfilename(filetypes=[("txt File", "*.txt")],initialdir=r".\test_situations")
		self.var_state_board_path.set(file_path if os.path.exists(file_path) else "")

	def load_board_from_file(self)->list[list[int]]|None:
		try:
			with open(self.var_state_board_path.get(), "r") as file:
				board = [[0] * 15 for _ in range(15)] # 0 = empty, 1 = player 1, 2 = player 2.
				for row in range(15):
					line = file.readline().strip().replace(" ", "") # remove \n and spaces
					if len(line) != 15 or not all(i in "012" for i in line):
						return None
					board[row] = [int(i) for i in line]
						
			print("board loaded")
			return board
		except:
			return None

	def start_new_game(self):
		if self.var_state_board_path.get()!="":
			initial_board = self.load_board_from_file()
			if initial_board is None:
				messagebox.showerror("Error", "Invalid file selected", parent=self)
				return
		else:
			initial_board = None

		#p1=Human, p2=...
		match self.var_p2_type.get():
			case "Human":
				self.master.controller = human_vs_human_controller.Human_vs_HumanController(self.master,initial_board)
			case "Test Algorithm":
				self.master.controller = human_vs_test_algorithm_controller.Human_vs_TestAlgorithmController(self.master,self.var_color_p1.get(),initial_board)
			case "AI-Model":
				self.master.controller = human_vs_AI_controller.Human_vs_AI_Controller(self.master,self.var_color_p1.get(),self.var_p2_model.get(),initial_board,self.var_allow_overrule.get())