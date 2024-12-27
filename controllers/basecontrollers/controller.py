import game.game
import ui.main_window
from game.stats.player_stats import update_player_stats
from file_management import filereader
from configuration.config import config

import logging


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

		self.record_replay = True
		self.last_move_model = None #value remains none when playing Human vs Human or Human vs Test
		self.BOARD_SIZE = int(config["GAME"]["board_size"])

	def set_up_game(self,player_types,board=None):
		p1_type, p2_type = player_types
		player1 = game.game.GameFactory.create_player(p1_type, 1) #player 1 always plays red and begins
		player2 = game.game.GameFactory.create_player(p2_type, 2)

		game_board = game.game.GameFactory.create_game_board(int(config["GAME"]["board_size"]))
		self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
		if any(p.type == "Test" for p in (self.game.player1, self.game.player2)):
			self.game.player1.game = self.game#needed for the test algorithm
			self.game.player2.game = self.game

		if board is not None:
			self.game.board.board = board
			print("initial board loaded")
			self.view.draw_pieces(self.game.board.board)
		else:
			self.reset_board()
		self.view.activate_game()

	def reset_board(self):
		game.game.Game().board.reset_board()
	
	def check_and_handle_winner(self):
		if self.game.winner == 0:#no winner, or tie
			return False
		
		if self.game.winner > 0: #one player won
			print("there's a winner")
			self.view.draw_line(self.game.board.winning_cells)
			if any(p.type == "Human" for p in (self.game.player1, self.game.player2)) or self.view.game_type == ui.main_window.GameType.evaluate:#if there's a human_player
				self.view.end_game()
		elif self.game.winner == -1: # draw
			self.view.end_game_draw()

		self.view.window_mode = ui.main_window.WindowMode.pause
		self.reset_board()
		update_player_stats(self.game,self.game.winner)
		if self.record_replay:
			filereader.save_replay(self.game.p1_moves, self.game.p2_moves)
		return True

	def get_player(self, player_id):
		match player_id:
			case 1:
				return self.game.player1
			case 2:
				return self.game.player2
			case _:
				return None

		
