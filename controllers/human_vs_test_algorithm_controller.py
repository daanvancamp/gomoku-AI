import ui.main_window
from .basecontrollers import controller
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Human_vs_TestAlgorithmController(controller.BaseController):
	def __init__(self, view:"ui.main_window.GomokuApp", color_human,initial_board=None):
		super().__init__(view)
		self.set_up_game(("Human", "Test") if color_human=="red" else ("Test", "Human"),initial_board)

		if self.game.player1.type=="Test": #red/player1 always plays first
			self.algorithm_put_piece()

	def human_put_piece(self, row, col):
		if self.game.put_piece(row, col):
			self.view.draw_pieces(self.game.board.board)

			if not self.check_and_handle_winner():
				self.algorithm_put_piece()
				self.check_and_handle_winner()
				
	def algorithm_put_piece(self):
		self.view.window_mode = ui.main_window.WindowMode.computer_move
		row, col = self.game.current_player.test_algorithm.ai_move()
		self.game.put_piece(row, col)
		self.view.draw_pieces(self.game.board.board)
		self.view.window_mode = ui.main_window.WindowMode.human_move

		
		
		