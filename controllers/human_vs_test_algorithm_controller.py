from time import time
import game.game
import ui.main_window
from . import controller
from configuration.config import *
import game.player
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

#todo: controller uitwerken om tegen test algoritme te spelen

# controller.py
class Human_vs_TestAlgorithmController(controller.BaseController):
    def __init__(self, view:"ui.main_window.GomokuApp", color_human):
        super().__init__(view)
        self.last_move_model=None
        start_p=time()
        if color_human=="red": #red always plays first
            player1 = game.game.GameFactory.create_player("Human", 1)
            player2 = game.game.GameFactory.create_player("Test", 2)
        else:
            print("blue selected")
            player1 = game.game.GameFactory.create_player("Test", 1)
            player2 = game.game.GameFactory.create_player("Human", 2)
        print("created 2 players in",time()-start_p)

        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.game.player1.game = self.game
        self.game.player2.game = self.game
        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()
        self.color_human=color_human

        if color_human!="red":
            self.algorithm_put_piece()

    def human_put_piece(self, row, col):
        if self.game.put_piece(row, col):
            self.view.draw_pieces(self.game.board.board)

            if not self.check_and_handle_winner():
                self.algorithm_put_piece()
                self.check_and_handle_winner()
                
    def algorithm_put_piece(self):
        row, col = self.game.current_player.test_algorithm.ai_move()
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board) 
        test_algorithm = game.algorithms.test_algorithm.TestAlgorithm.TestAlgorithm(self.game.current_player)
        test_algorithm.board = self.game.board.board
        scoreboard = test_algorithm.evaluate_board()
        print("###########")
        print(scoreboard)
        self.view.draw_scoreboard(self.game.board.board, scoreboard)
        
        
        