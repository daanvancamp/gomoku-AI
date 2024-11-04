from threading import Thread
from time import sleep
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox as mb

class FrameWebcam(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.after_id = None
        self.thread = None

        self.label_videofeed=tk.Label(self, text="no video feed available")
        self.label_videofeed.grid(row=0, column=0,pady=2,padx=2)
        self.label_board=tk.Label(self, text="no board available")
        self.label_board.grid(row=1, column=0,pady=2,padx=2)

    def update_video_feed(self):
        ret, frame = self.master.controller.cap.read()
        if ret:
            # convert frame from BGR (OpenCV) to RGB (Tkinter)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label_videofeed.imgtk = imgtk
            self.label_videofeed.configure(image=imgtk)
            self.after_id = self.master.after(20, self.update_video_feed)
        else:
            self.label_videofeed.configure(image="")  # Verwijder de afbeelding
            self.label_videofeed.imgtk = ""
            self.label_videofeed.config(text="no video feed available", bg="red")

            self.master.controller.cap.release() #this results in self.master.controller.cap.isOpened() returning False

            self.thread = Thread(target=self.check_connection_webcam)
            self.thread.start()
            
    def check_connection_webcam(self):
        while not self.master.controller.cap.isOpened():
            sleep(0.5) #minimize CPU usage
            self.master.controller.cap = cv2.VideoCapture(1,cv2.CAP_ANY)
            self.after_id = None
        self.after_id = self.master.after(20, self.update_video_feed)


    

