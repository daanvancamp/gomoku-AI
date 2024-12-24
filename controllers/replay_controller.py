import json
import game.gameboard as gb
from .basecontrollers import controller
from configuration.config import *
import logging
import ui.main_window

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class ReplayController(controller.BaseController):
	def __init__(self, view):
		super().__init__(view)
		self.moves = None
		self.game_board = gb.GameBoard(int(config["GAME"]["board_size"]))
		self.current_index = -1
		self.view = view
		self.view.window_mode = ui.main_window.WindowMode.replay

	def load_game(self, file_name):
		try:
			f = open(file_name,"r")
			self.moves = json.load(f)["moves"]
			self.current_index = -1
			self.activate_replay_buttons()
			self.view.draw_pieces(self.game_board.board)
		except json.JSONDecodeError:
			self.view.show_load_error("Invalid JSON file or not a json file")
		except Exception as e:
			self.view.show_load_error(e)
			
	def next_move(self):
		if self.current_index < len(self.moves) - 1:
			self.current_index += 1
			position_tuple = eval(self.moves[self.current_index]['position'])
			player_id = eval(self.moves[self.current_index]['player'])
			self.game_board.put_piece(position_tuple[0], position_tuple[1], player_id) 
		return self.game_board
		
	def previous_move(self):
		if self.current_index >= 0:
			self.current_index -= 1
			position_tuple = eval(self.moves[self.current_index]['position'])
			player_id = eval(self.moves[self.current_index]['player'])
			self.game_board.remove_piece(position_tuple[0], position_tuple[1])
		return self.game_board
	
	def activate_replay_buttons(self):
		self.view.activate_replay_frame()