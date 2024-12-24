import ui.main_window
from controllers.basecontrollers.controller import BaseController

import logging
import numpy as np

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class BaseEvaluationController(BaseController): #evaluation means that the AI plays against AI/Test Algorithm,while someone is evaluating its performance
    def __init__(self, view):
        super().__init__(view)
        self.view.window_mode = ui.main_window.WindowMode.computer_move

    def AI_put_piece(self):
        logger.info("AI move")
        
        gomoku_ai = self.game.current_player.ai
        gomoku_ai.board = self.game.board.board
        gomoku_ai.current_player_id = self.game.current_player.id
        
        old_state = self.game.board.board
        one_hot_board= gomoku_ai.convert_to_one_hot()
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

        row, col = action
        self.game.put_piece(row, col)

        self.view.draw_pieces(self.game.board.board)

        next_max_score, next_scores, next_scores_normalized = gomoku_ai.calculate_score(15)

        gomoku_ai.remember(old_state, action, score,self.game.board.board ,self.game.winner!=0 )
        gomoku_ai.train_short_memory(one_hot_board, action, short_score, scores, gomoku_ai.convert_to_one_hot(),next_scores,self.game.winner!=0)
        self.game.players[self.game.current_player.id - 1].move_loss.append(gomoku_ai.loss)

        self.game.current_player.weighed_moves.append(score)
        self.game.current_player.final_action = action
        self.game.current_player.moves += 1

        
