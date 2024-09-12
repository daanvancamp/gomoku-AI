from time import time
import game.game
import ui.main_window
from configuration.config import *
import game.player
import logging


def test_1():
    player1 = game.game.GameFactory.create_player("Human", 1)
    player2 = game.game.GameFactory.create_player("AI", 2)
    player2.load_model("standard-Mikko")
    game_board = game.game.GameFactory.create_game_board(15)
    game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
    board = np.zeros((game.game.Game().board.board_size,game.game.Game().board.board_size))
    game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)

# Running the application
if __name__ == "__main__":    
    test_1()



