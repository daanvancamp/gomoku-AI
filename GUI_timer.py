



from threading import Thread

eerste_run=True
def initialiseer_timer():
    global root_timer,label_timer,seconden_over
    from tkinter import Tk, Label
    seconden_over=30
    root_timer=Tk()
    root_timer.geometry("300x300")
    root_timer.title("Timer")
    label_timer=Label(root_timer,text=seconden_over,font=("Arial", 30),borderwidth=3, relief="solid")
    label_timer.place(relx=0.5, rely=0.5, anchor="center")
    
    return root_timer
    



def reset_timer():
    global seconden_over,label_timer
    seconden_over=30
    label_timer.config(text=seconden_over,fg="black")

def verander_timer():
    global root_timer,label_timer,seconden_over
    print("verander timer")
    print(seconden_over)
    seconden_over=seconden_over-1
    label_timer.config(text=seconden_over,fg="red"if seconden_over<10 else "black")

    if seconden_over>0 :
        print("verander timer nogmaals")
        root_timer.after(1000,verander_timer) #roept zichzelf aan
        print("na root_timer.after")
        #root_timer.mainloop()

    else:
        seconden_over=30
        label_timer.config(text=seconden_over,fg="black")


