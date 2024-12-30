import game.algorithms.ai.ai
from game.playboard_processor import PlayBoardProcessor
import ui.main_window
from features.speak_coordinates import speak_coordinates
from .basecontrollers import controller

import numpy as np
import logging
import cv2

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Human_vs_AI_RecognitionController(controller.BaseController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_human, modelname="standaard+3000"):
		super().__init__(view)
		logger.info("Initialize Human_vs_AI_RecognitionController")

		self.set_up_game(("Human", "AI") if color_human=="red" else ("AI", "Human")) # red always begins

		self.AI_player = self.game.player1 if color_human != "red" else self.game.player2
		self.AI_player.load_model(modelname,False)
		
		self.set_up_recognition(color_human)

		if self.game.player1.type=="AI": #player 1 always plays red and begins
			self.AI_put_piece()
		else:
			self.view.window_mode = ui.main_window.WindowMode.recognition
			
	def set_up_recognition(self,color_human):
		self.playboard_processor = PlayBoardProcessor("red", "blue", color_human)
		self.cap = cv2.VideoCapture(1,cv2.CAP_ANY) # faster connection time # isopened returns true until cap.release is used if you connect a webcam at first
		if not self.cap.isOpened():
			self.view.show_error("Camera not found","Please make sure the camera is connected to your computer and try again.")
			self.view.window_mode = ui.main_window.WindowMode.pause
			return
		
		self.view.frame_webcam.update_video_feed()

	def human_get_and_process_move(self,frame):
		human_move, edited_frame, error_message = self.playboard_processor.get_move(frame)
		if error_message is None:
			print(human_move)
			speak_coordinates(*human_move,self.game.current_player.type)
			self.human_put_piece(*human_move)
			self.view.frame_webcam.show_board(edited_frame)
		else:
			self.view.show_error("Error while analyzing frame",error_message)

	def human_put_piece(self, row, col):
		if self.game.put_piece(row, col): # if the square is empty do..., otherwise do nothing
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
		
		coordinates_best_moves = list(zip(*np.where(scores == max_score))) # AI or the overruling chooses one of these moves
		self.view.label_highest_scoring_moves.update(coordinates_best_moves)

		np_scores = np.array(scores).reshape(self.BOARD_SIZE, self.BOARD_SIZE)
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

		speak_coordinates(*action,self.game.current_player.type)
		self.game.put_piece(*action)
		self.view.draw_pieces(self.game.board.board)
		self.view.window_mode = ui.main_window.WindowMode.recognition

