import os.path
from math import isclose
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque
import operator

MAX_MEMORY = 1_000_0000          # origineel 1_000_000
BATCH_SIZE = 10_000
MIN_EPSILON = 0.01
EPSILON_DECAY_RATE = 0.999

#moeilijkheidsgraad is vermeld iedere keer.
#todo: Verbeteringen aanbrengen in het model door een complexere neurale netwerkarchitectuur te implementeren.:zeer moeilijk
#todo: Een aanpasbare leerfactor introduceren om de precisie van het leren te verbeteren. concreet: learn rate verlagen naarmate het trainen vordert.:matig
#De optimalisatiefunctie is veranderd van Adam naar SGD om de voorspelnauwkeurigheid te verhogen.:zeer eenvoudig
#todo: Experimenteren met genetische algoritmes om de optimale modelparameters te ontdekken.:zeer moeilijk
#todo: Meer tijd besteden aan het trainen van complexere netwerken om hun effectiviteit te testen. :??? lees conclusie finse student in detail


class ConvNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(ConvNet, self).__init__()
        # Define your CNN architecture here
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(3, hidden_dim, kernel_size=5, stride=1, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=5, stride=1),
            torch.nn.Dropout(p=0.05))
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(input_dim * input_dim, hidden_dim, kernel_size=5, stride=1, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=5, stride=1),
            torch.nn.Dropout(p=0.1))
        self.layer3 = torch.nn.Sequential(
            torch.nn.Conv2d(hidden_dim, output_dim, kernel_size=5, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=5),
            torch.nn.Dropout(p=0.2))
        self.fc2 = torch.nn.Linear(input_dim * input_dim, input_dim * input_dim, bias=True)
        self.conv1 = nn.Conv2d(in_channels=input_dim, out_channels=input_dim, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(in_channels=input_dim * input_dim, out_channels=input_dim * input_dim, kernel_size=5, padding=2)
        self.fc3 = nn.Linear(output_dim, input_dim, bias=False)
        self.fc1 = nn.Linear(output_dim, input_dim * input_dim)

    def forward(self, x):
        out = F.relu(self.layer1(x))
        out = F.relu(self.layer3(out))
        return out

    def load_model(self, file_name='model.pth'):
        model_folder = './data/'
        full_path = os.path.join(model_folder, file_name)
        if os.path.isfile(full_path):
            print("A model already exists, loading model...")
            print("Wanneer je het model traint, wordt het model bijgewerkt.")
            self.load_state_dict(torch.load(full_path))
        else:
            print("No model exists. Creating a new model.")

    def save_model(self, file_name='model.pth'):
        model_folder = './data/'
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)
        full_path = os.path.join(model_folder, file_name)
        torch.save(self.state_dict(), full_path)
        print(f"Model saved to directory {full_path}.")


class GomokuAI:
    def __init__(self, _board_size=15):
        self.n_games = 0
        self.game = None
        self.learning_rate = 0.00075
        self.board_size = _board_size
        self.gamma = 0.2
        self.epsilon = 0.25
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = self.build_model(self.board_size)
        #self.optimizer = optim.Adam(params=self.model.parameters(), lr=self.learning_rate) #veranderd naar SGD
        self.optimizer= optim.SGD(params=self.model.parameters(), lr=self.learning_rate)

        self.criterion = nn.MSELoss()
        self.loss = 0
        self.train = False
    def decrease_learning_rate(self):
        self.learning_rate *= 0.99 #decrease learning rate
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = self.learning_rate

    def set_game(self, _game):
        self.game = _game

    def build_model(self, input_dim: int) -> ConvNet:
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
        states = torch.tensor(states, dtype=torch.float).unsqueeze(0)  # .unsqueeze(0)
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

    def get_valid_moves(self, board):#voeg de nodige parameters toe. #returns list of valid moves (overroelen ai kan hier gebeuren door de lijst met lengte 1 te maken.) 
        #TODO: overroel AI
        valid_moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    valid_moves.append((row, col))
        return valid_moves
        '''directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for drow, dcol in directions:
            winning_cells = [(row, col)]
            winning_direction = ()
            count = 1
            # positive direction
            for i in range(1, 5):
                row_, col_ = row + i * drow, col + i * dcol
                if 0 <= row_ < instance.GRID_SIZE and 0 <= col_ < instance.GRID_SIZE and instance.board[row_][col_] == player:
                    count += 1
                    winning_cells.append((row_, col_))#cellen van tegenstander (meerdere naast elkaar)
                    winning_direction = [(drow, dcol)]
                    if i=1:
                        eerste_stuk_p=(row_,col_)
                    elif i=5:
                        laatste_stuk_p=(row_col_)
                    
                    
                else:
                    break
            # negative direction
            for i in range(1, 5):
                row_, col_ = row - i * drow, col - i * dcol
                if 0 <= row_ < instance.GRID_SIZE and 0 <= col_ < instance.GRID_SIZE and instance.board[row_][col_] == player:
                    count += 1
                    winning_cells.append((row_, col_))#cellen van tegenstander meerdere naast elkaar
                    winning_direction = (drow, dcol)
                    if i=1:
                        eerste_stuk_n=(row_,col_)
                    elif i=5:
                        laatste_stuk_n=(row_col_)
                else:
                    break
            if count == 3:
                valid_moves=              #enkel de 2 naburige cellen mogen gekozen worden door het model. #laat ai kiezen wanneer er meerdere keer 3 op een rij is
            elif count==4:
                valid_moves=              #enkel de naburige cel mag gekozen worden door het model.
            else: #laat de ai doen. Doe zoals normaal omdat er geen speler is die kan winnen als men niets doet.(De andere speler heeft geen 3 of 4 op een rij.)
                valid_moves = []
                for row in range(len(board)):
                    for col in range(len(board[row])):
                        if board[row][col] == 0:
                            valid_moves.append((row, col))
        


        return valid_moves'''

    def id_to_move(self, move_id, valid_moves):
        if move_id < len(valid_moves):
            return valid_moves[move_id]
        else:
            return None

    def get_action(self, state, one_hot_board, scores):
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
        attempts=0#initialiseer
        max_attempts=70 #todo:test dit
        while action is None:#Het programma blijft hier hangen!!!
            attempts+=1
            if attempts>max_attempts:
                  action = random.choice(valid_moves) #vorm: (x,y)
                  if action is None:
                      raise Exception("A random move couldn't be found")
                  print("move not found, random move chosen")
                  #stop na 3O pogingen #todo: controleer werking
                  #break
            # if no action, switch to exploration
            else:
                print("Exploration")
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
