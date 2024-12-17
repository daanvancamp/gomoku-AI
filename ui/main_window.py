from tkinter import *
import tkinter.messagebox as mb
import numpy as np
import logging
import enum

from ui.frame_recognition_buttons import FrameRecognitionButtons
from ui.frame_webcam import FrameWebcam

from .settings_windows import replay_window, new_game_window, train_window, scoreboard_window, models_window, physical_play_window
import controllers
from configuration.config import config

# Use the existing logger by name
logger = logging.getLogger('my_logger')


class WindowMode(enum.Enum):
	replay = 'replay'
	computer_move = 'computer_move'
	human_move = 'human_move'
	pause = 'pause'
	recognition ='recognition'#recognition in progress

class GameType(enum.Enum):
	human_vs_human = 'human_vs_human'
	replay = 'replay'



class GomokuApp(Tk):
	def __init__(self):
		logger.info("Initialize GomokuApp")
		
		super().__init__()

		self.title("Gomoku")
		self.config(background="#357EC7")
		self.bind("<Escape>", lambda e: self.toggle_fullscreen(True))
		self.bind("<F11>", lambda e: self.toggle_fullscreen())
		self.resizable(True, True)
		self.attributes("-fullscreen", True)

		self.window_mode = WindowMode.pause
		self.game_type = GameType.human_vs_human
		
		# Canvas to draw the chessboard
		self.canvas = Canvas(self, width=750, height=750)
		self.canvas.grid(row=0, column=0, rowspan=2, padx=10)

		self.menubar = Menu(self,font=("Helvetica", 12),tearoff=0)
		self.config(menu=self.menubar)

		self.new_game_menu = Menu(self.menubar,tearoff=0)
		self.new_game_menu.add_command(label="Play", command=lambda:self.open_new_window("Play"))
		self.new_game_menu.add_command(label="Play with physical board", command=lambda:self.open_new_window("PhysicalPlay"))
		self.new_game_menu.add_command(label="Train", command=lambda:self.open_new_window("Train"))
		self.new_game_menu.add_command(label="Replay", command=lambda:self.open_new_window("Replay"))
		self.menubar.add_cascade(label="New Game",menu=self.new_game_menu)

		self.models_menu = Menu(self.menubar,tearoff=0)
		self.models_menu.add_command(label="models", command=lambda:self.open_new_window("Models"))
		self.menubar.add_cascade(label="Models",menu=self.models_menu)
		
		self.scoreboard_menu = Menu(self.menubar,tearoff=0)
		self.scoreboard_menu.add_command(label="scoreboard", command=lambda:self.open_new_window("Scoreboard"))
		self.menubar.add_cascade(label="Scoreboard",menu=self.scoreboard_menu)
		
		self.squares = {}
		
		self.BOARDSIZE = int(config["OTHER VARIABLES"]["BOARDSIZE"])
		self.create_gomokuboard(self.BOARDSIZE)
		
		board = np.zeros((self.BOARDSIZE, self.BOARDSIZE))
		self.draw_pieces(board)
		self.controller = controllers
		
		self.frame_replay = Frame(self)

		self.prev_button = Button(self.frame_replay, text="◄ Previous", command=self.show_previous)

		self.next_button = Button(self.frame_replay, text="Next ►", command=self.show_next)

		# Place the buttons in the frame
		self.prev_button.pack(side=LEFT, padx=5)  # Place button1 on the left side of the frame
		self.next_button.pack(side=LEFT, padx=5)  # Place button2 next to button1 on the left side

		self.deactivate_replay_frame()

		self.frame_webcam = FrameWebcam(self)
		self.frame_recognition_buttons = FrameRecognitionButtons(self)
		
		self.color_player_1 = "red"
		self.color_player_2 = "blue"
		
		self.draw_scoreboard = False
		self.overruled_last_move = None

	def toggle_fullscreen(self,esc_was_used=False): #esc to exit fullscreen, f11 to enter fullscreen or to exit fullscreen
		self.attributes('-fullscreen', not self.attributes('-fullscreen')) if not esc_was_used else self.attributes('-fullscreen', False)

	def open_new_window(self, window_type):
		self.close_secondary_windows()
		self.last_window_type = window_type

		match window_type:
			case "Replay":
				new_window = replay_window.ReplayWindow(self)
			case "Play":
				new_window = new_game_window.NewGameWindow(self)
			case "PhysicalPlay":
				new_window = physical_play_window.PhysicalPlayWindow(self)
			case "Models":
				new_window = models_window.ModelsWindow(self)
			case "Train":
				new_window = train_window.TrainWindow(self)
			case "Scoreboard":
				new_window = scoreboard_window.ScoreboardWindow(self)
		
	def hide_unnecessary_widgets(self): #this function is used so the buttons are hided when starting a controller, not when opening a new window. (A user could close a window without starting a new game.)
		self.show_replay_buttons(self.last_window_type=="Replay") #show replay buttons when using replay mode
		self.show_recognition_widgets(self.last_window_type=="PhysicalPlay")

	def show_replay_buttons(self,show):
		if show:
			self.prev_button.pack(side=LEFT, padx=5)  # Place button1 on the left side of the frame
			self.next_button.pack(side=LEFT, padx=5)  # Place button2 next to button1 on the left side
		else:
			self.prev_button.pack_forget()
			self.next_button.pack_forget()
			self.deactivate_replay_frame()

	def show_recognition_widgets(self, show):
		if show:
			self.frame_webcam.grid(column=1, row=0, rowspan=3)
			self.frame_recognition_buttons.grid(column=0, row=2)
		else:
			self.frame_webcam.grid_forget()
			self.frame_recognition_buttons.grid_forget()

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
					color = "black"
				else:
					color = "white"

				# Create rectangle and store its ID
				square_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
				
				# Save the row, col, and coordinates as data for this square
				self.squares[square_id] = (row, col, x1, y1, x2, y2)

				# Bind click event to this rectangle
				self.canvas.tag_bind(square_id, "<Button-1>", self.on_square_click) # button-1 is a left click

	def on_square_click(self, event):
		if (self.window_mode == WindowMode.human_move):
			# Get the ID of the clicked square
			square_id = self.canvas.find_closest(event.x, event.y)[0]
			# Retrieve row, column, and coordinates from the stored dictionary
			row, col, x1, y1, x2, y2 = self.squares[square_id]
			#print(f"Clicked on square ({row},{col})")
			self.controller.human_put_piece(row, col)
				  
	def delete_pieces(self):
		self.canvas.delete("piece")

	def draw_pieces(self, board):
		board_np = np.array(board)
		for i in range(self.BOARDSIZE):
			for j in range(self.BOARDSIZE):
				if board_np[i,j] != 0:
					for value in self.squares.values():
						if value[0] == i and value[1] == j:
							padding = 10
							if board_np[i,j] == 1:
								color = self.color_player_1
							else:
								color = self.color_player_2

							if self.controller.last_move_model == (i,j):
								if self.overruled_last_move:
									self.canvas.create_rectangle(value[2] + padding, value[3] + padding, value[4] - padding, value[5] - padding, fill="dark orange" if color==self.color_player_1 else "light blue" , tags="piece")
								else:
									self.canvas.create_oval(value[2] + padding, value[3] + padding, value[4] - padding, value[5] - padding, fill="dark orange" if color==self.color_player_1 else "light blue" , tags="piece")
							else:
								self.canvas.create_oval(value[2] + padding, value[3] + padding, value[4] - padding, value[5] - padding, fill=color, tags="piece")
		self.update()#prevent flashing

	def draw_scoreboard(self, board, scoreboard):
		self.clear_text_on_canvas()
		if self.draw_scoreboard:
			for i in range(15):
				for j in range(15):
					if board[i][j] == 0:
						key_to_lookup = (i, j)
						for value in self.squares.values():
							if value[0] == i and value[1] == j:
								padding = 20
								if key_to_lookup in scoreboard:
									self.canvas.create_text(value[2]+padding, value[3]+padding, text=f"{scoreboard[key_to_lookup]:.2f}", font=('Helvetica', 12), fill="pink", tags="text")
	   
	def activate_game(self):
		self.close_secondary_windows()

	def show_previous(self):
		"""Show the previous item in the list."""
		if self.controller.current_index >= 0:
			self.delete_pieces()
			self.controller.previous_move()
			self.draw_pieces(self.controller.game_board.board)
		self.update_replay_button_states()

	def show_next(self):
		"""Show the next item in the list."""
		if self.controller.current_index < len(self.controller.moves) - 1:
			self.delete_pieces()
			self.controller.next_move()
			self.draw_pieces(self.controller.game_board.board)
		self.update_replay_button_states()

	def update_replay_button_states(self):
		"""Enable or disable buttons based on the current index."""
		current_index = self.controller.current_index
		self.prev_button.config(state=DISABLED if current_index == -1 else NORMAL)
		self.next_button.config(state=DISABLED if current_index == len(self.controller.moves) - 1 else NORMAL)

	def activate_replay_frame(self):
		self.frame_replay.grid(row=2, column=0, padx=10)  
		self.close_secondary_windows()
		
	def deactivate_replay_frame(self):
		self.frame_replay.grid_forget()

	def close_secondary_windows(self):
		for widget in self.winfo_children():
			if isinstance(widget, Toplevel):
				widget.destroy()
		
	def clear_canvas(self):
		self.canvas.delete("piece")
		self.canvas.delete("line")
		self.canvas.delete("text")
		
	def clear_text_on_canvas(self):
		self.canvas.delete("text")
	
	def draw_line(self, winning_cells): #draws a line through the winning cells
		padding = 25 #cell size= 50, so padding = 25 (the line has to go through the middle of each cell)

		first_cell = winning_cells[0] #start of the line, the list is sorted, form: (x,y)
		last_cell = winning_cells[-1] #end of the line, the list is sorted, form: (x,y)
		for value in self.squares.values():
			if value[0] == first_cell[0] and value[1] == first_cell[1]:
				x1 = value[2] + padding
				y1 = value[3] + padding

			if value[0] == last_cell[0] and value[1] == last_cell[1]:
				x2 = value[4] - padding
				y2 = value[5] - padding

		self.canvas.create_line(x1, y1, x2, y2, fill="white", width=4, tags="line")

	def display_coordinates(self,detected_move):
		self.frame_recognition_buttons.button_move_done.config(text=detected_move)
		self.after(5000,self.frame_recognition_buttons.button_move_done.config(text="Move done?"))

	def end_game(self):
		mb.showinfo("End of the game","There's a winner, "+str(self.controller.get_player(self.controller.game.winner)))

	def show_load_error(self, error):
		print("Please select a valid file, error:",error)
		self.show_error("invalid file",f"Please select a valid file, error:{error}")

	def show_error(self, title, errormessage):
		mb.showerror(title,errormessage)