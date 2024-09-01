from tkinter import *
import numpy as np
import operator
from game import GameFactory, GameBoard, Game
from secondwindow import SecondWindow



# Main Application Class
class MainApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("Clickable Chessboard")
        self.geometry("800x800")
        
        # Canvas to draw the chessboard
        self.canvas = Canvas(self, width=750, height=750)
        self.canvas.pack()

        # Label and Button for Main Window
        label = Label(self, text="This is the Main Window")
        label.pack(pady=20)

        # Button to open a new window
        open_window_button = Button(self, text="Open New Window", command=self.open_new_window)
        open_window_button.pack()
        
        # Store squares to identify them later
        self.squares = {}
        
        self.create_chessboard()
        
        board = np.zeros((15, 15))
        board[1,2]=1
        board[3,4]=2
        self.draw_pieces(board)

    def open_new_window(self):
        # Open a new window
        new_window = SecondWindow(self)

        
    def create_chessboard(self):
        rows, cols = 15, 15  # Chessboard has 15 rows and 15 columns
        square_size = 50    # Each square will be 50x50 pixels

        # Create the squares for the chessboard
        for row in range(rows):
            for col in range(cols):
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
        # Get the ID of the clicked square
        square_id = self.canvas.find_closest(event.x, event.y)[0]

        # Retrieve row, column, and coordinates from the stored dictionary
        row, col, x1, y1, x2, y2 = self.squares[square_id]

        # Print the clicked square position
        print(f"Square clicked at row {row}, column {col}")

        # Draw a circle inside the clicked square
        padding = 10  # Padding to keep the circle inside the square
        self.canvas.create_oval(x1 + padding, y1 + padding, x2 - padding, y2 - padding, fill="red")


    def draw_pieces(self, board):
        rows, cols = board.shape
        for i in range(rows):
            for j in range(cols):
                if board[i,j] != 0:
                    for value in self.squares.values():
                        print(value)  
                        if value[0] == i and value[1] == j:
                            print("gevonden")
                            padding = 10
                            if board[i,j] == 1:
                                color = "blue"
                            else:
                                color = "red"
                            self.canvas.create_oval(value[2] + padding, value[3] + padding, value[4] - padding, value[5] - padding, fill=color)

        








# # Running the application
# if __name__ == "__main__":
#     ##Create players
#     player1 = GameFactory.create_player("Human", 1)
#     player2 = GameFactory.create_player("AI", 2)
#     game_board = GameFactory.create_game_board(15)
#     game = GameFactory.create_game(game_board, player1, player2)
    
#     app = MainApp()
#     app.mainloop()
