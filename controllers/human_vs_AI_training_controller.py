import game.game
import ui.main_window
from . import controller
from configuration.config import *
import numpy as np
import game.algorithms.ai.ai
import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Human_vs_AI_Training_Controller(controller.BaseController):
    def __init__(self, view: "ui.main_window.GomokuApp",color_human):
        super().__init__(view)
        self.last_move_model=None
        logger.info("Initialize Human_vs_AI_Training_Controller")
        if color_human=="red": #red always plays first
            player1 = game.game.GameFactory.create_player("Human", 1)
            player2 = game.game.GameFactory.create_player("AI", 2)
            self.AI_player=player2
        else:
            player1 = game.game.GameFactory.create_player("AI", 1)
            player2 = game.game.GameFactory.create_player("Human", 2)
            self.AI_player=player1

        self.AI_player.load_model("standaard+3000")

        game_board = game.game.GameFactory.create_game_board(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.game:game.game.Game = game.game.GameFactory.initialize_new_game(game_board, player1, player2)
        self.initialize_board()

        self.view.window_mode = ui.main_window.WindowMode.human_move
        self.view.activate_game()

        self.record_replay = True
        self.mark_last_move_model = True

        if color_human!="red":
            self.AI_put_piece()
        
    def human_put_piece(self, row, col):
        logger.info("Human move")       

        if self.game.put_piece(row, col):
            self.view.draw_pieces(self.game.board.board)
            if not self.check_and_handle_winner():
                self.AI_put_piece()

                if self.check_and_handle_winner():
                    ...
            else:
                ...#todo finish this

    def AI_put_piece(self):
        logger.info("AI move")             
        
        gomoku_ai:game.algorithms.ai.ai.AI_Algorithm = self.game.current_player.ai
        gomoku_ai.board = self.game.board.board
        gomoku_ai.current_player_id = self.game.current_player.id
        
        old_state= self.game.board.board
        one_hot_board= gomoku_ai.convert_to_one_hot()
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

        

        row, col = action
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board)

        next_max_score, next_scores, next_scores_normalized = gomoku_ai.calculate_score(15)

        gomoku_ai.remember(old_state, action, score,self.game.board.board ,self.game.winner!=0 ) #todo how to get the variable to this line?
        gomoku_ai.train_short_memory(one_hot_board, action, short_score, scores, gomoku_ai.convert_to_one_hot(),next_scores,self.game.winner!=0)
        self.game.players[self.game.current_player.id - 1].move_loss.append(gomoku_ai.loss)

        self.game.current_player.weighed_moves.append(score)
        self.game.current_player.final_action = action
        self.game.current_player.moves += 1

    def train_at_the_end_of_the_round(self):
        data = {}
        loss_data = {}
        move_loss_data = {}
        for p in self.game.players:
            if p.TYPE == "MM-AI":
                p.ai.remember(self.game.board.board, p.final_action, p.score, self.game.board.board, True)
                p.ai.train_long_memory()
                p.score_loss.append(p.ai.loss)
                move_loss = [float(val) for val in p.move_loss]
                p.final_move_loss.append(sum(move_loss)/len(move_loss))
                p.ai.model.save_model()
                p.final_move_scores.append(sum(p.weighed_moves)/len(p.weighed_moves))
                # stats.log_message(f"{p.TYPE} {p.ID}: score loss: {float(p.ai.loss)}")
                # stats.log_message(f"{p.TYPE} {p.ID}: move loss: {sum(p.move_loss)/len(p.move_loss)}")
            p.reset_score()
            if self.last_round:
                if p.TYPE == "MM-AI":
                    data[f"{p.TYPE} {p.ID}: game accuracy"] = p.weighed_scores
                    data[f"{p.TYPE} {p.ID}: move accuracy"] = p.final_move_scores
                    loss_data[f"{p.TYPE} {p.ID}: score loss"] = [float(val) for val in p.score_loss]
                    move_loss_data[f"{p.TYPE} {p.ID}: move loss"] = p.final_move_loss
                    # stats.log_message(f"{p.TYPE} {p.ID}: average score loss: {sum([float(val) for val in p.score_loss]) / len([float(val) for val in p.score_loss])}")
                    # stats.log_message(f"{p.TYPE} {p.ID}: average move loss: {sum(p.final_move_loss) / len(p.final_move_loss)}")
                p.reset_all_stats()
        # if len(data) > 0:
        #     stats.plot_graph(data, 'accuracy')
        # if len(loss_data) > 0:
        #     stats.plot_graph(loss_data, 'loss data')
        # if len(move_loss_data) > 0:
        #     stats.plot_graph(move_loss_data, 'loss data')
