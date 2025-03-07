from tkinter import Menu

class Menubar(Menu):
	def __init__(self, master,*args,**kwargs):
		super().__init__(master,*args,**kwargs)
		self.master = master

		self.new_game_menu = Menu(self,tearoff=0)

		commands = [
			("Play","Play", "p"),
			("Play with physical board","PhysicalPlay", "b"),
			("Replay","Replay", "r"),
			("Train","Train", "t"),
			("Evaluate","Evaluate", "e"),
		]

		for index, (label, internal_name,abbreviation) in enumerate(commands):
			self.new_game_menu.add_command(
				label=f"{label} ({abbreviation})", command=lambda name=internal_name: self.master.open_new_window(name))
			
			if index == 2:
				self.new_game_menu.add_separator()

		for label,internal_name, key in commands:
			self.master.bind(key, lambda event, name=internal_name: self.master.open_new_window(name))

		self.add_cascade(label="New Game",menu=self.new_game_menu)

		self.models_menu = Menu(self,tearoff=0)
		self.models_menu.add_command(label="models", command=lambda:self.master.open_new_window("Models"))
		self.add_cascade(label="Models",menu=self.models_menu)