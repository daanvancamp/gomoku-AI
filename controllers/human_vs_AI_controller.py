import game.game
import ui.main_window
from . import controller
from configuration.config import *
import numpy as np
from utils.utils_AI import Utils_AI
import NN.ai

class Human_vs_AI_Controller(controller.BaseController):
    def __init__(self, view: "ui.main_window.GomokuApp"):
        super().__init__(view)
        player1 = game.game.GameFactory.create_player("Human", 1)
        player2 = game.game.GameFactory.create_player("AI", 2)
        player2.load_model("standard-Mikko")
        player2.set_allow_overrule(False) #todo: add GUI element to let the user decide
        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()

        self.utils_AI = Utils_AI()
        self.record_replay = True
        self.mark_last_move_model = False
        
    def human_put_piece(self, row, col):
        if self.game.put_piece(row, col):
            self.view.draw_pieces(self.game.board.board)
            self.view.draw_scoreboard(self.game.board.board)
            if not self.check_and_handle_winner():
                self.AI_put_piece()
                self.check_and_handle_winner()

    def AI_put_piece(self):
        one_hot_board = self.utils_AI.convert_to_one_hot(self.game.board.board, self.game.current_player.id)
        DVC_AI:NN.ai.GomokuAI = self.game.current_player.ai#player1.ai or player2.ai #always an instance of GomokuAI
        DVC_AI.set_game(one_hot_board)
        max_score, scores, scores_normalized = self.utils_AI.calculate_score(self.game.board.board)
        DVC_AI.current_player_id=self.game.current_player.id
        action = DVC_AI.get_action(self.game.board.board, one_hot_board, scores_normalized)
               
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
