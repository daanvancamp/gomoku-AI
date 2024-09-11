
#This is the startup file, run this one to start the game

from datetime import datetime
from utils.filereader import log_info_overruling
from ui import main_window
#from utils.music import initialiseer_muziek
from configuration.config import *
from logger_config import setup_logger



def log_new_run():
    log_info_overruling("\n\n\n\n\ndate and time: "+datetime.now().isoformat())
    log_info_overruling("\nnew run of the code begins:")




# Set up the logger
logger = setup_logger()

def main():
    logger.info("Starting the application")



# Running the application
if __name__ == "__main__":    
    logger.info("Starting the application")
    app = main_window.GomokuApp()    
    app.mainloop()
    
