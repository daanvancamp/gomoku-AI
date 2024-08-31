import json
import game.game
import ui.main_window
from . import controller
from config import *

# controller.py
class Human_vs_HumanController(controller.BaseController):
    def __init__(self, view: "ui.main_window.MainApp"):
        super().__init__(view)
        player1 = game.game.GameFactory.create_player("Human", 1)
        player2 = game.game.GameFactory.create_player("Human", 2)
        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()

    def human_put_piece(self, row, col):
        self.game.put_piece(row, col)
        self.view.draw_pieces(game.game.Game().board.board)
        if self.game.winner != 0:
            print("er is een winnaar")
            #todo: verder uitwerken wat er gebeurt als er een winnaar is; de winnende lijn moet uitgetekend worden