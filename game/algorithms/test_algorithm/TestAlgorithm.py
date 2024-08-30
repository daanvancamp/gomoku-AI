import random

class TestAlgorithm:
    def  __init__(self, player):
        self.player = player
        self.DEPTH = 5
        self.board = None
    
    def check_line(self, row, col, direction):
        score_white = score_black = previous = 0
        multiplier = 1
        adjacency_loss = 1
        for i in range(self.DEPTH-1):
            board_score = self.board[row + (direction[0] * (i + 1))][col + (direction[1] * (i + 1))]
            try:
                if board_score != 0:
                    if previous == board_score:
                        multiplier *= (1 + multiplier)
                    else:
                        multiplier = 1
                        score_white /= 2
                        score_black /= 2
                    if board_score == 1:    # black piece
                        if self.player.id == 0:
                            score_white += 5 * multiplier - i
                        elif self.player.id == 1:
                            score_black += 2 * multiplier - i
                            if i >= 3 and multiplier > 3:
                                score_black **= 2
                                break
                    elif board_score == 2:  # white piece
                        if self.player.id == 0:
                            score_black += 5 * multiplier - i
                        elif self.player.id == 1:
                            score_white += 2 * multiplier - i
                            if i >= 3 and multiplier > 3:
                                score_white **= 2
                                break
                    previous = board_score
                elif i == 0:
                    adjacency_loss *= 8
                elif i > 1 and multiplier > 3:
                    adjacency_loss /= 2
            except IndexError:
                break
        try:
            if self.board[row + direction[0]][col + direction[1]] != 0:
                # increase the score if there is the same piece on the opposing direction
                board_piece = self.board[row + direction[0]][col + direction[1]]
                test_piece = self.board[row - direction[0]][col - direction[1]]
                if board_piece == test_piece:
                    for j in range(self.DEPTH-1):
                        try:
                            current_piece = self.board[row + (direction[0] * (j+1))][col + (direction[1] * (j+1))]
                            if current_piece == 1 and current_piece == board_piece:
                                score_black *= ((j+1)*2)
                                adjacency_loss /= 2
                            if current_piece == 2 and current_piece == board_piece:
                                score_white *= ((j+1)*2)
                                adjacency_loss /= 2
                            else:
                                if j == 0:
                                    score_white /= 2
                                    score_black /= 2
                                break
                        except IndexError:
                            break
        except IndexError:
            pass
        score_white = score_white / adjacency_loss
        score_black = score_black / adjacency_loss
        return int(score_white), int(score_black)


    def evaluate_board(self):
        scores = {}
        board = self.board
        grid_size = 15
        directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]
        for row in range(grid_size):
            for col in range(grid_size):
                if board[row][col] != 0:
                    pass
                else:
                    score_own = score_enemy = 0
                    try:
                        for i in range(len(directions)):
                            score_own_, score_enemy_ = self.check_line(row, col, directions[i])
                            score_own += score_own_
                            score_enemy += score_enemy_
                    except IndexError:
                        pass
                    if score_own > score_enemy:
                        score = score_own
                    else:
                        score = score_enemy
                    if score < 0:
                        score = 0
                    scores[(row, col)] = score
        return scores


    def make_move(self, move):
        row, col = move
        self.board[row][col] = self.player.id


    def get_available_moves(self):
        moves = []
        for row in range(15):
            for col in range(15):
                 if self.board[row][col] == 0:
                     moves.append((row, col))
        return moves


    def check_game_over(self):
        for row in range(15):
            for col in range(15):
                if self.board[row][col] == 0:
                    return False
        return True
    

    def ai_move(self):
        self.board = self.player.game.board.board
        moves = self.get_available_moves()
        scores = self.evaluate_board()
        max_score = max(scores.values())
        try:
            best_move = random.choice([k for k,v in scores.items() if v == max_score])
        except IndexError:
            best_move = random.choice(moves)
        return best_move
