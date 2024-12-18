import game.game
import ui.main_window
from .basecontrollers import controller
from configuration.config import config
import numpy as np
import game.algorithms.ai.ai
import logging
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Human_vs_AI_Controller(controller.BaseController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_human, modelname="standaard+3000"):
		super().__init__(view)
		logger.info("Initialize Human_vs_AI_Controller")

		if color_human=="red": #red always plays first
			p1_type,p2_type = ("Human", "AI")
		else :
			p1_type,p2_type = ("AI", "Human")
		
		player1 = game.game.GameFactory.create_player(p1_type, 1)
		player2 = game.game.GameFactory.create_player(p2_type, 2)
			
		self.AI_player = player1 if color_human!="red" else player2
		self.AI_player.load_model(modelname,False)

		game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
		self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
		self.initialize_board() #load the selected situation if requested by the user

		self.view.activate_game()

		if self.game.player1.type=="AI": #player 1 always plays red and begins
			self.AI_put_piece()
		else:
			self.view.window_mode = ui.main_window.WindowMode.human_move
   
	def human_put_piece(self, row, col):
		if self.game.put_piece(row, col): #if the square is empty do..., otherwise do nothing
			logger.info("Human move") 
			self.view.draw_pieces(self.game.board.board)
			if not self.check_and_handle_winner():
				self.AI_put_piece()
				self.check_and_handle_winner()
				  
	def AI_put_piece(self):
		self.view.window_mode = ui.main_window.WindowMode.computer_move
		logger.info("AI move")
		
		gomoku_ai:game.algorithms.ai.ai.AI_Algorithm = self.game.current_player.ai
		gomoku_ai.board = self.game.board.board
		gomoku_ai.current_player_id = self.game.current_player.id
		gomoku_ai.convert_to_one_hot()
		max_score, scores, scores_normalized = gomoku_ai.calculate_score()
		
		action = gomoku_ai.get_action(scores_normalized)
		self.view.overruled_last_move = gomoku_ai.overruled_last_move

		coordinates_best_moves = list(zip(*np.where(scores == max_score)))#AI or the overruling chooses one of these moves
		self.view.label_highest_scoring_moves.update(coordinates_best_moves)

		np_scores = np.array(scores).reshape(15, 15)
		short_score = np_scores[action[0]][action[1]]
		
		self.last_move_model = action #=last move for example :(3,6)

		if max_score <= 0:
			# prevent division with negative values or zero
			score = 0
		else:
			score = short_score / max_score

		self.game.current_player.weighed_moves.append(score)
		self.game.current_player.final_action = action
		self.game.current_player.moves += 1

		row, col = action
		self.game.put_piece(row, col)
		self.view.draw_pieces(self.game.board.board)
		self.view.window_mode = ui.main_window.WindowMode.human_move

