


from cgitb import reset
import re


timer_bezig=False


def initialiseer_timer():
    global root_timer,label_timer,seconden_over,reset
    from tkinter import Tk, Label
    reset=False
    root_timer=Tk()
    root_timer.geometry("300x300")
    root_timer.title("Timer")
    seconden_over=30
    label_timer=Label(root_timer,text=seconden_over,font=("Arial", 30),borderwidth=3, relief="solid")
    label_timer.place(relx=0.5, rely=0.5, anchor="center")
    root_timer.mainloop()



def reset_timer():
    global reset
    reset=True

def verander_timer():
    global root_timer,label_timer,seconden_over,timer_bezig,reset
    timer_bezig=True
    seconden_over=seconden_over-1
    label_timer.config(text=seconden_over,fg="red"if seconden_over<10 else "black")

    if seconden_over>0 and reset==False:
        root_timer.after(1000,verander_timer) #roept zichzelf aan
        
    else:
        seconden_over=30
        label_timer.config(text=seconden_over,fg="black")
        timer_bezig=False #lees: thread.join() of thread.is_alive() of thread bezig



    