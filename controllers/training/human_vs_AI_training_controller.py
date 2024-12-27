from controllers.basecontrollers import controller_training
import ui.main_window
import logging
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Human_vs_AI_TrainingController(controller_training.BaseTrainingController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname,last_round, allow_overrule):
		super().__init__(view,last_round)
		logger.info("Initialize Human_vs_AI_TrainingController")
		self.last_round = True #training against a human always consists of one round

		self.set_up_game(("AI", "Human") if color_AI=="red" else ("Human", "AI"))

		AI_player = self.game.player1 if color_AI=="red" else self.game.player2
		AI_player.load_model(modelname,True)
		AI_player.set_allow_overrule(allow_overrule)

		if self.game.player1.type=="AI": #player 1 always plays red and begins
			self.AI_put_piece()

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

	
