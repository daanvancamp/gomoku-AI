import operator
import os
import time
from tkinter import Button, Frame, IntVar, Label, Tk,messagebox as mb,StringVar
import cv2
from PIL import Image, ImageTk 
import pygame
from AI_model import AI_Model
from music import start_music_delayed
import testai
import ai
import random
import stats
import numpy as np
import filereader
from threading import Thread
from detect_pieces import *

window_name = "Gomoku"
victory_text = ""
mark_last_move_model = True

class GomokuGame:
    def __init__(self, values):
        self.GRID_SIZE = values[1]
        self.WIDTH = self.HEIGHT = self.GRID_SIZE * values[0]
        self.CELL_SIZE = self.WIDTH // self.GRID_SIZE
        self.P1COL = values[2]
        self.P2COL = values[3]
        self.BOARD_COL = values[4]
        self.LINE_COL = values[5]
        self.SLEEP_BEFORE_END = values[6]
        self.board = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)] # 0 = empty, 1 = player 1, 2 = player 2. De waarden corresponderen aan de kleuren.
        self.screen = None #embedding isn't possible when defined here
        self.winning_cells = []
        self.current_game = 0
        self.last_round = False
        self.ai_delay = False
        self.use_recognition=False
        self.play_music = False
        self.show_overruling = False
        self.show_hover_effect = None
        self.record_replay=False
        self.show_graphs=False
        self.GUI=None
        self.running=None
        self.stop_game=False
        self.quit_program=False
        self.show_dialog=False
        self.skip_current_round = False
        self.game_modes=["Play Game","Training","Replay"]

        
    def set_board(self, board):
        self.board = board


class Player:
    def __init__(self, player_type, player_id):    
        #Initialize a Player object with the given player type and ID.
        self.TYPE = str(player_type) #type can be human, testai or AI-Model
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
        self.ai = ai.GomokuAI()
        self.AI_model=None
        
    def __str__(self) -> str:
        if self.TYPE =="human":
            return f"Player {self.id}: {self.TYPE}  "
        return f"Player {self.id}: {self.TYPE}"

    def calculate_score(self, max_score, is_winner, game_number):
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
        self.avg_score = self.sum_score / game_number+1
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
        
    def load_model(self, model):
        self.AI_model = AI_Model(model,self.ai.train)
        self.ai.model.load_model(model)

    def get_model_name(self):
        return self.AI_model.modelname
        
    def set_allow_overrule(self, allow_overrule):
        self.allow_overrule = allow_overrule
        self.ai.set_allow_overrule(allow_overrule)#ai=GomokuAI
        return self.id

# Set default player types. Can be changed on runtime (buttons in GUI)
player1 = Player("Human", 1)
player2 = Player("Human", 2)
players = [player1, player2]
current_player = player1


def logging_players():
    print("Logging players")
    print("Player 1 : " + str(player1.id))
    print("Player 1 : " + str(player1.TYPE))   
    print("Player 2 : " + str(player2.id))
    print("Player 2 : " + str(player2.TYPE))
    print("Current player : " + str(current_player.id))

def reset_player_stats():
    for i in range(len(players)):
        players[i].reset_score()

# Update win / loss stats of players: -1 = tie; 1 = player 1 won; 2 = player 2 won
def update_player_stats(instance:GomokuGame, winning_player):
    global player1, player2,players
    instance.GUI.update_wins(winning_player)
    AI_players=[p for p in players if p.TYPE=="AI-Model"]
    if winning_player > -1: # run if game was not a tie
        if winning_player == 1:
            if player1.TYPE =="AI-Model":
                player1.AI_model.log_win()
            if player2.TYPE =="AI-Model":
                player2.AI_model.log_loss()
        elif winning_player == 2:
            if player1.TYPE =="AI-Model":
                player1.AI_model.log_loss()
            if player2.TYPE =="AI-Model":
                player2.AI_model.log_win()

        for i in range(len(players)):
            if i == winning_player-1:
                players[i].wins += 1
                is_winner = True
            else:
                players[i].losses += 1
                is_winner = False
            players[i].calculate_score(instance.GRID_SIZE ** 2, is_winner, instance.current_game)
            if instance.last_round:
                players[i].calculate_win_rate(instance.current_game)
    else:
        for player in AI_players:
            player.AI_model.log_tie()

    for i in range(len(players)):
        players[i].calculate_score(0, False, instance.current_game)
    stats.log_win(players)
    if instance.last_round:
        stats.log_message(f"\nStatistics:\n{players[0].TYPE} {players[0].id}:\nwins: {players[0].wins} - win rate: {players[0].win_rate} - average score: {players[0].avg_score} - weighed score: {sum(players[0].weighed_scores)/len(players[0].weighed_scores)} - average moves: {players[0].avg_moves}.\n"
                          f"{players[1].TYPE} {players[1].id}:\nwins: {players[1].wins} - win rate: {players[1].win_rate} - average score: {players[1].avg_score} - weighed score: {sum(players[1].weighed_scores)/len(players[1].weighed_scores)} - average moves: {players[1].avg_moves}.")


# Function to draw the game board
def draw_board(instance:GomokuGame,last_move_model=None):
    global mark_last_move_model, player1, player2
    instance.screen.fill(instance.BOARD_COL)#screen needs to be cleared before drawing
    cell_size = instance.CELL_SIZE#cell_size=30
    radius_big_circle=cell_size//2 - 5#radius_big_circle=15
    radius_small_circle=cell_size//3 - 5#radius_small_circle=10
    radius_smallest_circle=cell_size//4 - 5#radius_smallest_circle=5
    red=(255,0,0) #R=255, G=0, B=0
    green=(0,255,0)
    cells_to_mark=[(7,7),(11,11),(3,3),(3,11),(11,3)]
    for row in range(instance.GRID_SIZE):#grid_size=15
        for col in range(instance.GRID_SIZE):
            if (row,col) in cells_to_mark:
                pygame.draw.rect(instance.screen, instance.LINE_COL, (col * cell_size, row * cell_size, cell_size, cell_size), 2)
            else:
                pygame.draw.rect(instance.screen, instance.LINE_COL, (col * cell_size, row * cell_size, cell_size, cell_size), 1)


            if instance.board[row][col] == 1:
                if (row,col)==last_move_model and mark_last_move_model:
                    pygame.draw.circle(instance.screen, instance.P1COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)
                    pygame.draw.circle(instance.screen, red, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_small_circle)

                    if instance.show_overruling and player1.ai.overruled_last_move:
                        pygame.draw.circle(instance.screen, green, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)
                else:
                    pygame.draw.circle(instance.screen, instance.P1COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)

            elif instance.board[row][col] == 2:
                if (row,col)==last_move_model and mark_last_move_model:
                    pygame.draw.circle(instance.screen, instance.P2COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)
                    pygame.draw.circle(instance.screen, red, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_small_circle)
                    if instance.show_overruling and player2.ai.overruled_last_move:
                        pygame.draw.circle(instance.screen, green, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)
                else:
                    pygame.draw.circle(instance.screen, instance.P2COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)

    # Draw the winning line
    if instance.winning_cells:
        start_row, start_col = instance.winning_cells[0]#start_cell=(0,0)
        end_row, end_col = instance.winning_cells[-1]#end_cell=(15,15)
        pygame.draw.line(instance.screen, (0, 255, 0),
                         (start_col * cell_size + cell_size // 2, start_row * cell_size + cell_size // 2),
                         (end_col * cell_size + cell_size // 2, end_row * cell_size + cell_size // 2), 5)
    if instance.show_hover_effect:
        ## adds hover effects to cells when mouse hovers over them##
        mouse_pos = pygame.mouse.get_pos()
        x,y = mouse_pos
        col = x // instance.CELL_SIZE
        row = y // instance.CELL_SIZE
        HOVER_COLOR = (211, 211, 211)
        if instance.GRID_SIZE > row >= 0 == instance.board[row][col] and 0 <= col < instance.GRID_SIZE:
            if instance.board[row][col] == 0:#cell is empty
                cell_size = instance.CELL_SIZE
                pygame.draw.circle(instance.screen, HOVER_COLOR, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)
                if current_player.id==1:
                    pygame.draw.circle(instance.screen, instance.P1COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)
                elif current_player.id==2:
                    pygame.draw.circle(instance.screen, instance.P2COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)

def reset_game(instance:GomokuGame):
    global current_player
    instance.board = [[0] * instance.GRID_SIZE for _ in range(instance.GRID_SIZE)]
    current_player = player1

def calculate_score(board, board_size=15):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    score_board = filereader.load_scores("consts.json")
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

def check_win(row, col, playerID, instance: GomokuGame):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for drow, dcol in directions:
        winning_cells = [(row, col)]
        winning_direction = ()
        count = 1
        # positive direction
        for i in range(1, 5):
            row_, col_ = row + i * drow, col + i * dcol
            if 0 <= row_ < instance.GRID_SIZE and 0 <= col_ < instance.GRID_SIZE and instance.board[row_][col_] == playerID:
                count += 1
                winning_cells.append((row_, col_))
                winning_direction = [(drow, dcol)]
            else:
                break
        # negative direction
        for i in range(1, 5):
            row_, col_ = row - i * drow, col - i * dcol
            if 0 <= row_ < instance.GRID_SIZE and 0 <= col_ < instance.GRID_SIZE and instance.board[row_][col_] == playerID:
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
            instance.winning_cells = winning_cells
            return True
    return False

def check_board_full(instance:GomokuGame):
    board = instance.board
    grid_size = instance.GRID_SIZE
    for row in range(grid_size):
        for col in range(grid_size):
            if board[row][col] == 0:
                return False
    return True

def convert_to_one_hot(board, player_id):
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

class fullscreen_GUI():
    def __init__(self,instance:GomokuGame):
        self.game_instance = instance
        self.root_play_game = None
        self.game_mode = None
    
    def quit_program(self):
        self.game_instance.quit_program = True
        self.stop_game()

    def skip_current_round(self):
        if self.game_mode==self.game_instance.game_modes[0]:#when playing
            self.game_instance.running = False
            self.game_instance.skip_current_round = True

    def stop_game(self):
        if self.vid is not None:
            self.vid.release()
        self.game_instance.running=False
        self.game_instance.stop_game=True
    
    def show_dialog_next_game(self):
        if self.game_instance.show_dialog:
            res=mb.askquestion(title='Start next game',message='Do you want to start the next game automatically?')
            if res.strip().lower() == 'yes' :
                pass
            else :
                mb.showinfo(message="Press any key to start the next game, you can wait as long as you want",title="Next game")
            
                self.key_pressed = False
                self.root_play_game.bind("<Key>", lambda event: self.on_key_press())
                while not self.key_pressed:
                    self.root_play_game.update()

    def on_key_press(self):
        self.key_pressed = True
     
    def update_wins(self,winner=None):
        if winner == 1:
            self.wins_player1 += 1
            self.var_wins_player1.set(self.wins_player1)
        elif winner == 2:
            self.wins_player2 += 1
            self.var_wins_player2.set(self.wins_player2)
        else:
            self.draws += 1
            self.var_draws.set(self.draws)

    def initialize_session(self):
        self.game_number = 0
        self.game_mode = self.game_instance.game_mode
                
        if self.game_instance.use_recognition:
            self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.vid = None

        self.wins_player1 = 0
        self.wins_player2 = 0
        self.draws = 0

    def initialize_fullscreen_GUI(self):
        global current_player

        self.initialize_session()

        if self.root_play_game is None:
            self.root_play_game = Tk()
            self.root_play_game.bind("<Escape>", lambda event: self.stop_game())
            self.root_play_game.bind("<q>", lambda event: self.quit_program())
            self.root_play_game.bind("<space>", lambda event: self.skip_current_round())

            self.var_current_player=StringVar(master=self.root_play_game)
            self.var_current_player.set("Current player: " + str(current_player.id))
            self.var_wins_player1 = IntVar(master=self.root_play_game)
            self.var_wins_player2 = IntVar(master=self.root_play_game)
            self.var_draws = IntVar(master=self.root_play_game)

            self.var_wins_player1.set(self.wins_player1)
            self.var_wins_player2.set(self.wins_player2)
            self.var_draws.set(self.draws)

            self.var_current_game=StringVar(master=self.root_play_game)

            self.var_current_game_mode=StringVar(master=self.root_play_game)

            #self.root_play_game.columnconfigure(0, weight=1)
            self.root_play_game.columnconfigure(1, weight=1)
            self.root_play_game.columnconfigure(2, weight=1)


            self.root_play_game.rowconfigure(0, weight=1)
            self.root_play_game.rowconfigure(1, weight=1)

            self.root_play_game.attributes("-fullscreen", True)
            self.root_play_game.config(bg="#357EC7")
            self.root_play_game.title("Gomoku")

            font_labels=("Arial", 18)
            distance_from_left_side=20

            self.frame_info=Frame(self.root_play_game,bg="#357EC7")
            self.frame_info.grid(row=0, column=0)
            self.current_player_label = Label(self.frame_info, textvariable=self.var_current_player, bg="#357EC7",fg='white', font=font_labels,pady=2,width=25)
            self.current_player_label.grid(row=0, column=0, sticky="w",padx=(distance_from_left_side,0),columnspan=2)
            self.label_current_game_mode=Label(self.frame_info, textvariable=self.var_current_game_mode, bg="#357EC7",fg="white", font=font_labels,width=25)
            self.label_current_game_mode.grid(row=1, column=0,sticky="w",padx=(distance_from_left_side,0))
            self.current_game_label=Label(self.frame_info, textvariable=self.var_current_game, bg="#357EC7",fg='white', font=font_labels,pady=2)
            self.current_game_label.grid(row=2, column=0, sticky="w",padx=(distance_from_left_side,0))

            self.frame_stats=Frame(self.frame_info,bg="#357EC7")
            self.frame_stats.grid(row=3, column=0, sticky="sw",pady=50)


            self.label_player1=Label(self.frame_stats, text="Player 1", bg="#357EC7",fg='white', font=font_labels,pady=2,width=10)
            self.label_player1.grid(row=0, column=1, sticky="sw")
            self.label_player2=Label(self.frame_stats, text="Player 2", bg="#357EC7",fg='white', font=font_labels,pady=2,width=10)
            self.label_player2.grid(row=0, column=2, sticky="sw")

            self.label_wins=Label(self.frame_stats, text="Wins: ", bg="#357EC7",fg='white', font=font_labels,pady=2)
            self.label_wins.grid(row=1, column=0, sticky="sw",padx=(distance_from_left_side,0))

            self.label_wins_player1=Label(self.frame_stats, textvariable=self.var_wins_player1, bg="#357EC7",fg='white', font=font_labels,pady=2)
            self.label_wins_player1.grid(row=1, column=1)
            self.label_wins_player2=Label(self.frame_stats, textvariable=self.var_wins_player2, bg="#357EC7",fg='white', font=font_labels,pady=2)
            self.label_wins_player2.grid(row=1, column=2)

            self.label_draws=Label(self.frame_stats, text="Draws: ", bg="#357EC7",fg='white', font=font_labels,pady=10)
            self.label_draws.grid(row=2, column=0, sticky="sw",padx=(distance_from_left_side,0))
            
            self.label_value_draws=Label(self.frame_stats, textvariable=self.var_draws, bg="#357EC7",fg='white', font=font_labels,pady=10)
            self.label_value_draws.grid(row=2, column=1,columnspan=2)

            self.label_recognition_info=Label(self.root_play_game,text="", bg="#357EC7",fg="white", font=font_labels)
            self.label_recognition_info.grid(row=0, column=1,sticky="n")

            self.embed_pygame = Frame(self.root_play_game, width=self.game_instance.WIDTH, height=self.game_instance.HEIGHT)
            self.embed_pygame.grid(row=0, column=1,rowspan=2)

            self.button_capture_image = Button(self.root_play_game, text="Capture Image (in development)", command=self.determine_move,width=25, bg="green",fg="white", font=font_labels)
            self.button_capture_image.grid(row=1, column=1,sticky="s",pady=(0,90))
            
            size_webcam_frame=500
            self.frame_webcam=Frame(self.root_play_game,bg="#357EC7")
            self.frame_webcam.grid(row=0, rowspan=2,column=2,sticky="e")

            self.label_webcam_image=Label(self.frame_webcam,text="Webcam photo view (in development)", bg="#357EC7",fg="white", font=font_labels)
            self.label_webcam_image.grid(row=0, column=0,sticky="e",padx=10)

            self.label_webcam_video=Label(self.frame_webcam,text="Webcam view", bg="#357EC7",fg="white", font=font_labels,width=size_webcam_frame,height=size_webcam_frame)
            self.label_webcam_video.grid(row=1, column=0,sticky="e")

            self.list_recognition_widgets=[self.label_webcam_video,self.label_webcam_image,self.button_capture_image,self.label_recognition_info,self.frame_webcam,self.button_capture_image]
            if not self.game_instance.use_recognition:
                for widget in self.list_recognition_widgets:
                    widget.grid_remove()
                self.root_play_game.columnconfigure(2, weight=0)
            
            self.widgets_to_hide_replay=[self.current_player_label,self.current_game_label,self.frame_stats]
            if self.game_mode==self.game_instance.game_modes[2]:#when replaying
                for widget in self.widgets_to_hide_replay:
                    widget.grid_remove()

            os.environ['SDL_WINDOWID'] = str(self.embed_pygame.winfo_id())
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        else:
            if not self.root_play_game.winfo_viewable():
                self.root_play_game.deiconify()

            if self.game_mode==self.game_instance.game_modes[2]:#when replaying
                for widget in self.widgets_to_hide_replay:
                    widget.grid_remove()
            else:
                for widget in self.widgets_to_hide_replay:
                    widget.grid()

            if self.game_instance.use_recognition:
                self.root_play_game.columnconfigure(2, weight=1)
                for widget in self.list_recognition_widgets:
                    if not widget.winfo_viewable():
                        widget.grid()
            else:
                self.root_play_game.columnconfigure(2, weight=0)
                for widget in self.list_recognition_widgets:
                    if widget.winfo_viewable():
                        widget.grid_remove()

        
        self.var_current_game_mode.set("Game mode: " + self.game_mode)
        self.label_current_game_mode.update()

        pygame.display.init()
        self.game_instance.screen = pygame.display.set_mode((self.game_instance.WIDTH, self.game_instance.HEIGHT))
    
        self.pygame_loop()


    def hide_GUI(self):
        self.root_play_game.withdraw()

    def refresh_labels(self):
        if current_player.TYPE == "Human":
            player_text="Human         "
        elif current_player.TYPE == "AI-Model":
            player_text="AI-Model      "
        else:
            player_text="Test Algorithm"

        self.var_current_player.set("Current player: " + str(current_player.id) + " : " + player_text)
        self.current_player_label.update()

        self.var_current_game.set("Game: " + str(self.game_number+1))
        self.current_game_label.update()

    def refresh_screen(self,game_number):
        self.game_number = game_number
        self.refresh_labels()
        pygame.display.flip()

    def pygame_loop(self):
        global current_player
        pygame.display.flip()
        self.root_play_game.update()
        self.root_play_game.after(100, self.pygame_loop)

        if self.game_instance.use_recognition:
            self.root_play_game.after(150,lambda: self.show_webcam_view(self.label_webcam_video))
    
    def crop_to_square(self,frame):
        height, width = frame.shape[:2]
        smallest_side = min(height, width)
        start_x = (width - smallest_side) // 2 
        start_y = (height - smallest_side) // 2
        square_frame = frame[start_y:start_y + smallest_side, start_x:start_x + smallest_side]
        return square_frame

    def show_webcam_view(self,label):
        try:
            # Capture the video frame by frame 
            _, frame = self.vid.read() 
        except:
            self.vid=cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.show_webcam_view(label)
        try:

            frame=self.crop_to_square(frame)

            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
  
            captured_image = Image.fromarray(opencv_image) 
  
            photo_image = ImageTk.PhotoImage(image=captured_image,master=self.root_play_game)
  
            label.photo_image = photo_image 
  
            self.root_play_game.after(0,label.config(image=photo_image)) 
        except:
            pass

    def determine_move(self):
        if self.game_instance.play_music:
            Thread(target=lambda:pygame.mixer.music.fadeout(1000)).start()#don't block the main thread
        #write_relevant_pieces_after_move_to_file()
        #(x,y)=recognize_move()
      
        (x,y)=(None,None)
        #write_relevant_pieces_before_move_to_file()
        self.show_webcam_view(self.label_webcam_image)
        if (x,y) ==(None,None):
            self.root_play_game.after(0,self.label_recognition_info.config(text="No move was recognized, try again later.",fg="red"))
            return #don't do anything
        x,y=(x,y)
        self.root_play_game.after(0,self.label_recognition_info.config(text="Your move was successfully recognized.",fg="green"))
        try:
            handle_human_move(self.game_instance, x, y , players, p1_moves, p2_moves)
        except:
            handle_human_move(self.game_instance, x, y, players)

    

def handle_human_move(instance:GomokuGame, x, y, players,p1_moves=None, p2_moves=None):
    global victory_text, winning_player,current_player
    col = x // instance.CELL_SIZE 
    row = y // instance.CELL_SIZE
    if instance.GRID_SIZE > row >= 0 == instance.board[row][col] and 0 <= col < instance.GRID_SIZE:
        instance.board[row][col] = current_player.id
        if current_player.id == 1 and instance.record_replay:
            p1_moves.append((row, col))
        elif instance.record_replay:
            p2_moves.append((row, col))
        players[current_player.id - 1].moves += 1
        if check_win(row, col, current_player.id, instance):
            victory_text = f"Player {current_player.id} wins!"
            winning_player = current_player.id
            instance.running = False
        else:
            #logging_players()
            if instance.play_music:
                Thread(target=start_music_delayed).start()

            # Switch player if neither player have won
            current_player = players[2 - current_player.id]  #current_player kan 2 zijn of 1, maar in beide gevallen zal er van speler gewisseld worden.
            #logging_players()    

def runGame(instance:GomokuGame, game_number):#main function
    # Main game loop
    global window_name, victory_text, current_player, player1, player2,p1_moves, p2_moves,winning_player

    if instance.use_recognition:
        print("using recognition")
    else:
        print("not using recognition")

    if player1.TYPE=="AI-Model":
        if player1.allow_overrule:
            print("Overruling is allowed for player 1")
        else:
            print("Overruling is not allowed for player 1")

    if player2.TYPE=="AI-Model":
        if player2.allow_overrule:
            print("Overruling is allowed for player 2")
        else:
            print("Overruling is not allowed for player 2")
    
    mark_last_move_model=True
    instance.winning_cells = []
    instance.running = True
    instance.stop_game = False
    winning_player = 0

    if instance.record_replay:
        p1_moves = []
        p2_moves = []

    while instance.running:
        handle_pygame_events()
        if not check_board_full(instance):
            # Human move
            if current_player.TYPE == "Human":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        instance.running = False 
                    elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_UP or event.type == pygame.K_RIGHT) and event.button == 1: #kan zo gelaten worden. Wanneer op de muis wordt gedrukt,wordt de zet gelezen van het bestand
                        
                        if not instance.use_recognition:
                            x,y=event.pos

                            if instance.play_music:
                                Thread(target=lambda:pygame.mixer.music.fadeout(1000)).start()#don't block the main thread
                        else:
                            continue
                        try:
                            handle_human_move(instance, x, y, players, p1_moves, p2_moves) 
                        except:
                            handle_human_move(instance, x, y, players)   

            # test algorithm move
            elif current_player.TYPE == "Test Algorithm" and not testai.check_game_over(instance):
                if instance.ai_delay:
                    time.sleep(random.uniform(0.25, 1.0))   # randomize ai "thinking" time
                ai_row, ai_col = testai.ai_move(instance, players[current_player.id-1].id)
                testai.make_move((ai_row, ai_col), current_player.id, instance)
                players[current_player.id-1].moves += 1

                if current_player.id == 1 and instance.record_replay:
                    p1_moves.append((ai_row, ai_col))
                elif instance.record_replay:
                    p2_moves.append((ai_row, ai_col))

                if check_win(ai_row, ai_col, current_player.id, instance):
                    victory_text = f"AI-Model {players[current_player.id-1].id} wins!"
                    winning_player = current_player.id
                    instance.running = False
                else:
                    current_player = players[2 - current_player.id]
                    #logging_players()   
            
            # AI model
            elif current_player.TYPE == "AI-Model":
                if instance.ai_delay:
                    time.sleep(random.uniform(0.25, 1.0))   # randomize AI "thinking" time
                one_hot_board = convert_to_one_hot(instance.board, players[current_player.id-1].id)
                DVC_AI = players[current_player.id-1].ai#player1.ai or player2.ai #always an instance of GomokuAI
                DVC_AI.set_game(one_hot_board)
                max_score, scores, scores_normalized = calculate_score(instance.board)
                DVC_AI.current_player_id=current_player.id
                action = DVC_AI.get_action(instance.board, one_hot_board, scores_normalized)
               
                np_scores = np.array(scores).reshape(15, 15)
                short_score = np_scores[action[0]][action[1]]
                if mark_last_move_model:
                    last_move_model=action #=last move for example :(3,6)
                else:
                    last_move_model=None
                if max_score <= 0:
                    # prevent division with negative values or zero
                    score = 0
                else:
                    score = short_score / max_score
                if current_player.id == 1 and instance.record_replay:
                    p1_moves.append(action)
                elif instance.record_replay:
                    p2_moves.append(action)

                players[current_player.id - 1].weighed_moves.append(score)
                instance.board[action[0]][action[1]] = current_player.id
                game_over = check_win(action[0], action[1], current_player.id, instance)
                players[current_player.id-1].final_action = action
                players[current_player.id - 1].moves += 1
                if game_over:
                    victory_text = f"AI-Model {players[current_player.id - 1].id} wins!"
                    winning_player = current_player.id
                    print("player that has won:",winning_player)
                    instance.running = False
                else:
                    current_player = players[2 - current_player.id]
                    #print("Na switch player AI!!!!!!!!!!!")
                    #logging_players()    
            try:
                draw_board(instance,last_move_model)
            except :
                draw_board(instance)

            instance.GUI.refresh_screen(game_number)
                
        else:
            victory_text = "TIE"
            winning_player = -1
            instance.running = False

    # End game
    
    if not instance.stop_game and not instance.skip_current_round:
        if instance.record_replay:
            filereader.save_replay(p1_moves, p2_moves)
        stats.log_message(victory_text)
        update_player_stats(instance, winning_player)
        time.sleep(instance.SLEEP_BEFORE_END)#sleep before closing for SLEEP_BEFORE_END seconds
        instance.GUI.show_dialog_next_game()

    reset_game(instance)


def handle_pygame_events():
    if not player1.TYPE == "Human" and  not player2.TYPE == "Human":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pygame.QUIT:
                    pygame.quit()

def runTraining(instance:GomokuGame, game_number):#main function
    # Main game loop
    global window_name, victory_text, current_player,player1,player2,winning_player
    mark_last_move_model=False 

    if player1.allow_overrule:
        print("Overruling is allowed for player 1")
    else:
        print("Overruling is not allowed for player 1")

    if player2.TYPE=="AI-Model":
        if player2.allow_overrule:
            print("Overruling is allowed for player 2")
        else:
            print("Overruling is not allowed for player 2")

    for p in players:
        if p.TYPE == "AI-Model":
            p.ai.model.load_model(p.AI_model.modelname)
            p.ai.train = True
        elif p.TYPE == "Human":
            p.ai.train = False
            mark_last_move_model=True

    instance.play_music=False

    instance.winning_cells = []
    instance.running = True
    instance.stop_game = False
    winning_player = 0

    if instance.record_replay:
        p1_moves = []
        p2_moves = []

    while instance.running:
        handle_pygame_events()
        # Check if board is full    
        if not check_board_full(instance):
            # Human move
            if current_player.TYPE == "Human":
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        instance.running = False 
                        #druk op linkermuisknop om te zetten
                    elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_UP or event.type == pygame.K_RIGHT) and event.button == 1: #kan zo gelaten worden. Wanneer op de muis wordt gedrukt,wordt de zet gelezen van het bestand
                        Thread(target=lambda:pygame.mixer.music.fadeout(1000)).start()#don't block the main thread
                        x,y=event.pos
                        try:
                            handle_human_move(instance, x, y, instance.record_replay, players, p1_moves, p2_moves) 
                        except:
                            handle_human_move(instance, x, y, instance.record_replay, players)
            # test algorithm
            elif current_player.TYPE == "Test Algorithm" and not testai.check_game_over(instance):
                if instance.ai_delay:
                    time.sleep(random.uniform(0.25, 1.0))   # randomize ai "thinking" time
                ai_row, ai_col = testai.ai_move(instance, players[current_player.id-1].id)
                testai.make_move((ai_row, ai_col), current_player.id, instance)
                players[current_player.id-1].moves += 1
                if current_player.id == 1 and instance.record_replay:
                    p1_moves.append((ai_row, ai_col))
                elif instance.record_replay:
                    p2_moves.append((ai_row, ai_col))
                if check_win(ai_row, ai_col, current_player.id, instance):
                    victory_text = f"AI-Model {players[current_player.id-1].id} wins!"
                    winning_player = current_player.id
                    instance.running = False
                else:
                    current_player = players[2 - current_player.id]
                    #logging_players()   
            
            # AI-Model
            elif current_player.TYPE == "AI-Model":
                if instance.ai_delay:
                    time.sleep(random.uniform(0.25, 1.0))   # randomize AI "thinking" time
                one_hot_board = convert_to_one_hot(instance.board, players[current_player.id-1].id)
                handle_pygame_events()
                mm_ai = players[current_player.id-1].ai
                mm_ai.set_game(one_hot_board)
                old_state = instance.board
                max_score, scores, scores_normalized = calculate_score(instance.board)
                mm_ai.current_player_id=current_player.id
                action = mm_ai.get_action(instance.board, one_hot_board, scores_normalized)
                if mark_last_move_model:
                    last_move=action #=last move for example :(3,6)
                else:
                    last_move=None
                np_scores = np.array(scores).reshape(15, 15)
                short_score = np_scores[action[0]][action[1]]
                if max_score <= 0:
                    # prevent division with negative values or zero
                    score = 0
                else:
                    score = short_score / max_score
                if current_player.id == 1 and instance.record_replay:
                    p1_moves.append(action)
                elif instance.record_replay:
                    p2_moves.append(action)
                players[current_player.id - 1].weighed_moves.append(score)
                instance.board[action[0]][action[1]] = current_player.id
                game_over = check_win(action[0], action[1], current_player.id, instance)
                next_max_score, next_scores, next_scores_normalized = calculate_score(instance.board)
            
                mm_ai.remember(old_state, action, score, instance.board, game_over)
                mm_ai.train_short_memory(one_hot_board, action, short_score, scores, convert_to_one_hot(instance.board, current_player), next_scores, game_over)
                current_player.move_loss.append(mm_ai.loss)
                
                current_player.final_action = action
                current_player.moves += 1
                if game_over:
                    victory_text = f"AI-Model {players[current_player.id - 1].id} wins!"
                    winning_player = current_player.id
                    instance.running = False
                else:
                    current_player = players[2 - current_player.id]
                    #logging_players()    
            try:
                draw_board(instance,last_move)
            except:
                draw_board(instance)
            handle_pygame_events()
            instance.GUI.refresh_screen(game_number)
                
        else:
            victory_text = "TIE"
            winning_player = -1
            instance.running = False

    
    # For any AI-Model, train for long memory and save model
    if not instance.stop_game:
        if instance.record_replay:
            filereader.save_replay(p1_moves, p2_moves)

        stats.log_message(victory_text)#only log when game isn't interrupted
        update_player_stats(instance, winning_player)

        data = {}
        loss_data = {}
        move_loss_data = {}
        for p in players:
            handle_pygame_events()
            if p.TYPE == "AI-Model":
                p.ai.remember(instance.board, p.final_action, p.score, instance.board, True)
                p.ai.train_long_memory()
                p.score_loss.append(p.ai.loss)
                move_loss = [float(val) for val in p.move_loss]
                p.final_move_loss.append(sum(move_loss)/len(move_loss))
                p.ai.model.save_model(p.AI_model.modelname) #only saves after each round
                p.final_move_scores.append(sum(p.weighed_moves)/len(p.weighed_moves))
                stats.log_message(f"{p.TYPE} {p.id}: score loss: {float(p.ai.loss)}")
                stats.log_message(f"{p.TYPE} {p.id}: move loss: {sum(p.move_loss)/len(p.move_loss)}")
            p.reset_score()
            if instance.last_round:
                if p.TYPE == "AI-Model":
                    data[f"{p.TYPE} {p.id}: game accuracy"] = p.weighed_scores
                    data[f"{p.TYPE} {p.id}: move accuracy"] = p.final_move_scores
                    loss_data[f"{p.TYPE} {p.id}: score loss"] = [float(val) for val in p.score_loss]
                    move_loss_data[f"{p.TYPE} {p.id}: move loss"] = p.final_move_loss
                    stats.log_message(f"{p.TYPE} {p.id}: average score loss: {sum([float(val) for val in p.score_loss]) / len([float(val) for val in p.score_loss])}")
                    stats.log_message(f"{p.TYPE} {p.id}: average move loss: {sum(p.final_move_loss) / len(p.final_move_loss)}")
                p.reset_all_stats()#purely for testing purposes
        if instance.show_graphs:
            if len(data) > 0:
                stats.plot_graph(data, 'accuracy')
            if len(loss_data) > 0:
                stats.plot_graph(loss_data, 'loss data')
            if len(move_loss_data) > 0:
                stats.plot_graph(move_loss_data, 'loss data')

        time.sleep(instance.SLEEP_BEFORE_END)#sleep before closing for SLEEP_BEFORE_END seconds
    
    reset_game(instance)

def runReplay(instance:GomokuGame, moves:dict=None):#main function
    # Main game loop
    global window_name, victory_text, current_player

    instance.winning_cells = []
    instance.running = True
    instance.stop_game = False

    if moves is not None:#always true for now
        move_id = 0
        position = list(moves.keys())
    else:
        pass
        
    while instance.running:
        handle_pygame_events()
        if not check_board_full(instance):
            #Replay
            if players[current_player.id - 1].TYPE == "Replay":
                if instance.ai_delay:
                    time.sleep(random.uniform(0.25, 1.0))   # randomize ai "thinking" time
                instance.board[position[move_id][0]][position[move_id][1]] = current_player.id
                last_move = position[move_id]
                if check_win(position[move_id][0], position[move_id][1], current_player.id, instance):
                    victory_text = f"AI model {players[current_player.id-1].id} wins!"
                    instance.running = False
                else:
                    current_player = players[2 - current_player.id]
                    move_id += 1
            try:
                draw_board(instance,last_move)
            except:
                draw_board(instance)
            instance.GUI.refresh_screen(0)
                
        else:
            victory_text = "TIE"
            instance.running = False

    # End game
    if not instance.stop_game:
        stats.log_message(victory_text)
        instance.GUI.show_dialog_next_game()
        time.sleep(instance.SLEEP_BEFORE_END)#sleep before closing for SLEEP_BEFORE_END seconds

    reset_game(instance)



pygame.quit()