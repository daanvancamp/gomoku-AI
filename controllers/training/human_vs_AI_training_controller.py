from controllers.basecontrollers import controller_training
import game.game
import ui.main_window
from configuration.config import config
import game.algorithms.ai.ai
import logging
from utils import filereader, stats, player_stats
# Use the existing logger by name
logger = logging.getLogger('my_logger')
#todo there's a bugfix needed (zero division error)
class Human_vs_AI_TrainingController(controller_training.BaseTrainingController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname="standaard+3000"):
		super().__init__(view)
		logger.info("Initialize Human_vs_AI_TrainingController")
		self.last_round = True #only one round

		self.set_up_game(("AI", "Human") if color_AI=="red" else ("Human", "AI"))

		self.AI_player = self.game.player1 if color_AI=="red" else self.game.player2
		self.AI_player.load_model(modelname,True)

		if self.game.player1.type=="AI": #player 1 always plays red and begins
			self.AI_put_piece()
		else:
			self.view.window_mode = ui.main_window.WindowMode.human_move

	def human_put_piece(self, row, col):
		if self.game.put_piece(row, col):
			logger.info("Human move")
			self.view.draw_pieces(self.game.board.board)
			if not self.check_and_handle_winner():
				self.AI_put_piece()
				self.check_and_handle_winner()
				if self.game.winner!=0: # if someone won
					self.train_at_the_end_of_the_round()
			else:
				self.train_at_the_end_of_the_round()

	
