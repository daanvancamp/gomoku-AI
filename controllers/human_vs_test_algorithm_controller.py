from time import time
import game.game
import ui.main_window
from . import controller
from configuration.config import *
import game.player
#todo: controller uitwerken om tegen test algoritme te spelen

# controller.py
class Human_vs_TestAlgorithmController(controller.BaseController):
    def __init__(self, view:"ui.main_window.GomokuApp", color_human):
        super().__init__(view)

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
            if self.game.current_player == self.game.player2:
                self.game.switch_player()
            self.algorithm_put_piece()

    def human_put_piece(self, row, col):
        self.game.put_piece(row, col)
        self.view.draw_pieces(game.game.Game().board.board)
        if self.game.winner != 0:
            print("er is een winnaar")
            self.view.end_game()
            self.initialize_board()
        else:
            self.algorithm_put_piece()
            self.handle_winner()
                
    def algorithm_put_piece(self):
        row, col = self.game.current_player.test_algorithm.ai_move()
        self.game.put_piece(row, col)
        self.view.draw_pieces(game.game.Game().board.board)

        #todo verify if this could should be used instead of the above...
        # if self.color_human!="red":
        #     row, col = self.game.player1.test_algorithm.ai_move()
        #     self.game.put_piece(row, col)
        #     self.view.draw_pieces(game.game.Game().board.board)
        # else:
        #     row, col = self.game.player2.test_algorithm.ai_move()
        #     self.game.put_piece(row, col)
        #     self.view.draw_pieces(game.game.Game().board.board)
            