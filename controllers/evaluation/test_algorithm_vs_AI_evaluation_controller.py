from controllers.basecontrollers.controller_evaluation import BaseEvaluationController
import ui.main_window
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')
#don't change anything, development in progress
class TestAlgorithm_vs_AI_EvaluationController(BaseEvaluationController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname,allow_overrule):
		super().__init__(view)
		logger.info("Initialize TestAlgorithm_vs_AI_EvaluationController")

		self.set_up_game(("AI", "Test") if color_AI=="red" else ("Test", "AI"))

		self.AI_player = self.game.player1 if color_AI=="red" else self.game.player2
		self.AI_player.load_model(modelname,True)
		self.AI_player.set_allow_overrule(allow_overrule)
		
		self.game.player1.game = self.game#needed for the test algorithm
		self.game.player2.game = self.game

	def algorithm_put_piece(self):
		row, col = self.game.current_player.test_algorithm.ai_move()
		self.game.put_piece(row, col)
		self.view.draw_pieces(self.game.board.board)

	def next_move(self):
		if self.game.winner != 0: 
			return
		if self.game.current_player.type == "AI":
			self.AI_put_piece()
		else:
			self.algorithm_put_piece()
		self.check_and_handle_winner()
