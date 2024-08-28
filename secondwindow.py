
from tkinter import *
# Second Window Class
class SecondWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Second Window")
        self.geometry("250x150")

        # Label for Second Window
        label = Label(self, text="This is the Second Window")
        label.pack(pady=20)

        # Button to close the window
        close_button = Button(self, text="Close Window", command=self.destroy)
        close_button.pack()
