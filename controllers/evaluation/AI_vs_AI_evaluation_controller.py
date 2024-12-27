from controllers.basecontrollers.controller_evaluation import BaseEvaluationController
import ui.main_window

import logging
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class AI_vs_AI_EvaluationController(BaseEvaluationController):
	def __init__(self, view: "ui.main_window.GomokuApp",modelname_1,modelname_2,allow_overrule):
		super().__init__(view)
		logger.info("Initialize AI_vs_AI_EvaluationController")
		self.set_up_game(("AI", "AI"))

		self.game.player1.load_model(modelname_1, True)
		self.game.player2.load_model(modelname_2, True)
		for p in self.game.players: p.set_allow_overrule(allow_overrule)

	def next_move(self):
		if self.game.winner != 0:
			return
		self.AI_put_piece()

		if self.check_and_handle_winner():
			self.view.unbind("<Right>",self.binding_id)

	

	
