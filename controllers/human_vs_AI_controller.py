import game.game
import ui.main_window
from . import controller
from configuration.config import *
import numpy as np
from utils.utils_AI import Utils_AI
import NN.ai
#todo: controller uitwerken om tegen AI te spelen

class Human_vs_AI_Controller(controller.BaseController):
    def __init__(self, view: "ui.main_window.GomokuApp"):
        super().__init__(view)
        player1 = game.game.GameFactory.create_player("Human", 1)
        player2 = game.game.GameFactory.create_player("AI", 2)
        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()

        self.utils_AI = Utils_AI()

    def human_put_piece(self, row, col):
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board)
        if not self.check_and_handle_winner():

            self.AI_put_piece()
            self.check_and_handle_winner()

    def AI_put_piece(self):
        #todo: add AI move
        one_hot_board = self.utils_AI.convert_to_one_hot(self.game.board.board, self.game.players[self.game.current_player.id-1].id)
        DVC_AI:NN.ai.GomokuAI = self.game.players[self.game.current_player.id-1].ai#player1.ai or player2.ai #always an instance of GomokuAI
        DVC_AI.set_game(one_hot_board)
        max_score, scores, scores_normalized = self.utils_AI.calculate_score(self.game.board.board)
        DVC_AI.current_player_id=self.game.current_player.id
        action = DVC_AI.get_action(self.game.board.board, one_hot_board, scores_normalized)
               
        np_scores = np.array(scores).reshape(15, 15)
        short_score = np_scores[action[0]][action[1]]
        # if mark_last_move_model:
        #     last_move_model=action #=last move for example :(3,6)
        # else:
        #     last_move_model=None
        if max_score <= 0:
            # prevent division with negative values or zero
            score = 0
        else:
            score = short_score / max_score

        # if self.game.current_player.id == 1 and instance.record_replay:
        #     p1_moves.append(action)
        # elif instance.record_replay:
        #     p2_moves.append(action)

        self.game.players[self.game.current_player.id - 1].weighed_moves.append(score)
        self.game.board.board[action[0]][action[1]] = self.game.current_player.id
        self.game.players[self.game.current_player.id-1].final_action = action
        self.game.players[self.game.current_player.id - 1].moves += 1

        row, col = action
        self.game.put_piece(row, col)
        self.view.draw_pieces(game.game.Game().board.board)