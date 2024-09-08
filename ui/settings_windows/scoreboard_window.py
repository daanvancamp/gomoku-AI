import tkinter as tk 
from configuration.config import *
import ui.main_window

WIDTH=int(config["OTHER VARIABLES"]["WIDTH"])
HEIGHT=int(config["OTHER VARIABLES"]["HEIGHT"])
#todo: window verder afwerken
class ScoreboardWindow (tk.Toplevel):#the methods of gomokuapp need to be callable from the frame
	def __init__(self, master: "ui.main_window.GomokuApp"):
		super().__init__(master)

		self.check_var = tk.BooleanVar()
		self.title("Scoreboard Window")
		self.geometry(f"{WIDTH}x{HEIGHT}")
		self.master: "ui.main_window.GomokuApp" = master
		self.scoreboard_check = tk.Checkbutton(self, text="Show scoreboard", variable=self.check_var)
		self.scoreboard_check.grid(row=1, column=0, columnspan=2)
		self.button_apply_changes = tk.Button(self, text="Apply", command=self.apply_changes)
		self.button_apply_changes.grid(row=2, column=0, columnspan=2)
		self.master = master

	def apply_changes(self):
		self.master.draw_scoreboard_bool = self.check_var.get()
		self.master.close_secondary_windows()
		



