import tkinter as tk

class FrameRecognitionButtons(tk.Frame):
	def __init__(self, master):
		super().__init__(master,bg="#357EC7")
		self.master = master

		self.button_move_done = tk.Button(self, text="Move done?",bg="green",fg="white", command = self.process_move)
		self.button_move_done.grid(row=0, column=0,pady=2,padx=2)

		self.id1 = None
		self.id2 = None
		
	def grid(self, *args, **kwargs):
		super().grid(*args, **kwargs)
		self.id1 = self.master.bind("<Right>", lambda event: self.process_move())
		self.id2 = self.master.bind("<space>", lambda event: self.process_move())

	def grid_forget(self, *args, **kwargs):
		super().grid_forget(*args, **kwargs)
		if self.id1 is not None and self.id2 is not None:
			self.master.unbind("<Right>",self.id1)
			self.master.unbind("<space>",self.id2)

	def process_move(self):
		ret, frame = self.master.controller.cap.read()

		if ret:
			self.master.controller.human_get_and_process_move(frame)
		else:
			self.master.show_error("No webcam available", "Please connect a webcam and try again")
