from functools import lru_cache
import game.algorithms.test_algorithm.TestAlgorithm
from game.algorithms.ai.ai import AI_Algorithm
import game.game
from configuration.config import config
from model_management.AI_model import AI_Model

import logging

# Use the existing logger by name
logger = logging.getLogger('my_logger')

class Player:
    def __init__(self, player_id,playertype):
        self.TYPE = playertype
        self.id = int(player_id) #id can be 1 or 2
        self.moves = 0
        self.wins = 0
        self.losses = 0
        self.score = 0
        self.sum_score = 0
        self.avg_score = 0
        self.all_moves = []
        self.avg_moves = 0
        self.weighed_scores = []
        self.score_loss = []
        self.weighed_moves = []
        self.move_loss = []
        self.final_move_scores = []
        self.final_move_loss = []
        self.win_rate = 0
        self.allow_overrule = True
        self.final_action = None
        self.game = None

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if self.TYPE =="human":
            return f"Player {self.id}: {self.TYPE}  "
        return f"Player {self.id}: {self.TYPE}"

    def calculate_score(self, max_score, is_winner, game_number):
        print(game_number+1)
        if max_score > 0:
            if is_winner:
                self.score = (max_score - self.moves) / max_score
            else:
                self.score = -((max_score - self.moves) / max_score)
            # weighed_score = self.score / max_score
            self.weighed_scores.append(self.score)
        else:
            self.score = 0
            self.weighed_scores.append(0)
        print(f"score: {self.score}")
        self.sum_score += self.score
        self.avg_score = self.sum_score / (game_number+1)
        self.all_moves.append(self.moves)
        self.avg_moves = sum(self.all_moves) / len(self.all_moves)

    def calculate_win_rate(self, rounds):
        self.win_rate = self.wins / rounds

    def reset_score(self):
        self.score = 0
        self.moves = 0
        self.weighed_moves = []
        self.move_loss = []

    def reset_all_stats(self): #purely for testing purposes
        self.moves = 0
        self.wins = 0
        self.losses = 0
        self.score = 0
        self.sum_score = 0
        self.avg_score = 0
        self.weighed_scores = []
        self.score_loss = []
        self.all_moves = []
        self.weighed_moves = []
        self.move_loss = []
        self.final_move_scores = []
        self.final_move_loss = []
        self.avg_moves = 0


class AI_Player(Player):
    def __init__(self, player_id):
        super().__init__(player_id,"AI")  # Call the constructor of the base class
        self.ai = AI_Algorithm(int(config["OTHER VARIABLES"]["BOARDSIZE"]))
        self.ai.train = False

    def load_model(self, model):
        self.ai.load_model(model) 

    def get_model_name(self):
        return self.AI_model.modelname
        
    def set_allow_overrule(self, allow_overrule):
        self.allow_overrule = allow_overrule
        self.ai.set_allow_overrule(allow_overrule)#ai=GomokuAI


@lru_cache(maxsize=None)
class Human_Player(Player):
    def __init__(self, player_id):    
        super().__init__(player_id,"Human")  # Call the constructor of the base class


@lru_cache(maxsize=None)
class Test_Player(Player):
    def __init__(self, player_id):    
        super().__init__(player_id,"Test")  # Call the constructor of the base class
        self.test_algorithm = game.algorithms.test_algorithm.TestAlgorithm.TestAlgorithm(self)