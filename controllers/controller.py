import game.game
import numpy as np
import ui.main_window
class BaseController:
    def __init__(self, view):
        self.view:"ui.main_window.GomokuApp" = view
        self.view.controller = self
    def initialize_board(self):
        game.game.Game().board.board = np.zeros((game.game.Game().board.board_size,game.game.Game().board.board_size))
    
    def check_and_handle_winner(self):
        #todo: verder uitwerken wat er gebeurt als er een winnaar is; de winnende lijn moet uitgetekend worden
        if self.game.winner != 0:
            print("er is een winnaar")
            self.view.end_game()
            self.initialize_board()
            return True
        else:
            return False


        
