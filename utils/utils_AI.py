import numpy as np
import utils.filereader
class Utils_AI:
    def __init__(self):
        pass
    def convert_to_one_hot(self,board, player_id):
        board = np.array(board)
        height, width = board.shape
        one_hot_board = np.zeros((3, height, width), dtype=np.float32)
        one_hot_board[0] = (board == 0).astype(np.float32)
        if player_id == 1:
            one_hot_board[1] = (board == 1).astype(np.float32)  # AI's pieces as Player 1
            one_hot_board[2] = (board == 2).astype(np.float32)  # Enemy's pieces as Player 2
        else:
            one_hot_board[1] = (board == 2).astype(np.float32)  # AI's pieces as Player 2
            one_hot_board[2] = (board == 1).astype(np.float32)
        return one_hot_board
    
    def calculate_score(self,board, board_size=15):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        score_board = utils.filereader.load_scores("./configuration/consts.json")
        scored_board = np.zeros((board_size, board_size))
        for row in range(len(board[0])):
            for col in range(len(board[1])):
                adjacent_tiles = {}
                tiles = {}
                if board[row][col] == 0:
                    for i in range(len(directions)):
                        forward = []
                        for j in range(5):
                            try:
                                forward.append(board[row + ((j + 1) * directions[i][0])][col + ((j + 1) * directions[i][1])])
                            except IndexError:
                                break
                        tiles[directions[i]] = forward
                    adjacent_tiles[(row, col)] = tiles
                else:
                    adjacent_tiles[(row, col)] = -1
                total_score = 0
                try:
                    for id, values in adjacent_tiles.items():
                        directions = list(values.keys())
                        for i in range(0, len(directions), 2):  # Iterate in pairs (opposing directions)
                            dir1, dir2 = directions[i], directions[i + 1]
                            line1, line2 = values[dir1], values[dir2]
                            score1 = 0
                            score2 = 0
                            first = 0
                            # Convert line so that the first non-zero cell is 1 and any opposing non-zero number is 2
                            for j in range(len(line1)):
                                try:
                                    if first == 0 and line1[j] > 0:
                                        first = line1[j]
                                    if line1[j] > 0:
                                        if line1[j] == first:
                                            line1[j] = 1
                                        else:
                                            line1[j] = 2
                                except IndexError:
                                    break
                            first = 0
                            for k in range(len(line2)):
                                try:
                                    if first == 0 and line2[k] > 0:
                                        first = line2[k]
                                    if line2[k] > 0:
                                        if line2[k] == first:
                                            line2[k] = 1
                                        else:
                                            line2[k] = 2
                                except IndexError:
                                    break
                            lines = [str(line1), str(line2)]
                            for category in score_board:
                                for key in category.keys():
                                    for item in category[key]:
                                        for l in range(len(lines)):
                                            if lines[l] in item:
                                                if l == 0:
                                                    score1 += item[lines[l]]
                                                else:
                                                    score2 += item[lines[l]]
                            if score1 > 0 and score2 > 0:
                                total_score += (score1 + score2)
                            else:
                                total_score += (score1 + score2)
                except AttributeError:
                    total_score = -1
                scored_board[row][col] = total_score
        scores_normalized = []
        max_score = int(np.amax(scored_board))
        scored_board_flat = scored_board.flatten()
        # normalize the score for ai training purposes
        for i in range(len(scored_board_flat)):
            new_normalized_score = 0
            if max_score > 0:
                new_normalized_score = (scored_board_flat[i] / (max_score / 2) - 1)
            if new_normalized_score < 0:
                new_normalized_score = 0
            scores_normalized.append(new_normalized_score)
        return max_score, scored_board, scores_normalized#return de hoogste score, het board met scores, de scores genormaliseerd
