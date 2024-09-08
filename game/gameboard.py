import numpy as np
import operator

class GameBoard:
    def  __init__(self, grid_size):
        self.board = np.zeros((grid_size, grid_size))
        self.winning_cells = None
        self.grid_size = grid_size
        self.board_size = self.grid_size
    
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
    
    def put_piece(self, row, col, player_id):
        self.board[row][col] = player_id

    def square_empty(self, row, col):
        return self.board[row][col] == 0
        
    def remove_piece(self, row, col):
        self.board[row][col] = 0

    def check_board_full(self, marker_id):
        pass
    


    def calculate_short_score(self, player_id : int, move: tuple, board: tuple, max_score_calculation=False):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]
        score = 0
        first_spot = None
        try:
            for i in range(len(directions)):
                current_score = 0
                for j in range(5):
                    current_spot = board[move[0] + ((j + 1) * directions[i][0])][move[1] + ((j + 1) * directions[i][1])]
                    if j == 0:
                        first_spot = current_spot
                    if not max_score_calculation:
                        # if current_spot == 1 or current_spot == 2:  # run only if current spot is not empty
                        if current_spot > 0:
                            print(
                                f"current spot: {current_spot}. Location: ({move[0] + ((j + 1) * directions[i][0])}, {move[1] + ((j + 1) * directions[i][1])})")
                            if first_spot is not None:
                                current_score += self.calculate_score(current_score, move, board, current_spot, j,
                                                                      directions[i], first_spot)
                            else:
                                current_score += self.calculate_score(current_score, move, board, current_spot, j,
                                                                      directions[i])
                        else:
                            pass
                    elif max_score_calculation:
                        if board[move[0]][move[1]] != 0:
                            current_score = -1
                            break
                        else:
                            if first_spot != None:
                                current_score = self.calculate_score(current_score, move, board, current_spot, j,
                                                                     directions[i], first_spot)
                            else:
                                current_score = self.calculate_score(current_score, move, board, current_spot, j,
                                                                     directions[i])
                    else:
                        pass  # exit immediately if hits an empty spot and not max score count
                score += current_score
        except IndexError:
            pass
        if max_score_calculation and score < -1:
            score = -1  # clamp max score calculation min value to -1, which represents a non-valid move
        return score

    def calculate_score(self, current_score, move, board, current_spot, j, direction: tuple, first_spot=-1) -> int:
        score = 0
        previous_spot = board[move[0] + ((j - 1) * direction[0])][move[1] + ((j - 1) * direction[1])]
        if current_spot == previous_spot:
            if first_spot > 0:
                if current_score > 0:
                    score = current_score * (
                                j + 1)  # increase score if the current and previous spots are of the same color
                else:
                    score = j + 1
        else:
            if first_spot > 0:  # a situation where a line is blocked
                for k in range(3):  # check opposing direction for continuation
                    opposing_spot = board[move[0] - ((j + 1) * direction[0])][move[1] - ((j + 1) * direction[1])]
                    if opposing_spot != 0 and opposing_spot == first_spot:
                        score = current_score * (
                                    k + 1)  # increase score if opposing direction has the same color as the first spot of the current direction
                    elif opposing_spot != 0 and opposing_spot != first_spot:
                        if (j + 1) + (
                                k + 1) <= 4:  # if the lines are too short and blocked from both sides, don't reward
                            score = 0
            else:
                pass
        return score


    def calculate_scoreboard(self, player_id: int, board: tuple, board_size=15):
        scoreboard = np.zeros((board_size, board_size))
        for row in range(board_size):
            for col in range(board_size):
                scoreboard[row][col] = self.calculate_short_score(player_id, (row, col), board, True)
        return scoreboard

