import json
import game.game
import ui.main_window
from . import controller

#todo controller uitwerken om tegen test algoritme te spelen

# controller.py
class Human_vs_TestAlgorithmController(controller.Controller):
    def __init__(self, view):
        super().__init__(view)
        player1 = game.game.GameFactory.create_player("Human", 1)
        player2 = game.game.GameFactory.create_player("Human", 2)
        game_board = game.game.GameFactory.create_game_board(15)
        self.game = game.game.GameFactory.create_game(game_board, player1, player2)
        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()

    def put_piece(self, row, col):
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board)
        if self.game.winner != 0:
            print("er is een winnaar")