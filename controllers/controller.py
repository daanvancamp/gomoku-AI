import game.game
import numpy as np
import ui.main_window
from utils.player_stats import update_player_stats
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class BaseController:
    def __init__(self, view):
        self.view:"ui.main_window.GomokuApp" = view
        self.view.controller = self
    def initialize_board(self):
        game.game.Game().board.reset_board()
    
    def check_and_handle_winner(self):
        #todo: verder uitwerken wat er gebeurt als er een winnaar is; de winnende lijn moet uitgetekend worden
        if self.game.winner != 0:
            print("er is een winnaar")
            self.view.end_game()
            self.initialize_board()
            update_player_stats(self.game,self.game.winner)
            return True
        else:
            return False


        
