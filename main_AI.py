from time import time
import game.game
import ui.main_window
from configuration.config import *
import game.player
import numpy as np
import logging
import unittest
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F



class TestGomoku(unittest.TestCase):
    def test_model1(self):
        self.player1 = game.player.AI_Player(1)
        self.player2 = game.player.AI_Player(2)    
        self.player2.load_model("standard-Mikko")
        self.game_board = game.game.GameFactory.create_game_board(15)
        
        self.game_board.board[1][1]=1
        self.game_board.board[2][1]=1       
        self.game_board.board[3][1]=1
        self.game_board.board[4][1]=1

        self.game_board.board[3][8]=2
        self.game_board.board[4][7]=2       
        self.game_board.board[9][3]=2
        self.game_board.board[10][10]=2        

        self.game = game.game.GameFactory.initialize_new_game(self.game_board, self.player1, self.player2)
        self.player1.ai.board = self.game_board.board
        self.player1.ai.current_player_id = 1
        self.player1.ai.convert_to_one_hot()
        current_state = torch.tensor(self.player1.ai.get_state(self.player1.ai.one_hot_board), dtype=torch.float)
        print(f"The shape of the state is {current_state.shape}")
        print(current_state)

        with torch.no_grad():
            prediction = self.player1.ai.model(current_state)
            print(f"The shape of the prediction is {prediction.shape}")
            torch.set_printoptions(threshold=float('inf'))
            print(prediction)
            print(torch.max(prediction))
        
        max_score, scores, scores_normalized = self.player1.ai.calculate_score()
        action =  self.player1.ai.get_action(scores_normalized)
        np_scores = np.array(scores).reshape(15, 15)
        print(np_scores)
        print(scores_normalized)
        print(action)
            
if __name__ == '__main__':
    # Load and run only the 'test_add' method
    suite = unittest.TestSuite()
    suite.addTest(TestGomoku('test_model1'))
    runner = unittest.TextTestRunner()
    runner.run(suite)




