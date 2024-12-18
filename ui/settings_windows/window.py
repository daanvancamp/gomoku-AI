from tkinter import Toplevel
import ui

class BaseWindow(Toplevel):
	def __init__(self, master, WIDTH, HEIGHT, title):
		super().__init__(master, width=WIDTH, height=HEIGHT)

		self.title(title)
		self.geometry(f"{WIDTH}x{HEIGHT}")
		self.attributes("-topmost", True)
		
		self.master: "ui.main_window.GomokuApp" = master