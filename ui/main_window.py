from tkinter import *
import tkinter.messagebox as mb
import numpy as np
import logging
import enum

from ui.widgets_main_window import frame_recognition_buttons, frame_webcam, label_highest_scoring_moves

from .settings_windows import replay_window, new_game_window, train_window, models_window, physical_play_window, evaluate_window
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
	evaluate = 'evaluate'
	physical_play = 'physical_play'



class GomokuApp(Tk):
	def __init__(self):
		logger.info("Initialize GomokuApp")
		
		super().__init__()

		self.title("Gomoku")
		self.config(background='#357EC7')
		self.bind("<Escape>", lambda e: self.toggle_fullscreen_state(True))
		self.bind("<F11>", lambda e: self.toggle_fullscreen_state())
		self.resizable(True, True)
		self.attributes("-fullscreen", True)

		self.window_mode = WindowMode.pause
		self.game_type = GameType.human_vs_human
		
		# Canvas to draw the chessboard
		self.canvas = Canvas(self, width=750, height=750)
		self.canvas.grid(row=0, column=0, rowspan=2, padx=10,pady=10)

		self.menubar = Menu(self,font=("Helvetica", 12),tearoff=0)
		self.config(menu=self.menubar)

		self.new_game_menu = Menu(self.menubar,tearoff=0)
		self.new_game_menu.add_command(label="Play", command=lambda:self.open_new_window("Play"))
		self.new_game_menu.add_command(label="Play with physical board", command=lambda:self.open_new_window("PhysicalPlay"))
		self.new_game_menu.add_command(label="Train", command=lambda:self.open_new_window("Train"))
		self.new_game_menu.add_command(label="Replay", command=lambda:self.open_new_window("Replay"))
		self.new_game_menu.add_command(label="Evaluate", command=lambda:self.open_new_window("Evaluate"))
		self.menubar.add_cascade(label="New Game",menu=self.new_game_menu)

		self.models_menu = Menu(self.menubar,tearoff=0)
		self.models_menu.add_command(label="models", command=lambda:self.open_new_window("Models"))
		self.menubar.add_cascade(label="Models",menu=self.models_menu)
		
		self.squares = {}
		self.square_size = 50
		
		self.BOARDSIZE = int(config["GAME"]["board_size"])
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

		self.frame_webcam = frame_webcam.FrameWebcam(self)
		self.frame_recognition_buttons = frame_recognition_buttons.FrameRecognitionButtons(self)

		self.label_highest_scoring_moves = label_highest_scoring_moves.LabelHighestScoringMoves(self)
		self.label_highest_scoring_moves.grid(row=3, column=0,pady=2,padx=2)

		self.color_player_1 = "red"
		self.color_player_2 = "blue"
		
		self.overruled_last_move = None

	def toggle_fullscreen_state(self,esc_was_used=False): #esc to exit fullscreen, f11 to enter fullscreen or to exit fullscreen
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
			case "Evaluate":
				new_window = evaluate_window.EvaluateWindow(self)
		
	def hide_unnecessary_widgets(self): #this function is used so the buttons are hided when starting a controller, not when opening a new window. (A user may want to close a window without starting a new game.)
		self.show_replay_buttons(self.last_window_type=="Replay") #show replay buttons when using replay mode
		self.show_recognition_widgets(self.last_window_type=="PhysicalPlay")
		self.show_highest_scores_label(self.last_window_type in ["Play","Train","Evaluate","Replay"])

	def show_highest_scores_label(self,show):
		if show:
			self.label_highest_scoring_moves.grid(row=3, column=0,pady=2,padx=2)
			self.label_highest_scoring_moves.config(text="")
		else:
			self.label_highest_scoring_moves.grid_forget()

	def show_replay_buttons(self,show):
		if show:
			self.activate_replay_frame()
		else:
			self.deactivate_replay_frame()

	def show_recognition_widgets(self, show):
		if show:
			self.frame_webcam.grid(column=1, row=0, rowspan=3)
			self.frame_recognition_buttons.grid(column=0, row=2)
		else:
			self.frame_webcam.grid_forget()
			self.frame_recognition_buttons.grid_forget()

	def create_gomokuboard(self, grid_size):
		self.squares_mapping = {} 
		# Create the squares for the chessboard
		for row in range(grid_size):
			for col in range(grid_size):
				x1 = col * self.square_size
				y1 = row * self.square_size
				x2 = x1 + self.square_size
				y2 = y1 + self.square_size

				# Alternate the colors
				if (row + col) % 2 == 0:
					color = "black"
				else:
					color = "white"

				# Create rectangle and store its ID
				square_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
				
				# Save the row, col, and coordinates as data for this square
				self.squares[square_id] = (row, col, x1, y1, x2, y2)
				self.squares_mapping[(row, col)] = (x1, y1, x2, y2)

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

	def get_piece_color(self,player_id,row,col):
		if self.controller.last_move_model == (row,col):
			return "dark orange" if player_id == 1 else "light blue"#the slightly different colors show the last move of the AI, so it's easier to see
		return self.color_player_1 if player_id == 1 else self.color_player_2

	def draw_pieces(self, board):
		self.delete_pieces() #remove the previous drawing, remove all old pieces
		board_np = np.array(board)
		padding = 10
		for (i, j), piece in np.ndenumerate(board_np):
			if piece != 0:#if the cell is not empty
				x1, y1, x2, y2 = self.squares_mapping[(i, j)]
				color = self.get_piece_color(piece,i,j)
				
				if self.controller.last_move_model == (i, j) and self.overruled_last_move:
					draw_method = self.canvas.create_rectangle #show an overruled move as a square
				else:
					draw_method = self.canvas.create_oval

				draw_method(x1 + padding, y1 + padding, x2 - padding, y2 - padding, fill=color, tags="piece")

		self.update()#prevent flashing

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
		first_cell = winning_cells[0] #start of the line, the list is sorted, form: (x,y)
		last_cell = winning_cells[-1] #end of the line, the list is sorted, form: (x,y)
		x1, y1 = self.squares_mapping[first_cell][:2]
		x2, y2 = self.squares_mapping[last_cell][2:]

		padding = self.square_size/2 #the line has to go through the middle of each cell
		self.canvas.create_line(x1 + padding, y1 + padding, x2 - padding, y2 - padding, fill="white", width=4, tags="line")

	def display_coordinates(self,detected_move):
		self.frame_recognition_buttons.button_move_done.config(text=detected_move)
		self.after(5000,self.frame_recognition_buttons.button_move_done.config(text="Move done?"))

	def end_game(self):
		mb.showinfo("End of the game","There's a winner, "+str(self.controller.get_player(self.controller.game.winner)))

	def end_game_draw(self):
		mb.showinfo("End of the game","The game ended in a draw")

	def show_load_error(self, error):
		print("Please select a valid file, error:",error)
		self.show_error("invalid file",f"Please select a valid file, error:{error}")

	def show_error(self, title, errormessage):
		mb.showerror(title,errormessage)