from controllers.basecontrollers import controller_training
import game.game
import ui.main_window
from configuration.config import *
import game.algorithms.ai.ai
import logging
from utils import stats, player_stats
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class TestAlgorithm_vs_AI_TrainingController(controller_training.BaseTrainingController):
    def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname="standaard+3000"):
        super().__init__(view)
        logger.info("Initialize TestAlgorithm_vs_AI_TrainingController")
        if color_AI!="red": #red always plays first
            player1 = game.game.GameFactory.create_player("Test", 1) #player 1 always plays red and begins
            player2 = game.game.GameFactory.create_player("AI", 2)
            self.AI_player=player2
        else:
            player1 = game.game.GameFactory.create_player("AI", 1)
            player2 = game.game.GameFactory.create_player("Test", 2)
            self.AI_player=player1

        self.AI_player.load_model(modelname,True)

        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.game.player1.game = self.game
        self.game.player2.game = self.game
        self.view.window_mode = ui.main_window.WindowMode.computer_move
        self.view.activate_game()

        if self.game.player1.type=="AI": #player 1 always plays red and begins, in other words, AI begins if it is red.
            while True:
                self.AI_put_piece()
                if self.check_and_handle_winner():
                    break
                self.algorithm_put_piece()
                if self.check_and_handle_winner():
                    break
        else:
            while True:
                self.algorithm_put_piece()
                if self.check_and_handle_winner():
                    break
                self.AI_put_piece()
                if self.check_and_handle_winner():
                    break

        self.train_at_the_end_of_the_round()

    def algorithm_put_piece(self):
        self.view.window_mode = ui.main_window.WindowMode.computer_move
        row, col = self.game.current_player.test_algorithm.ai_move()
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board)

        test_algorithm = game.algorithms.test_algorithm.TestAlgorithm.TestAlgorithm(self.game.current_player)
        test_algorithm.board = self.game.board.board
        scoreboard = test_algorithm.evaluate_board()#calculate scoreboard 
        print("###########")
        print(scoreboard)
        self.view.draw_scoreboard(self.game.board.board, scoreboard) #draw scoreboard if enabled
        

    
