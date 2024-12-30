from tkinter import Menu

class Menubar(Menu):
	def __init__(self, master,*args,**kwargs):
		super().__init__(master,*args,**kwargs)
		self.master = master

		self.new_game_menu = Menu(self,tearoff=0)

		commands = [
			("Play", "p"),
			("Play with physical board", "b"),
			("Replay", "r"), # a seperator is added here
			("Train", "t"),
			("Evaluate", "e"),
		]

		for index, (label, _) in enumerate(commands):
			self.new_game_menu.add_command(
				label=label, command=lambda lbl=label: self.master.open_new_window(lbl))
			
			if index == 2:
				self.new_game_menu.add_separator()

		for label, key in commands:
			self.master.bind(key, lambda event, lbl=label: self.master.open_new_window(lbl))

		self.add_cascade(label="New Game",menu=self.new_game_menu)

		self.models_menu = Menu(self,tearoff=0)
		self.models_menu.add_command(label="models", command=lambda:self.master.open_new_window("Models"))
		self.add_cascade(label="Models",menu=self.models_menu)