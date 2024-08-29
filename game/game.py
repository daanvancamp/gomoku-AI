from . import player
from . import gameboard

class Game:
    def  __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board =board


class GameFactory:
    def create_player(player_type, player_id): 
        if player_type == "AI":
            return player.AI_Player(player_id)
        elif player_type == "Test":
            return player.AI_Player(player_id)
        else: 
            return player.Human_Player(player_id)
    
    def create_game_board(grid_size):
        return gameboard.GameBoard(grid_size)

    def create_game(game_board, player1, player2):
        return Game(player1, player2, game_board)