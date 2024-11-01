import game.game
import ui.main_window
from controllers.basecontrollers.controller import BaseController
from utils import stats, player_stats

import logging
import numpy as np

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class BaseTrainingController(BaseController): #training means that the AI plays against AI, Human or test algorithm, while improving its model.
    def __init__(self, view):
        self.view:"ui.main_window.GomokuApp" = view
        self.view.controller = self
        #todo can be changed to super().__init__(view) if the init function of the basecontroller still is the same as the two lines above

        self.last_round = False #todo toggle on and off when needed, temporarily disabled
        self.record_replay = True
        self.last_move_model = None #has to be declared to prevent errors in main_window.py
        self.show_graphs = None #todo let the user choose, add this to the menu in the future

    def AI_put_piece(self):
        logger.info("AI move")
        
        gomoku_ai:game.algorithms.ai.ai.AI_Algorithm = self.game.current_player.ai
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

        if self.record_replay:
            if self.game.current_player.id == 1:
                self.game.p1_moves.append(action)
            else:
                self.game.p2_moves.append(action)

        row, col = action
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board)

        next_max_score, next_scores, next_scores_normalized = gomoku_ai.calculate_score(15)

        gomoku_ai.remember(old_state, action, score,self.game.board.board ,self.game.winner!=0 ) #todo does this work?
        gomoku_ai.train_short_memory(one_hot_board, action, short_score, scores, gomoku_ai.convert_to_one_hot(),next_scores,self.game.winner!=0)
        self.game.players[self.game.current_player.id - 1].move_loss.append(gomoku_ai.loss)

        self.game.current_player.weighed_moves.append(score)
        self.game.current_player.final_action = action
        self.game.current_player.moves += 1

    def train_at_the_end_of_the_round(self):
        print("training at the end of the round")
        player_stats.update_player_stats(self.game,self.game.player1.id if self.game.winner==1 else self.game.player2.id)
        data = {}
        loss_data = {}
        move_loss_data = {}
        for p in self.game.players:
            if p.TYPE == "AI":
                p.ai.remember(self.game.board.board, p.final_action, p.score, self.game.board.board, True)
                p.ai.train_long_memory()
                p.score_loss.append(p.ai.loss)
                move_loss = [float(val) for val in p.move_loss]
                p.final_move_loss.append(sum(move_loss)/len(move_loss)) #todo fix zero division error that occurs once in a while
                p.ai.model.save_model(p.get_model_name())#todo check if this works
                p.final_move_scores.append(sum(p.weighed_moves)/len(p.weighed_moves))
                stats.log_message(f"{p.TYPE} {p.id}: score loss: {float(p.ai.loss)}")
                stats.log_message(f"{p.TYPE} {p.id}: move loss: {sum(p.move_loss)/len(p.move_loss)}")
            p.reset_score()
            if self.last_round:
                if p.TYPE == "AI":
                    data[f"{p.TYPE} {p.id}: game accuracy"] = p.weighed_scores
                    data[f"{p.TYPE} {p.id}: move accuracy"] = p.final_move_scores
                    loss_data[f"{p.TYPE} {p.id}: score loss"] = [float(val) for val in p.score_loss]
                    move_loss_data[f"{p.TYPE} {p.id}: move loss"] = p.final_move_loss
                    stats.log_message(f"{p.TYPE} {p.id}: average score loss: {sum([float(val) for val in p.score_loss]) / len([float(val) for val in p.score_loss])}")
                    stats.log_message(f"{p.TYPE} {p.id}: average move loss: {sum(p.final_move_loss) / len(p.final_move_loss)}")
                p.reset_all_stats()
        
        if self.show_graphs:
            if len(data) > 0:
                stats.plot_graph(data, 'accuracy')
            if len(loss_data) > 0:
                stats.plot_graph(loss_data, 'loss data')
            if len(move_loss_data) > 0:
                stats.plot_graph(move_loss_data, 'loss data')


        
