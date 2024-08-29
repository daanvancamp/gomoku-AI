import tkinter as tk
from tkinter import ttk
import numpy as np
from . import replay_window
from . import new_game_window
import enum
import controller


class WindowMode(enum.Enum):
    replay = 'replay'
    computer_move = 'computer_move'
    human_move = 'human_move'
    pause = 'pause'


class GameType(enum.Enum):
    human_vs_human = 'human_vs_human'
    replay = 'replay'


# Main Application Class
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gomoku")
        self.geometry("800x800")
        
        self.window_mode = WindowMode.pause
        self.game_type = GameType.human_vs_human
        
        # Canvas to draw the chessboard
        self.canvas = tk.Canvas(self, width=750, height=750)
        self.canvas.grid(row=1, column=0, padx=10)

        # Label and Button for Main Window
        label = ttk.Label(self, text="This is the Main Window")
        label.grid(row=0, column=0, padx=10)

        self.menubar=tk.Menu(self)
        self.config(menu=self.menubar)
        self.new_game_menu = tk.Menu(self.menubar,tearoff=0)

        self.new_game_menu.add_command(label="Play", command=lambda:self.open_new_window("Play"))
        self.new_game_menu.add_command(label="Train", command=lambda:self.open_new_window("Train"))
        self.new_game_menu.add_command(label="Replay", command=lambda:self.open_new_window("Replay"))

        self.menubar.add_cascade(label="New Game",menu=self.new_game_menu)

        self.models_menu=tk.Menu(self.menubar,tearoff=0)
        self.models_menu.add_command(label="models", command=lambda:self.open_new_window("Models"))

        self.menubar.add_cascade(label="Models",menu=self.models_menu)
        
        # Store squares to identify them later
        self.squares = {}
        
        self.create_gomokuboard(15)
        
        board = np.zeros((15, 15))
        self.draw_pieces(board)
        self.controller = controller
        
        self.frame_replay = tk.Frame(self)
        # Previous button
        self.prev_button = ttk.Button(self.frame_replay, text="◄ Previous", command=self.show_previous)

        # Next button
        self.next_button = ttk.Button(self.frame_replay, text="Next ►", command=self.show_next)

        # Place the buttons in the frame
        self.prev_button.pack(side=tk.LEFT, padx=5)  # Place button1 on the left side of the frame
        self.next_button.pack(side=tk.LEFT, padx=5)  # Place button2 next to button1 on the left side

        self.deactivate_replay_frame()
        
        self.color_player_1 = "red"
        self.color_player_2 = "blue"

    
    def open_new_window(self, window_type):
        if (window_type == "Replay"):
            new_window = replay_window.ReplayWindow(self)
        elif (window_type == "Play"):
            new_window = new_game_window.NewGameWindow(self)
        
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

            # Print the clicked square position
            print(f"Square clicked at row {row}, column {col}")

            self.controller.put_piece(row, col)
                  
    def delete_pieces(self):
        self.canvas.delete("piece")

    def draw_pieces(self, board):
        rows, cols = board.shape
        for i in range(rows):
            for j in range(cols):
                if board[i,j] != 0:
                    for value in self.squares.values():
                        if value[0] == i and value[1] == j:
                            padding = 10
                            if board[i,j] == 1:
                                color = "blue"
                            else:
                                color = "red"
                            self.canvas.create_oval(value[2] + padding, value[3] + padding, value[4] - padding, value[5] - padding, fill=color, tags="piece")

    def activate_game(self):  
        self.close_secondary_windows()

    def show_previous(self):
        """Show the previous item in the list."""
        if self.controller.current_index >= 0:
            self.delete_pieces()
            self.controller.previous()
            self.draw_pieces(self.controller.game_board.board)
        self.update_replay_button_states()

    def show_next(self):
        """Show the next item in the list."""
        if self.controller.current_index < len(self.controller.moves) - 1:
            self.delete_pieces()
            self.controller.next()
            self.draw_pieces(self.controller.game_board.board)
        self.update_replay_button_states()

    def update_replay_button_states(self):
        """Enable or disable buttons based on the current index."""
        if self.controller.current_index == -1:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if self.controller.current_index == len(self.controller.moves) - 1:
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    def activate_replay_frame(self):
        self.frame_replay.grid(row=3, column=0, padx=10)  
        self.close_secondary_windows()
        
    def deactivate_replay_frame(self):
        self.frame_replay.grid_forget()

        
    def close_secondary_windows(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        


