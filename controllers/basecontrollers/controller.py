import game.game
import ui.main_window
from utils.player_stats import update_player_stats
import logging
from utils import filereader

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class BaseController:
	def __init__(self, view):
		self.view:"ui.main_window.GomokuApp" = view
		self.view.controller = self
		self.view.clear_canvas()
		self.view.hide_unnecessary_widgets()
		if self.view.frame_webcam.after_id is not None:
			self.view.after_cancel(self.view.frame_webcam.after_id)

		self.record_replay = True #todo add this option to the GUI
		self.last_move_model=None #value remains none when playing Human vs Human or Human vs Test

	def initialize_board(self):
		game.game.Game().board.reset_board()
	
	def check_and_handle_winner(self):
		if self.game.winner != 0:
			print("er is een winnaar")
			self.view.draw_line(self.game.board.winning_cells)
			self.view.end_game()
			self.view.window_mode = ui.main_window.WindowMode.pause
			self.initialize_board()
			update_player_stats(self.game,self.game.winner)
			if self.record_replay:
				filereader.save_replay(self.game.p1_moves, self.game.p2_moves)
			return True
		else:
			return False

	def get_player(self, player_id):
		match player_id:
			case 1:
				return self.game.player1
			case 2:
				return self.game.player2
			case _:
				return None

		
