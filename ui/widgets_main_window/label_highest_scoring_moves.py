from tkinter import Label

class LabelHighestScoringMoves(Label):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.config(bg="#357EC7", fg="white",font=("bold",14),width=150,wraplength=150)

	def update(self, highest_scoring_moves):
		self.config(text=f"Moves with highest score: {highest_scoring_moves}"if len(highest_scoring_moves)<10 else highest_scoring_moves[:10]+"...")
