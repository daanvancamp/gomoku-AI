from controllers.basecontrollers.controller_evaluation import BaseEvaluationController
import ui.main_window
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class TestAlgorithm_vs_AI_EvaluationController(BaseEvaluationController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname,allow_overrule):
		super().__init__(view)
		self.set_up_game(("AI", "Test") if color_AI=="red" else ("Test", "AI"))

		AI_player = self.game.player1 if color_AI=="red" else self.game.player2
		AI_player.load_model(modelname,True)
		AI_player.set_allow_overrule(allow_overrule)

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
		if self.check_and_handle_winner():
			self.view.unbind("<Right>",self.binding_id)
