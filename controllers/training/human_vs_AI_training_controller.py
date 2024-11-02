from controllers.basecontrollers import controller_training
import game.game
import ui.main_window
from configuration.config import *
import numpy as np
import game.algorithms.ai.ai
import logging
from utils import stats, player_stats
# Use the existing logger by name
logger = logging.getLogger('my_logger')
#todo there's a bugfix needed
class Human_vs_AI_TrainingController(controller_training.BaseTrainingController):
    def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname="standaard+3000"):
        super().__init__(view)
        logger.info("Initialize Human_vs_AI_TrainingController")
        if color_AI=="red": #red always plays first
            player1 = game.game.GameFactory.create_player("AI", 1)
            player2 = game.game.GameFactory.create_player("Human", 2)
            self.AI_player = player1
        else:
            player1 = game.game.GameFactory.create_player("Human", 1) #player 1 always plays red and begins
            player2 = game.game.GameFactory.create_player("AI", 2)
            self.AI_player = player2

        self.AI_player.load_model(modelname,True)

        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()

        if self.game.player1.type=="AI": #player 1 always plays red and begins
            self.AI_put_piece()
        
    def human_put_piece(self, row, col):
        if self.game.put_piece(row, col):
            logger.info("Human move")       
            self.view.draw_pieces(self.game.board.board)
            if not self.check_and_handle_winner():
                self.AI_put_piece()
                 #todo fix the bug that causes the program to detect a win too late
                self.check_and_handle_winner() #todo check if this line causes issues
                if self.game.winner!=0: # if someone won
                    self.train_at_the_end_of_the_round()
            else:
                self.train_at_the_end_of_the_round()
                #todo finish this

    
