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
		if color_AI=="red": #red always plays first (and is player 1)
			p1_type,p2_type = ("AI", "Test")
		else:
			p1_type,p2_type = ("Test", "AI")

		player1 = game.game.GameFactory.create_player(p1_type, 1)
		player2 = game.game.GameFactory.create_player(p2_type, 2)
			
		self.AI_player = player1 if color_AI=="red" else player2
		self.AI_player.load_model(modelname,True)

		game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
		self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
		self.initialize_board()

		self.game.player1.game = self.game
		self.game.player2.game = self.game
		self.view.window_mode = ui.main_window.WindowMode.computer_move
		self.view.activate_game()

		p1_play, p2_play = (self.AI_put_piece, self.algorithm_put_piece) if self.game.player1.type=="AI" else (self.algorithm_put_piece, self.AI_put_piece)

		while True:
			p1_play()
			if self.check_and_handle_winner():
				break
			p2_play()
			if self.check_and_handle_winner():
				break

		self.train_at_the_end_of_the_round()

	def algorithm_put_piece(self):
		self.view.window_mode = ui.main_window.WindowMode.computer_move
		row, col = self.game.current_player.test_algorithm.ai_move()
		self.game.put_piece(row, col)
		self.view.draw_pieces(self.game.board.board)
	
