from controllers.basecontrollers import controller_training
import ui.main_window
import logging
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class AI_vs_AI_TrainingController(controller_training.BaseTrainingController):
	def __init__(self, view: "ui.main_window.GomokuApp",modelname_1,modelname_2,last_round):
		super().__init__(view,last_round)
		self.set_up_game(("AI", "AI"))

		self.game.player1.load_model(modelname_1, True)
		self.game.player2.load_model(modelname_2, True)

		self.view.window_mode = ui.main_window.WindowMode.computer_move

		while True:
			self.AI_put_piece() #current player does a move (the player switches after each move)
			if self.check_and_handle_winner():
				break

		self.train_at_the_end_of_the_round()
		

	
