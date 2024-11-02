import tkinter as tk

class FrameRecognitionButtons(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.button_move_done = tk.Button(self, text="Move done", command=lambda: self.master.controller.human_get_move())
        self.button_move_done.grid(row=0, column=0,pady=2,padx=2)

