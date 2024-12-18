from tkinter import Label

class LabelHighestScoringMoves(Label):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.config(bg="blue", fg="white")

	def update(self, highest_scoring_moves):
		self.config(text=f"Moves with highest score: {highest_scoring_moves}")
