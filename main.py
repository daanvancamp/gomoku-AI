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
    ##Create players
    player1 = game.GameFactory.create_player("Human", 1)
    player2 = game.GameFactory.create_player("Human", 2)
    game_board = game.GameFactory.create_game_board(15)
    game = game.GameFactory.create_game(game_board, player1, player2)

    app = main_window.MainApp(controller)    
    controller = controller.Controller(game, app)
    app.set_controller(controller)
    app.mainloop()
    
