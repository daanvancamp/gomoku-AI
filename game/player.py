from functools import lru_cache
import game.algorithms.test_algorithm.TestAlgorithm
from NN.ai import GomokuAI
import game.game
from configuration.config import config

class Player:
    def __init__(self, player_id):
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
        return f"{self.__class__.__name__}({self.id})"
@lru_cache(maxsize=None)
class AI_Player(Player):
    def __init__(self, player_id):    
        super().__init__(player_id)  # Call the constructor of the base class
        self.AI_model=None
        self.ai=GomokuAI(int(config["OTHER VARIABLES"]["BOARDSIZE"]))

 
@lru_cache(maxsize=None)
class Human_Player(Player):
    def __init__(self, player_id):    
        super().__init__(player_id)  # Call the constructor of the base class

@lru_cache(maxsize=None)
class Test_Player(Player):
    def __init__(self, player_id):    
        super().__init__(player_id)  # Call the constructor of the base class
        self.test_algorithm = game.algorithms.test_algorithm.TestAlgorithm.TestAlgorithm(self)