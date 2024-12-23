from controllers.basecontrollers import controller_training
import ui.main_window
import logging
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class AI_vs_AI_TrainingController(controller_training.BaseTrainingController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_p1,modelname_1="standaard+3000",modelname_2="standaard+3000",last_round=False):
		super().__init__(view,last_round)
		logger.info("Initialize AI_vs_AI_TrainingController")
		self.set_up_game(("AI", "AI"))

		p1_model, p2_model = (modelname_1, modelname_2) if color_p1 == "red" else (modelname_2, modelname_1)
		self.game.player1.load_model(p1_model, True)
		self.game.player2.load_model(p2_model, True)

		self.view.window_mode = ui.main_window.WindowMode.computer_move

		while True:
			self.AI_put_piece() #current player does a move (the player switches after each move)
			if self.check_and_handle_winner():
				break

		self.train_at_the_end_of_the_round()
		

	
