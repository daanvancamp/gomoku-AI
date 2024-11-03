import game.game
import numpy as np
import ui.main_window
from utils.player_stats import update_player_stats
import logging
from utils import filereader

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class BaseController:
    def __init__(self, view):
        self.view:"ui.main_window.GomokuApp" = view
        self.view.controller = self
        self.view.clear_canvas()
        self.record_replay = True #todo add this option to the GUI

    def initialize_board(self):
        game.game.Game().board.reset_board()
    
    def check_and_handle_winner(self):
        if self.game.winner != 0:
            print("er is een winnaar")
            self.view.draw_line(self.game.board.winning_cells)
            self.view.end_game()
            self.initialize_board()
            update_player_stats(self.game,self.game.winner)
            if self.record_replay:
                filereader.save_replay(self.game.p1_moves, self.game.p2_moves)
            return True
        else:
            return False


        
