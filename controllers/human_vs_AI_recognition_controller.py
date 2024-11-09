import game.game
import ui.main_window
from .basecontrollers import controller
from configuration.config import *
import numpy as np
import game.algorithms.ai.ai
import logging
import cv2
from game.playboard_processor import PlayBoardProcessor
# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Human_vs_AI_RecognitionController(controller.BaseController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_human, modelname="standaard+3000"):
		super().__init__(view)
		logger.info("Initialize Human_vs_AI_Controller")

		if color_human=="red": #red always plays first
			player1 = game.game.GameFactory.create_player("Human", 1) #player 1 always plays red and begins
			player2 = game.game.GameFactory.create_player("AI", 2)
			self.AI_player = player2
		else:
			player1 = game.game.GameFactory.create_player("AI", 1)
			player2 = game.game.GameFactory.create_player("Human", 2)
			self.AI_player = player1

		self.AI_player.load_model(modelname,False)

		game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
		self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
		self.initialize_board()

		self.view.activate_game()
		
		self.playboard_processor = PlayBoardProcessor("red", "blue", color_human) #red always plays first
		self.cap = cv2.VideoCapture(1,cv2.CAP_ANY) #faster connection time #isopened returns true until cap.release is used if you connect a webcam at first
		if not self.cap.isOpened():
			self.view.show_error("Camera not found","Please make sure the camera is connected to your computer and try again.")
			self.view.window_mode = ui.main_window.WindowMode.pause
			return
		
		self.view.frame_webcam.update_video_feed()

		if self.game.player1.type=="AI": #player 1 always plays red and begins
			self.AI_put_piece()
		else:
			self.view.window_mode = ui.main_window.WindowMode.recognition
		
	def human_get_and_process_move(self,frame):
		human_move, edited_frame = self.playboard_processor.get_move(frame)
		match human_move:
			case [one_human_move]:
				if isinstance(one_human_move[0],str) or isinstance(one_human_move[1] ,str):
					self.view.show_error("Invalid move",f"invalid coordinates:{one_human_move}")
				else:
					self.human_put_piece(one_human_move[0], one_human_move[1])
					self.view.frame_webcam.show_board(edited_frame)

			case "multiple moves detected":
				self.view.show_error("Multiple moves detected","Please only make one move at a time.")

			case "no moves detected":
				self.view.show_error("No moves detected","Did you make any moves?")

			case "no chessboard detected":
				self.view.show_error("Chessboard not detected","Please make sure the chessboard is clearly visible and try again.")

			case _:
				self.view.show_error("Unknown error",f"Please try again. move: {human_move}")

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
		self.view.window_mode = ui.main_window.WindowMode.recognition

