from players import *
import numpy as np
import operator

class GameBoard:
    def  __init__(self, grid_size):
        self.board = np.zeros((grid_size, grid_size))
        self.winning_cells = None
        self.grid_size = grid_size
    
    def check_win(self, row, col, player_id):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for drow, dcol in directions:
            winning_cells = [(row, col)]
            winning_direction = ()
            count = 1
            # positive direction
            for i in range(1, 5):
                row_, col_ = row + i * drow, col + i * dcol
                if 0 <= row_ < self.grid_size and 0 <= col_ < self.grid_size and self.board[row_][col_] == player_id:
                    count += 1
                    winning_cells.append((row_, col_))
                    winning_direction = [(drow, dcol)]
                else:
                    break
            # negative direction
            for i in range(1, 5):
                row_, col_ = row - i * drow, col - i * dcol
                if 0 <= row_ < self.grid_size and 0 <= col_ < self.grid_size and self.board[row_][col_] == player_id:
                    count += 1
                    winning_cells.append((row_, col_))
                    winning_direction = (drow, dcol)
                else:
                    break
            if count >= 5:  # Victory condition 
                match winning_direction:    # sort the array so that a strike can be drawn correctly
                    case (1, 0): #if winning_direction==(1,0):
                        winning_cells.sort()
                    case(0, 1):#if winning_direction==(0,1):
                        winning_cells.sort(key=lambda i: i[1])
                    case(1, 1):#if winning_direction==(1,1):
                        winning_cells.sort(key=operator.itemgetter(0, 1))
                    case(1, -1):#if winning_direction==(1,-1):
                        winning_cells.sort(key=operator.itemgetter(0, 1), reverse=True)
                self.winning_cells = winning_cells
                return True
        return False
    
    def check_board_full(self, marker_id):
        pass


class Game:
    def  __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board =board

class GameFactory:
    def create_player(player_type, player_id): 
        if player_type == "AI":
            return AI_Player(player_id)
        elif player_type == "Test":
            return AI_Player(player_id)
        else: 
            return Human_Player(player_id)
    
    def create_game_board(grid_size):
        return GameBoard(grid_size)

    def create_game(game_board, player1, player2):
        return Game(player1, player2, game_board)