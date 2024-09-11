import game.game
import ui.main_window
from . import controller
from configuration.config import *
import numpy as np
import game.algorithms.ai.ai
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Human_vs_AI_Controller(controller.BaseController):
    def __init__(self, view: "ui.main_window.GomokuApp"):
        super().__init__(view)
        logger.info("Initialize Human_vs_AI_Controller")

        player1 = game.game.GameFactory.create_player("Human", 1)
        player2 = game.game.GameFactory.create_player("AI", 2)
        player2.load_model("standard-Mikko")
        player2.set_allow_overrule(False) #todo: add GUI element to let the user decide
        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()

        self.record_replay = True
        self.mark_last_move_model = False
        
    def human_put_piece(self, row, col):
        logger.info("Human move")       

        if self.game.put_piece(row, col):
            self.view.draw_pieces(self.game.board.board)
            if not self.check_and_handle_winner():
                self.AI_put_piece()
                self.check_and_handle_winner()

    def AI_put_piece(self):
        logger.info("AI move")             
        
        gomoku_ai:game.algorithms.ai.ai.AI_Algorithm = self.game.current_player.ai
        gomoku_ai.board = self.game.board.board
        gomoku_ai.current_player_id = self.game.current_player.id
        gomoku_ai.convert_to_one_hot()
        max_score, scores, scores_normalized = gomoku_ai.calculate_score()
        action = gomoku_ai.get_action(scores_normalized)
               
        np_scores = np.array(scores).reshape(15, 15)
        short_score = np_scores[action[0]][action[1]]
        if self.mark_last_move_model:
            self.last_move_model=action #=last move for example :(3,6)
        else:
            self.last_move_model=None

        if max_score <= 0:
            # prevent division with negative values or zero
            score = 0
        else:
            score = short_score / max_score

        if self.record_replay:
            if self.game.current_player.id == 1:
                self.game.p1_moves.append(action)
            else:
                self.game.p2_moves.append(action)

        self.game.current_player.weighed_moves.append(score)
        self.game.current_player.final_action = action
        self.game.current_player.moves += 1

        row, col = action
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board) 
