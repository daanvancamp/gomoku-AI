#todo readd the feature to load a situation, using a text file, how should it be done?
#todo show graphs after training process
#fix bug in models tab
#todo improve player_stats.py, too much unnecessary nesting
#This is the startup file, please run this file to start the game

from datetime import datetime
from utils.filereader import log_info_overruling
from ui import main_window
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
    
