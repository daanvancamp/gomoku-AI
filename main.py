from datetime import datetime
from threading import Thread
from utils.filereader import log_info_overruling
from UI import mainmenu_window
from utils.music import initialiseer_muziek


# def main():
#     mainmenu.mainmenu_run()

def log_new_run():
    log_info_overruling("\n\n\n\n\ndate and time: "+datetime.now().isoformat())
    log_info_overruling("\nnew run of the code begins:")

if __name__ == '__main__':
    log_new_run()
    initialiseer_muziek()
    app = mainmenu_window.GomokuApp()

    app.mainloop()
