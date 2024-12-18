from controllers.basecontrollers import controller_training
import game.game
import ui.main_window
from configuration.config import config
import game.algorithms.ai.ai
import logging
from utils import filereader, stats, player_stats
# Use the existing logger by name
logger = logging.getLogger('my_logger')
#todo there's a bugfix needed (zero division error)
class Human_vs_AI_TrainingController(controller_training.BaseTrainingController):
	def __init__(self, view: "ui.main_window.GomokuApp",color_AI,modelname="standaard+3000"):
		super().__init__(view)
		self.last_round = True #only one round
		logger.info("Initialize Human_vs_AI_TrainingController")

		if color_AI=="red": #red always plays first
			p1_type,p2_type = ("AI", "Human")
		else :
			p1_type,p2_type = ("Human", "AI")

		player1 = game.game.GameFactory.create_player(p1_type, 1) #player 1 always plays red and begins
		player2 = game.game.GameFactory.create_player(p2_type, 2)

		self.AI_player = player1 if color_AI=="red" else player2
		self.AI_player.load_model(modelname,True)

		game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
		self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
		self.initialize_board()

		self.view.window_mode = ui.main_window.WindowMode.human_move
		self.view.activate_game()

		if self.game.player1.type=="AI": #player 1 always plays red and begins
			self.AI_put_piece()
		
	def human_put_piece(self, row, col):
		if self.game.put_piece(row, col):
			logger.info("Human move")
			self.view.draw_pieces(self.game.board.board)
			if not self.check_and_handle_winner():
				self.AI_put_piece()
				self.check_and_handle_winner()
				if self.game.winner!=0: # if someone won
					self.train_at_the_end_of_the_round()
			else:
				self.train_at_the_end_of_the_round()

	def check_and_handle_winner(self):
		if self.game.winner != 0:
			print("er is een winnaar")
			self.view.draw_line(self.game.board.winning_cells)
			self.view.end_game() #the additional line in comparison to the other training controllers: a messagebox is shown when a human is playing
			self.view.window_mode = ui.main_window.WindowMode.pause
			self.initialize_board()
			player_stats.update_player_stats(self.game,self.game.winner)
			if self.record_replay: #the replay is always recorded, but only saved if the user wants it
				filereader.save_replay(self.game.p1_moves, self.game.p2_moves)
			return True
		else:
			return False

	
