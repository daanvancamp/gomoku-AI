import os.path
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque
from filereader import log_info_overruling

MAX_MEMORY = 1_000_0000          # origineel 1_000_000
BATCH_SIZE = 10_000
MIN_EPSILON = 0.01
EPSILON_DECAY_RATE = 0.999

class ConvNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(ConvNet, self).__init__()
        self.list_dropout_rates=[0.05,0.1,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
        # Define your CNN architecture here
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(3, hidden_dim, kernel_size=5, stride=1, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=5, stride=1),
            torch.nn.Dropout(p=self.list_dropout_rates[0]))
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(input_dim * input_dim, hidden_dim, kernel_size=5, stride=1, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=5, stride=1),
            torch.nn.Dropout(p=self.list_dropout_rates[1]))
        self.layer3 = torch.nn.Sequential(
            torch.nn.Conv2d(hidden_dim, output_dim, kernel_size=5, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=5),
            torch.nn.Dropout(p=self.list_dropout_rates[2]))

        self.fc2 = torch.nn.Linear(input_dim * input_dim, input_dim * input_dim, bias=True)
        self.conv1 = nn.Conv2d(in_channels=input_dim, out_channels=input_dim, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(in_channels=input_dim * input_dim, out_channels=input_dim * input_dim, kernel_size=5, padding=2)
        self.fc3 = nn.Linear(output_dim, input_dim, bias=False)
        self.fc1 = nn.Linear(output_dim, input_dim * input_dim)

    def forward(self, x):
        out = F.relu(self.layer1(x))
        out = F.relu(self.layer3(out))
        return out

    def load_model(self, folder,file_name='model.pth'):
        model_folder = './data/models/'+folder.strip()
        full_path = os.path.join(model_folder, file_name)
        print("Full path model:",full_path)
        if os.path.isfile(full_path):
            print("A model already exists, loading model...")
            self.load_state_dict(torch.load(full_path,weights_only=False))
        else:
            print("No model exists. Creating a new model.")

    def save_model(self, folder,file_name='model.pth'):
        model_folder = './data/models/'+folder.strip()
        file_name=file_name.strip()#remove \n from filename
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)
        full_path = os.path.join(model_folder, file_name)
        torch.save(self.state_dict(), full_path)
        print(f"Model saved to directory {full_path}.")


class GomokuAI:
    def __init__(self,_board_size=15):
        self.n_games = 0
        self.game = None
        self.learning_rate = 0.00075
        self.board_size = _board_size
        self.gamma = 0.2
        self.epsilon = 0.25
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = self.build_model(self.board_size)
        self.optimizer= optim.SGD(params=self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()
        self.loss = 0
        self.train = False
        self.allow_overrule = True
        self.current_player_id = None
        self.threat_moves =[]
        self.valid_moves = []
        self.overruled_last_move = False

    def decrease_learning_rate(self):
        self.learning_rate *= 0.9999 #decrease learning rate
        print("learning rate automatically declined by 0.001%, current lr:", self.learning_rate)
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = self.learning_rate

    def set_game(self, _game):
        self.game = _game

    def build_model(self, input_dim: int) -> ConvNet:#multi-layered network
        return ConvNet(input_dim, 30, 255)

    def get_state(self, game):
        return torch.tensor(game, dtype=torch.float32).unsqueeze(0)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def adjust_epsilon(self):
        if self.epsilon > MIN_EPSILON:
            self.epsilon *= EPSILON_DECAY_RATE

    def train_long_memory(self):
        self.model.train()
        if len(self.memory) < BATCH_SIZE:
            mini_batch = self.memory
        else:
            mini_batch = random.sample(self.memory, BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*mini_batch)
        # Convert to tensors
        states = torch.tensor(states, dtype=torch.float).unsqueeze(0) 
        rewards = torch.tensor(rewards, dtype=torch.float)
        q_pred = rewards
        q_target = rewards + (self.gamma * (~torch.tensor(dones)))
        # Loss and backpropagation
        loss = self.criterion(q_pred, q_target)
        loss.requires_grad_(requires_grad=True)
        loss.backward()
        self.loss = loss.detach().numpy()  # for logging purposes
        self.optimizer.step()
        self.adjust_epsilon()

    def train_short_memory(self, state, action, reward, scores, next_state, next_scores, done):
        self.model.train()
        state = torch.tensor(state, dtype=torch.float).unsqueeze(0)
        next_state = torch.tensor(next_state, dtype=torch.float).unsqueeze(0)
        reward = torch.tensor([reward], dtype=torch.float)
        q_pred = self.model(state)
        q_next = self.model(next_state)
        q_new = q_pred + self.learning_rate * (reward + self.gamma * torch.argmax(q_pred - q_next))

        loss = self.criterion(q_pred, q_new)
        loss.requires_grad_(requires_grad=True)
        loss.backward()
        self.loss = loss.detach().numpy()  # for logging purposes
        self.optimizer.step()
        self.optimizer.zero_grad(set_to_none=False)
    
    def set_allow_overrule(self, allow_overrule):
        self.allow_overrule = allow_overrule
        
    def remove_unvalid_moves(self):
        for move in self.threat_moves:
            if move not in self.valid_moves:
                self.threat_moves.remove(move)#remove unvalid moves
        if self.threat_moves:#if not threat_moves==[]
            print("overruled:", self.threat_moves)
            self.overruled_last_move = True
            return self.threat_moves
        else:
            print("no threat moves were valid moves, returning valid moves:the model will choose on its own")
            log_info_overruling("no threat moves were valid moves, returning valid moves: "+"the model will choose on its own")
            self.overruled_last_move = False
            return self.valid_moves

    def can_win_in_one_move(self, board)->list:
         log_info_overruling("function can_win_in_one_move called")
         winning_moves=[]
         directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
         current_player=self.current_player_id
         for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == 0:
        
                    for drow, dcol in directions:
                        count = 0  
                        open_ends = 0
                        adjacent_two = 0 
            
                        for i in range(1, 5):
                            r, c = row + i * drow, col + i * dcol
                            if 0 <= r < len(board) and 0 <= c < len(board):
                                if board[r][c] == current_player:
                                    count += 1
                                    if count == 2 and i == 2:
                                        adjacent_two += 1
                                elif board[r][c] == 0:
                                    open_ends += 1
                                    break
                                else:
                                    break
                            else:
                                break
            
                        for i in range(1, 5):
                            r, c = row - i * drow, col - i * dcol
                            if 0 <= r < len(board) and 0 <= c < len(board):
                                if board[r][c] == current_player:
                                    count += 1
                                    if count == 2 and i == 2:
                                        adjacent_two += 1
                                elif board[r][c] == 0:
                                    open_ends += 1
                                    break
                                else:
                                    break
                            else:
                                break
            
                        if  (count == 4 and open_ends >= 0) or adjacent_two == 2 or (count == 3 and open_ends >= 1):
                            winning_moves.append((row, col))
                            break
         if winning_moves:
            log_info_overruling("It will choose on its own, it can win in one move if it does the right move.")
            return True
         else:
            log_info_overruling("no winning moves found")
            return False

    def get_valid_moves(self, board)->list:
        log_info_overruling("\n\nfunction get_valid_moves called")
        log_info_overruling("the involved player is player " + str(self.current_player_id))
        opponent = 3 - self.current_player_id  # 3-2=1 and 3-1=2 Player 1 is a one in the list and player 2 is a 2 in the list.
        self.valid_moves = []
        self.threat_moves = []
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        overrule=self.allow_overrule #shorter variable name
    
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == 0:  # Lege cel
                    self.valid_moves.append((row, col))

                    for drow, dcol in directions:
                        count = 0  
                        open_ends = 0
                        adjacent_two = 0 
                        three_and_one_pattern = False
    
                        # Check in positive direction
                        for i in range(1, 5):
                            r, c = row + i * drow, col + i * dcol
                            if 0 <= r < len(board) and 0 <= c < len(board):
                                if board[r][c] == opponent:
                                    count += 1
                                    if count == 2 and i == 2:
                                        adjacent_two += 1
                                elif board[r][c] == 0:
                                    open_ends += 1
                                    # Check for xxx_x pattern
                                    if count == 3:
                                        for j in range(1, 3):
                                            rr, cc = r + j * drow, c + j * dcol
                                            if 0 <= rr < len(board) and 0 <= cc < len(board) and board[rr][cc] == opponent:
                                                three_and_one_pattern = True
                                                break
                                    break
                                else:
                                    break
                            else:
                                break
    
                        # Check in negative direction
                        for i in range(1, 5):
                            r, c = row - i * drow, col - i * dcol
                            if 0 <= r < len(board) and 0 <= c < len(board):
                                if board[r][c] == opponent:
                                    count += 1
                                    if count == 2 and i == 2:
                                        adjacent_two += 1
                                elif board[r][c] == 0:
                                    open_ends += 1
                                    # Check for x_xxx pattern
                                    if count == 3:
                                        for j in range(1, 3):
                                            rr, cc = r - j * drow, c - j * dcol
                                            if 0 <= rr < len(board) and 0 <= cc < len(board) and board[rr][cc] == opponent:
                                                three_and_one_pattern = True
                                                break
                                    break
                                else:
                                    break
                            else:
                                break
    
                        if (count == 3 and open_ends == 2) or (count == 4) or adjacent_two == 2 or three_and_one_pattern:
                            self.threat_moves.append((row, col))
                            log_info_overruling(f"player {opponent} has a threat at {row}, {col}")
                       
                            if adjacent_two == 2 or (count == 4) or three_and_one_pattern:
                                log_info_overruling(f"player {opponent} has a winning threat at {row}, {col}")
                                if adjacent_two == 2:
                                    log_info_overruling(f"player {opponent} has 2 times 2 in a row: xx_xx")
                                elif count == 4 and open_ends >= 0:
                                    log_info_overruling(f"player {opponent} has 4 in a row: _xxxx_")
                                elif three_and_one_pattern:
                                    log_info_overruling(f"player {opponent} has 3 in a row and 1 nearby: xxx_x or x_xxx")

                            break  # There's no need to search any further for this cell.
    
        if overrule and self.threat_moves and not self.can_win_in_one_move(board): #if threat_moves is not empty
            log_info_overruling("overruled: " + str(self.threat_moves))
            for row in board:
                log_info_overruling(str(row))
            log_info_overruling("status: an overruled move is executed by the AI")
            log_info_overruling("allow_overrule: " + str(self.allow_overrule))
            self.threat_moves=self.remove_unvalid_moves()
            return self.threat_moves
        else:
            print("a normal move is executed by the AI")
            for row in board:
                log_info_overruling(str(row))
            log_info_overruling("status: a normal move is executed by the AI")
            log_info_overruling("allow_overrule: " + str(self.allow_overrule))
            self.overruled_last_move = False
            return self.valid_moves

    def id_to_move(self, move_id, valid_moves):
        if move_id < len(valid_moves):
            return valid_moves[move_id]
        else:
            return None

    def get_action(self, state, one_hot_board, scores)->tuple:
        valid_moves = self.get_valid_moves(state)
        np_scores = np.array(scores).reshape(15, 15)
        current_state = torch.tensor(self.get_state(one_hot_board), dtype=torch.float)

        action = None
        with torch.no_grad():
            prediction = self.model(current_state)
        if random.random() < self.epsilon and self.train:
            # print("Exploration")
            num_moves_to_select = max(int(len(valid_moves) * .025), 1)
            if num_moves_to_select > 0:
                try:
                    top_moves_indices = torch.topk(prediction.flatten(), k=num_moves_to_select-1).indices
                    action = self.id_to_move(top_moves_indices[torch.randint(len(top_moves_indices), (1,))].item(), valid_moves)
                except RuntimeError:
                    action = None
        else:
            # print("Exploitation")
            pred_possible_moves = int(torch.max(prediction))
            pred_indices = np.where(np_scores == pred_possible_moves)
            if len(pred_indices[0]) > 0:
                idx = random.randint(0, len(pred_indices[0])-1)
                if (pred_indices[0][idx], pred_indices[1][idx]) in valid_moves:
                    action = (pred_indices[0][idx], pred_indices[1][idx])
            else:
                action = None
        attempts=0
        max_attempts=70
        while action is None:
            attempts+=1
            if attempts>max_attempts:
                  action = random.choice(valid_moves) #form: (x,y), move is completely random after max_attempts
                  if action is None:
                      raise Exception("A random move couldn't be found")
                  print("move not found, random move chosen")
                 
            # if no action, switch to exploration
            else:
                #print("Exploration") #this is the one that I commented out, the rest should be commented out. ###
                action = self.id_to_move(self.get_random_action(state), valid_moves)
        # Decay Epsilon Over Time
        self.adjust_epsilon()
        return action

    def get_random_action(self, board):
        while True:
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board) - 1)
            if board[row][col] == 0:
                p = (row % (len(board) - 1) * len(board)) + (col + 1)
                break
        return p

    def convert_to_one_hot(self, board, player_id):#vermijd dat ai denkt dat de getallen iets betekenen.
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

    def calculate_short_score(self, move: tuple, board: tuple, max_score_calculation=False):
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

    def calculate_short_max_score(self, board: tuple, board_size=15):
        moves = []
        for row in range(board_size):
            for col in range(board_size):
                score = self.calculate_short_score((row, col), board, True)
                moves.append(score)
                if score > 0:
                    print(f"score: {score}, location: {row}, {col}")
        moves_normalized = []
        for i in range(len(moves)):
            if max(moves) > 0:
                new_normalized_move = (moves[i] / (max(moves) / 2) - 1)
            else:
                new_normalized_move = 0
            if new_normalized_move < 0:
                new_normalized_move = 0
            moves_normalized.append(new_normalized_move)
        print(f"best score: {max(moves)}")
        np_moves_norm = np.array(moves)
        reshaped = np.reshape(np_moves_norm, (board_size, board_size))
        return max(moves), moves, moves_normalized
