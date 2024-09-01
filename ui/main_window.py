from time import time
from tkinter import ttk
from tkinter import *
import numpy as np

from game.game import Game
from .settings_windows import replay_window
from .settings_windows import new_game_window
from .settings_windows import train_window
from .settings_windows import models_window
import enum
import controllers
from configuration.config import *
import tkinter.messagebox as mb

class WindowMode(enum.Enum):
    replay = 'replay'
    computer_move = 'computer_move'
    human_move = 'human_move'
    pause = 'pause'


class GameType(enum.Enum):
    human_vs_human = 'human_vs_human'
    replay = 'replay'



class GomokuApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("Gomoku")
        self.config(background="#357EC7")
        self.resizable(True, True)
        self.attributes("-fullscreen", False) #todo: set to true in production
        self.tk.call('tk', 'scaling', 1.5)#adjust depending on your screen resolution

        self.window_mode = WindowMode.pause
        self.game_type = GameType.human_vs_human
        
        # Canvas to draw the chessboard
        self.canvas = Canvas(self, width=750, height=750)
        self.canvas.grid(row=1, column=0, padx=10)

        # Label and Button for Main Window
        label = ttk.Label(self, text="Gomoku")
        label.grid(row=0, column=0, padx=10)

        self.menubar= Menu(self,font=("Helvetica", 12),tearoff=0)
        self.config(menu=self.menubar)
        self.new_game_menu = Menu(self.menubar,tearoff=0)

        self.new_game_menu.add_command(label="Play", command=lambda:self.open_new_window("Play"))
        self.new_game_menu.add_command(label="Train", command=lambda:self.open_new_window("Train"))
        self.new_game_menu.add_command(label="Replay", command=lambda:self.open_new_window("Replay"))

        self.menubar.add_cascade(label="New Game",menu=self.new_game_menu)

        self.models_menu= Menu(self.menubar,tearoff=0)
        self.models_menu.add_command(label="models", command=lambda:self.open_new_window("Models"))

        self.menubar.add_cascade(label="Models",menu=self.models_menu)
        
        # Store squares to identify them later
        self.squares = {}
        
        self.BOARDSIZE=int(config["OTHER VARIABLES"]["BOARDSIZE"])
        self.create_gomokuboard(self.BOARDSIZE)#todo: needs to be read from the consts file
        
        board = np.zeros((self.BOARDSIZE, self.BOARDSIZE))
        self.draw_pieces(board)
        self.controller = controllers
        
        self.frame_replay = Frame(self)
        # Previous button
        self.prev_button = Button(self.frame_replay, text="◄ Previous", command=self.show_previous)

        # Next button
        self.next_button = Button(self.frame_replay, text="Next ►", command=self.show_next)

        # Place the buttons in the frame
        self.prev_button.pack(side=LEFT, padx=5)  # Place button1 on the left side of the frame
        self.next_button.pack(side=LEFT, padx=5)  # Place button2 next to button1 on the left side

        self.deactivate_replay_frame()
        
        self.color_player_1 = "red"
        self.color_player_2 = "blue"

    
    def open_new_window(self, window_type):
        start=time()
        self.close_secondary_windows()

        match window_type:
            case "Replay":
                new_window = replay_window.ReplayWindow(self)
            case "Play":
                new_window = new_game_window.NewGameWindow(self)
            case "Models":
                new_window = models_window.ModelsWindow(self)
            case "Train":
                new_window = train_window.TrainWindow(self)
        
        self.show_replay_buttons(window_type=="Replay")

        print("time open window",time()-start)
    
    def show_replay_buttons(self,show):
        if show:
            self.prev_button.pack(side=LEFT, padx=5)  # Place button1 on the left side of the frame
            self.next_button.pack(side=LEFT, padx=5)  # Place button2 next to button1 on the left side
        else:
            self.prev_button.pack_forget()
            self.next_button.pack_forget()


    def create_gomokuboard(self, grid_size):
        square_size = 50    # Each square will be 50x50 pixels
        # Create the squares for the chessboard
        for row in range(grid_size):
            for col in range(grid_size):
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size

                # Alternate the colors
                if (row + col) % 2 == 0:
                    color = "white"
                else:
                    color = "black"
                
                # Create rectangle and store its ID
                square_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                
                # Save the row, col, and coordinates as data for this square
                self.squares[square_id] = (row, col, x1, y1, x2, y2)

                # Bind click event to this rectangle
                self.canvas.tag_bind(square_id, "<Button-1>", self.on_square_click)

    def on_square_click(self, event):
        if (self.window_mode == WindowMode.human_move):
            # Get the ID of the clicked square
            square_id = self.canvas.find_closest(event.x, event.y)[0]
            # Retrieve row, column, and coordinates from the stored dictionary
            row, col, x1, y1, x2, y2 = self.squares[square_id]
            self.controller.human_put_piece(row, col)
                  
    def delete_pieces(self):
        self.canvas.delete("piece")

    def draw_pieces(self,board):
        rows, cols = board.shape
        for i in range(rows):
            for j in range(cols):
                if board[i,j] != 0:
                    for value in self.squares.values():
                        if value[0] == i and value[1] == j:
                            padding = 10
                            if board[i,j] == 1:
                                color = self.color_player_1
                            else:
                                color = self.color_player_2
                            self.canvas.create_oval(value[2] + padding, value[3] + padding, value[4] - padding, value[5] - padding, fill=color, tags="piece")

    def activate_game(self):  
        self.close_secondary_windows()
        self.canvas.config(state="normal")

    def show_previous(self):
        """Show the previous item in the list."""
        if self.controller.current_index >= 0:
            self.delete_pieces()
            self.controller.previous()
            self.draw_pieces(Game().board.board)
        self.update_replay_button_states()

    def show_next(self):
        """Show the next item in the list."""
        if self.controller.current_index < len(self.controller.moves) - 1:
            self.delete_pieces()
            self.controller.next()
            self.draw_pieces(Game().board.board)
        self.update_replay_button_states()

    def update_replay_button_states(self):
        """Enable or disable buttons based on the current index."""
        if self.controller.current_index == -1:
            self.prev_button.config(state=DISABLED)
        else:
            self.prev_button.config(state=NORMAL)

        if self.controller.current_index == len(self.controller.moves) - 1:
            self.next_button.config(state=DISABLED)
        else:
            self.next_button.config(state=NORMAL)

    def activate_replay_frame(self):
        self.frame_replay.grid(row=3, column=0, padx=10)  
        self.close_secondary_windows()
        
    def deactivate_replay_frame(self):
        self.frame_replay.grid_forget()

        
    def close_secondary_windows(self):
        for widget in self.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()
        

    def clear_board(self):
        self.canvas.delete("piece")
    
    def end_game(self):
         mb.showinfo("End of the game","There's a winner, player"+str(self.controller.game.winner))
         self.clear_board()
         self.canvas.config(state=DISABLED)