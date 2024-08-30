#from datetime import datetime
#from threading import Thread
#from utils.filereader import log_info_overruling
from ui import main_window
from game import game
#from utils.music import initialiseer_muziek
from controller import controller

from config import *


def log_new_run():
    log_info_overruling("\n\n\n\n\ndate and time: "+datetime.now().isoformat())
    log_info_overruling("\nnew run of the code begins:")


# Running the application
if __name__ == "__main__":    
    app = main_window.MainApp()    
    app.mainloop()
    
