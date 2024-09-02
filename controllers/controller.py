import game.game
import numpy as np

class BaseController:
    def __init__(self, view):
        self.view = view
        self.view.controller = self
    def initialize_board(self):
        game.game.Game().board.board = np.zeros((game.game.Game().board.board_size,game.game.Game().board.board_size))
    
    def check_winner(self):
        if self.game.winner != 0:
            print("er is een winnaar")
            self.view.end_game()
            self.initialize_board()


        
