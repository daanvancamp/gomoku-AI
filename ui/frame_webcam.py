import tkinter as tk

class FrameWebcam(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.label_videofeed=tk.Label(self, text="no video feed available")
        self.label_videofeed.grid(row=0, column=0,pady=2,padx=2)
        self.label_board=tk.Label(self, text="no board available")
        self.label_board.grid(row=1, column=0,pady=2,padx=2)

