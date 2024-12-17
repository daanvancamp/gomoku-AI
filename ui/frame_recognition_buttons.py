import tkinter as tk

class FrameRecognitionButtons(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.button_move_done = tk.Button(self, text="Move done?", command = self.process_move)
        self.button_move_done.grid(row=0, column=0,pady=2,padx=2)
        self.master.bind("<Right>", lambda event: self.process_move())
        self.master.bind("<space>", lambda event: self.process_move())

    def process_move(self):
        ret, frame = self.master.controller.cap.read()

        if ret:
            self.master.controller.human_get_and_process_move(frame)
        else:
            self.master.show_error("No webcam available", "Please connect a webcam and try again")
