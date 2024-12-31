from controllers.basecontrollers import controller_training
import ui.main_window
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class TestAlgorithm_vs_AI_TrainingController(controller_training.BaseTrainingController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname="standaard+3000",last_round=False):
		super().__init__(view,last_round)
		self.set_up_game(("AI", "Test") if color_AI=="red" else ("Test", "AI"))

		self.AI_player = self.game.player1 if color_AI=="red" else self.game.player2
		self.AI_player.load_model(modelname,True)

		self.view.window_mode = ui.main_window.WindowMode.computer_move

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
		row, col = self.game.current_player.test_algorithm.ai_move()
		self.game.put_piece(row, col)
		self.view.draw_pieces(self.game.board.board)
	
