from logging import root
import tkthread; tkthread.patch()
import tkinter as tk
from threading import Thread, Event
from queue import Queue
import time

seconden_over = 30
label_timer = None
root_timer = None
running = False  
timer_queue = Queue()
stop_event = Event()

def update_timer():
    global seconden_over, running
    while running and seconden_over > 0:
        seconden_over -= 1
        timer_queue.put(seconden_over)
        time.sleep(1)

def timer_update_label():
    global label_timer
    if not timer_queue.empty():
        time_left = timer_queue.get()
        label_timer.config(text=time_left)
    if running:
        root_timer.after(100, timer_update_label)

def start_timer():
    global root_timer, label_timer, running
    running = True
    if not root_timer:
        root_timer = tk.Tk()
        root_timer.title("Timer")
        label_timer = tk.Label(root_timer, text=seconden_over, font=("Helvetica", 48))
        label_timer.pack()

    # Start updating the timer label
    root_timer.after(100, timer_update_label)
    root_timer.mainloop()

def start_thread_timer():
    Thread(target=start_timer, daemon=True).start()
    Thread(target=update_timer, daemon=True).start()

def reset_timer():
    global seconden_over, running
    running = False  # Stop the timer
    seconden_over = 30
    if label_timer:
        label_timer.config(text=seconden_over)
    running = True
    Thread(target=update_timer, daemon=True).start()

