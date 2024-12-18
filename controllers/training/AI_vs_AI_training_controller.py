from controllers.basecontrollers import controller_training
import game.game
import ui.main_window
from configuration.config import *
import game.algorithms.ai.ai
import logging
from utils import stats, player_stats
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class AI_vs_AI_TrainingController(controller_training.BaseTrainingController):
    def __init__(self, view: "ui.main_window.GomokuApp",color_p1,modelname_1="standaard+3000",modelname_2="standaard+3000"):
        super().__init__(view)
        logger.info("Initialize AI_vs_AI_TrainingController")
        player1, player2 = (game.game.GameFactory.create_player("AI", i) for i in (1, 2))
        
        if color_p1=="red": #red always plays first
            player1.load_model(modelname_1,True)
            player2.load_model(modelname_2,True)
        else:
            player1.load_model(modelname_2,True)
            player2.load_model(modelname_1,True)

        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.view.window_mode = ui.main_window.WindowMode.computer_move
        self.view.activate_game()

        while True:
            self.AI_put_piece() #current player does a move (the player switches after each move)
            if self.check_and_handle_winner():
                break

        self.train_at_the_end_of_the_round()
        

    
