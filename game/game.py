from . import player
from . import gameboard
from utils.singleton_class import Singleton
class Game(metaclass=Singleton):
    def initialize_game(self, player1, player2, board:gameboard.GameBoard):
        self.player1 = player1
        self.player2 = player2
        self.players=[self.player1,self.player2]
        self.current_player = player1
        self.board = board
        self.winner = 0
        self.current_game = 0
        self.last_round = False

        self.p1_moves = []
        self.p2_moves = []

    def put_piece(self, row, col) -> bool:
        if self.board.square_empty(row, col):
            self.board.put_piece(row, col, self.current_player.id)
        else:
            return False

        if self.board.check_win(row, col, self.current_player.id):
            self.winner = self.current_player.id
        else:
            self.switch_player()
        return True
    
    def switch_player(self):
        if self.current_player.id == 1:
            self.current_player = self.player2
        else: 
            self.current_player = self.player1
   

class GameFactory:
    def create_player(player_type, player_id):
        match player_type:
            case "AI":
                return player.AI_Player(player_id)
            case "Test":
                return player.Test_Player(player_id)
            case _:
                return player.Human_Player(player_id)
    
    def create_game_board(grid_size):
        return gameboard.GameBoard(grid_size)

    def initialize_new_game(game_board:gameboard.GameBoard, player1, player2):
        game = Game()
        game.initialize_game(player1, player2, game_board)#it is a singleton class
        return game