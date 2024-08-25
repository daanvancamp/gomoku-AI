from ast import Lambda
import random
import sys
from threading import Thread
from time import sleep
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import messagebox as mb

import numpy as np
from utils import filereader,stats
from model_management import modelmanager
from game import gomoku
from UI import game_window
from game import gomoku
from utils.singleton_class import Singleton

WIDTH = 540
HEIGHT = 500

game_instance = gomoku.GomokuGame(filereader.create_gomoku_game("consts.json"))
modelmanager_instance = modelmanager.ModelManager()

distance_from_left_side=10
style_numbers = ["georgia", 10, "white", 12, 2]#font, size, color, bold, underline




class GameSettings(metaclass=Singleton):
	def __init__(self) -> None:
		self.var_game_runs = StringVar()
		self.var_game_runs.set("1")
		self.var_delay = BooleanVar()
		self.var_delay.set(False)
		self.var_log = BooleanVar()
		self.var_log.set(False)
		self.var_rep = BooleanVar()
		self.var_rep.set(True)
		self.replay_path = StringVar()
		self.replay_path.set(r".\data\replays")
		self.var_play_music=BooleanVar()
		self.var_play_music.set(False)
		self.var_show_overruling=BooleanVar()
		self.var_show_overruling.set(True)
		self.var_show_graphs=BooleanVar()
		self.var_show_graphs.set(False)
		self.var_show_dialog=BooleanVar()
		self.var_show_dialog.set(False)
		self.var_use_recognition=BooleanVar()
		self.var_use_recognition.set(False)
		self.var_startingPlayer=StringVar()
		self.var_startingPlayer.set("Player 1")
		self.var_start_from_file=BooleanVar()
		self.var_start_from_file.set(False)
		self.state_board_path=StringVar()
		self.state_board_path.set(r".\test_situations\specific_situation.txt")


class GomokuApp(Tk):
	def __init__(self):
		global Gamesettings
		Tk.__init__(self)
		self.title("Gomoku -- Main Menu")
		self.configure(background="#357EC7")
		self.attributes("-topmost", True)
		self.bind("<Escape>", lambda event: self.quit_program())
		self.bind("<q>", lambda event: self.quit_program())
		self.attributes("-fullscreen", False)#temporarily set to false because it is easier to test
		Gamesettings = GameSettings()

		self.tk_setPalette(background='white', foreground='black',
			   activeBackground='gray', activeForeground='black')

		Thread_maintain_GUI=Thread(target=self.maintain_GUI,daemon=True)#end when main program ends
		Thread_maintain_GUI.start()

		gomoku.player1.var_playerType = StringVar()
		gomoku.player2.var_playerType = StringVar()
		gomoku.player1.var_playerType.set("Human")
		gomoku.player2.var_playerType.set("AI-Model")
		
		gomoku.player1.var_allow_overrule=BooleanVar()
		gomoku.player1.var_allow_overrule.set(True)
		gomoku.player2.var_allow_overrule=BooleanVar()
		gomoku.player2.var_allow_overrule.set(True)
		
		gomoku.player1.var_model=StringVar()
		gomoku.player2.var_model=StringVar()
		gomoku.player1.var_model.set("standaard")
		gomoku.player2.var_model.set("standaard")

		gomoku.player1.var_number_of_training_loops_comboboxes=StringVar()
		gomoku.player1.var_number_of_training_loops_comboboxes.set(0)
		gomoku.player2.var_number_of_training_loops_comboboxes=StringVar()
		gomoku.player2.var_number_of_training_loops_comboboxes.set(0)

		self.frame1 = FramePlay(self)
		self.frame2 = FrameTrain(self)
		self.frame3 = FrameReplay(self)
		self.frame4 = FrameModels(self)
		
		game_instance.Gamewindow = game_window.GameWindow(game_instance,self) #needs to be declared after all the frames are created

		self.menubar=Menu(self)
		self.new_game_menu = Menu(self.menubar,tearoff=0)

		self.new_game_menu.add_command(label="Play", command=lambda:self.add_frame_to_grid(self.frame1))
		self.new_game_menu.add_command(label="Train", command=lambda:self.add_frame_to_grid(self.frame2))
		self.new_game_menu.add_command(label="Replay", command=lambda:self.add_frame_to_grid(self.frame3))

		self.menubar.add_cascade(label="New Game",menu=self.new_game_menu)

		self.models_menu=Menu(self.menubar,tearoff=0)
		self.models_menu.add_command(label="models", command=lambda:self.add_frame_to_grid(self.frame4))

		self.menubar.add_cascade(label="Models",menu=self.models_menu)
		self.config(menu=self.menubar)


	def set_player_type(self,player_id):
			if player_id == 1:
				newtype = gomoku.player1.var_playerType.get()
			else:
				newtype = gomoku.player2.var_playerType.get()
			gomoku.players[player_id-1].TYPE=newtype

	def quit_program(self):
		print("quitting game")
		sys.exit() #end the program

	def add_frame_to_grid(self,frame):
		game_instance.Gamewindow.stop_game()
		self.remove_all_widgets()
		frame.grid(row=0,column=0)

	def remove_all_widgets(self):
		try:
			self.frame1.grid_remove()
			self.frame2.grid_remove()
			self.frame3.grid_remove()
			self.frame4.grid_remove()
			game_instance.Gamewindow.grid_remove()
		except Exception as e:
			pass
		
		#todo: determine why this code doesn't work. The above code seems to work.
		# for widget in self.winfo_children():
		# 	if widget.winfo_ismapped():  # Controleer of de widget zichtbaar is
		# 		widget.grid_remove()


	def browse_state_files(self):
		file_path = filedialog.askopenfilename(filetypes=[("txt File", "*.txt")],initialdir=r".\test_situations")
		Gamesettings.state_board_path.set(file_path)

	def browse_files(self):
		file_path = filedialog.askopenfilename(filetypes=[("Json File", "*.json")],initialdir=r".\data\replays")
		Gamesettings.replay_path.set(file_path)
   
	def run(self):
		gomoku.run(game_instance)

	def load_board_from_file(self)->list[list[int]]:
		try:
			with open(Gamesettings.state_board_path.get(), "r") as file:
				board = [[0] * 15 for _ in range(15)] # 0 = empty, 1 = player 1, 2 = player 2.
				for row in range(15):
					line = file.readline().replace("\n", "").replace(" ", "") # remove \n and spaces
					for col in range(15):      
						board[row][col]=int(line[col])
						if int(line[col]) not in [0, 1, 2]:
							return None
			print("board loaded")
			return board
		except:
			return None


	def start_new_game(self):
		global game_instance
		filereader.log_info_overruling("\n\n\nnew session begins:")
		self.add_frame_to_grid(game_instance.Gamewindow)
		game_instance.use_recognition = Gamesettings.var_use_recognition.get()
		game_instance.play_music = Gamesettings.var_play_music.get()
		game_instance.show_overruling = Gamesettings.var_show_overruling.get()
		game_instance.record_replay = Gamesettings.var_rep.get()
		game_instance.show_dialog = Gamesettings.var_show_dialog.get()
		if game_instance.use_recognition:
			game_instance.P1COL = "red"
			game_instance.P2COL = "blue"

		game_instance.ai_delay = Gamesettings.var_delay.get()
		stats.should_log = Gamesettings.var_log.get()
	
		
		gomoku.player1.TYPE=gomoku.player1.var_playerType.get()
		gomoku.player2.TYPE=gomoku.player2.var_playerType.get()

		if (gomoku.player1.TYPE=="Human" or gomoku.player2.TYPE=="Human") and not game_instance.use_recognition:
			game_instance.show_hover_effect=True
		else:
			game_instance.show_hover_effect=False

		stats.setup_logging(gomoku.player1.TYPE, gomoku.player2.TYPE)

		if gomoku.player1.TYPE == "AI-Model":
			gomoku.player1.load_model(gomoku.player1.var_model.get())
			gomoku.player1.set_allow_overrule(gomoku.player1.var_allow_overrule.get())
		if gomoku.player2.TYPE == "AI-Model":
			gomoku.player2.load_model(gomoku.player2.var_model.get())
			gomoku.player2.set_allow_overrule(gomoku.player2.var_allow_overrule.get())

		if Gamesettings.var_startingPlayer.get() == "Player 1":
			gomoku.current_player = gomoku.player1
		else:
			gomoku.current_player = gomoku.player2
		
		valid_number = False

		while not valid_number:
			try:
				runs = int(Gamesettings.var_game_runs.get())
				valid_number=True
			except:
				print("invalid number, try again")

		game_instance.game_mode=game_instance.game_modes[0]
		game_instance.Gamewindow.restart_game_window()
		for i in range(runs):
			filereader.log_info_overruling("run "+str(i+1)+" begins:")
			stats.log_message(f"Game  {i+1} begins.")

			game_instance.current_game = i+1
			game_instance.last_round = (i+1 == runs)
			board_loaded=None
			if Gamesettings.var_start_from_file.get():
				board = self.load_board_from_file()
				if board is not None:
					board_loaded=True
				else:
					self.label_unvalid_file.config(text="Board file not valid, try again with another file.")
					board_loaded=False
				game_instance.set_board(board)

			if (board_loaded and Gamesettings.var_start_from_file.get()) or (not Gamesettings.var_start_from_file.get()):
				try:
					
					gomoku.runGame(game_instance, i) #main function
					if game_instance.stop_game:
						break
				except Exception as e:
					print("error in gomoku.run")
					raise Exception("There is an error in the main function/loop, it can be anything." , str(e))
			else:
				print("Please select a valid file that contains the board in the following format and try again:")
				example_board=""
				for i in range(15):
					for b in range(15):
						print(random.randint(0,2), end="")
						example_board+=str(random.randint(0,2))
					print("\n",end="")
				print("The board can only contain 0, 1, or 2. 0 = empty, 1 = player 1, 2 = player 2.")

				mb.showerror(message=example_board, title="Invalid board file, try again",detail="The board can only contain 0, 1, or 2. 0 = empty, 1 = player 1, 2 = player 2.")

				break
		self.game_over()

	def start_new_training(self):
		global game_instance
		filereader.log_info_overruling("\n\n\nnew session begins:")
		self.add_frame_to_grid(game_instance.Gamewindow)

		game_instance.use_recognition = False
		game_instance.play_music = False
		game_instance.show_overruling=False
		game_instance.record_replay=True
		game_instance.show_graphs=Gamesettings.var_show_graphs.get()

		gomoku.player1.TYPE="AI-Model"
		gomoku.player2.TYPE=gomoku.player2.var_playerType.get()
	
		if gomoku.player1.TYPE=="Human" or gomoku.player2.TYPE=="Human":
			game_instance.show_hover_effect=True
		else:
			game_instance.show_hover_effect=False

		gomoku.player1.load_model(gomoku.player1.var_model.get())#player 1 is always an AI-Model when training
		gomoku.player1.set_allow_overrule(gomoku.player1.var_allow_overrule.get())

		if gomoku.player2.TYPE == "AI-Model":
			gomoku.player2.load_model(gomoku.player2.var_model.get())
			gomoku.player2.set_allow_overrule(gomoku.player2.var_allow_overrule.get())

		if Gamesettings.var_startingPlayer.get() == "Player 1":
			gomoku.current_player = gomoku.player1
		else:
			gomoku.current_player = gomoku.player2


		try:
			valid_number = False
			while not valid_number:
				try:
					runs = int(Gamesettings.var_game_runs.get())
					valid_number=True
				except:
					print("invalid number, try again")

			game_instance.ai_delay = False #never wait when training
			stats.should_log = Gamesettings.var_log.get()
			stats.setup_logging(gomoku.player1.TYPE, gomoku.player2.TYPE)

			game_instance.game_mode=game_instance.game_modes[1]
			game_instance.Gamewindow.restart_game_window()

			for i in range(runs):
				filereader.log_info_overruling("run "+str(i+1)+" begins:")
			
				stats.log_message(f"Game  {i+1} begins.")
				game_instance.current_game = i+1
				game_instance.last_round = (i+1 == runs)
				try:
					gomoku.run_training(game_instance, i) #main function
					if game_instance.stop_game:
						break
				except Exception as e:
					print("error in gomoku.run, herschrijf die functie.")
					raise Exception("There is an error in the main function/loop, it can be anything." , str(e))

				if gomoku.player1.TYPE == "AI-Model":
					#gomoku.player1 is an object of the class Player, ai is an object of the class gomokuAI and ai.decrease_learning_rate() is a method of the class gomokuAI
					gomoku.player1.ai.decrease_learning_rate()#todo: calculate decrease rate based on number of training rounds
					gomoku.player1.AI_model.log_number_of_training_loops(gomoku.player2.TYPE)
				if gomoku.player2.TYPE == "AI-Model":
					#gomoku.player2 is an object of the class Player, ai is an object of the class gomokuAI and ai.decrease_learning_rate() is a method of the class gomokuAI
					gomoku.player2.ai.decrease_learning_rate()
					gomoku.player2.AI_model.log_number_of_training_loops(gomoku.player1.TYPE)
					#arguments: model_name, number_of_additional_training_loops, opponent
			  
		except ValueError:
			print("Most likely: Game runs value invalid, try again.")
		print("game over")
		self.game_over()


	def start_new_replay(self):
		global game_instance
		game_instance.show_hover_effect=False
		game_instance.show_dialog = Gamesettings.var_show_dialog.get()
		self.add_frame_to_grid(game_instance.Gamewindow)


		filereader.log_info_overruling("\n\n\nnew session begins:")
   
		moves = filereader.load_replay(Gamesettings.replay_path.get())

		if moves is None:
			replay_loaded=False
		else:
			replay_loaded=True
	
		if replay_loaded:
			self.label_info_replay_file_loaded.config(text="Replay file succesfully loaded",fg="green")

			game_instance.use_recognition = False
			game_instance.play_music = False

			gomoku.player1.TYPE = "Replay"
			gomoku.player2.TYPE = "Replay"

			gomoku.current_player = gomoku.player1

			game_instance.ai_delay = Gamesettings.var_delay.get()
			stats.should_log = Gamesettings.var_log.get()
			stats.setup_logging(gomoku.player1.TYPE, gomoku.player2.TYPE)

			game_instance.game_mode=game_instance.game_modes[2]
			game_instance.Gamewindow.restart_game_window()

			try:
				gomoku.run_replay(game_instance,moves) #main function
			except Exception as e:
				print("error in gomoku.run, herschrijf die functie.")
				raise Exception("There is an error in the main function/loop, it can be anything." , str(e)) 
		else:
			print("Try again, please select a valid json file and make sure that it's not opened")
			self.label_info_replay_file_loaded.config(text="Try again, please select a valid json file and make sure that it's not opened in another program",fg="red")
			mb.showerror("Try again, please select a valid json file",message="Please close the file if it is opened in another program")
		self.game_over()

	def game_over(self):
		global game_instance
		game_instance.current_game = 0
		if game_instance.quit_program:
			self.quit_program()

	def create_new_model(self):
		modelmanager_instance.create_new_model(self.var_name_model.get())
		self.refresh_models()
		self.refresh_training_stats()

	def delete_model(self):
		global last_selected_model
		for i in self.Lb1.curselection():
			modelmanager_instance.delete_model(self.Lb1.get(i))
		self.refresh_models()
		last_selected_model=self.Lb1.get(0)
		self.refresh_training_stats()
		
	def reset_all_stats(self):
		global last_selected_model
		for i in self.Lb1.curselection():
			modelmanager_instance.get_model(self.Lb1.get(i)).reset_stats(True)
		if self.Lb1.curselection()==():
			modelmanager_instance.get_model(last_selected_model).reset_stats(True)
		self.refresh_models()
		self.refresh_training_stats()

	def reset_end_states(self):
		global last_selected_model
		for i in self.self.Lb1.curselection():
			modelmanager_instance.get_model(self.Lb1.get(i)).reset_end_states()
		if self.self.Lb1.curselection()==():
			modelmanager_instance.get_model(last_selected_model).reset_end_states()
		self.refresh_models()
		self.refresh_training_stats()

	def refresh_models(self):
		self.self.Lb1.delete(0,END)
		i = 0
		models = modelmanager_instance.get_list_models()
		for model in models:
			self.Lb1.insert(i, model)
			i+=1
		self.CbModel1.configure(values=models)
		self.CbModel2.configure(values=models)
		self.CbModelTrain1.configure(values=models)
		self.CbModelTrain2.configure(values=models)

	def quit_program(self):
		sys.exit()#end the program

	def maintain_GUI(self):
		#add delay to this loop if the program stutters or crashes on your computer
		tab_text = "Play gomoku"
		last_value_repvar=True
		last_value_load_board_from_file=False
		while True:
			sleep(1)
			while not game_instance.running:
				try:

					old_tab_text= tab_text
					current_tab = self.tabControl.index(self.tabControl.select())
					tab_text = self.tabControl.tab(current_tab, "text")
					if tab_text=="Train" and old_tab_text!=tab_text:
						self.game_instance.var_game_runs.set("3000")
					elif tab_text=="Play gomoku" and old_tab_text!=tab_text:
						self.game_instance.var_game_runs.set("1")
						self.var_delay.set(False)
					elif tab_text=="Replay old games" and old_tab_text!=tab_text:
						self.var_delay.set(True)

					if tab_text=="Train":
						self.label_shortcuts.config(text="In game shortcuts: esc = return to this menu, q = terminate program")
					elif tab_text=="Replay old games":
						self.label_shortcuts.config(text="In game shortcuts: esc = return to this menu, q = terminate program")
					elif tab_text=="Play gomoku":
						self.label_shortcuts.config(text="In game shortcuts: esc = return to this menu, q = terminate program , space = skip the current round")

					##TAB 1##
					if gomoku.player1.var_playerType.get() == "Human" and gomoku.player2.var_playerType.get() == "Human":
						self.var_log.set(False)
						self.var_rep.set(False)
						self.logbutton.config(state=DISABLED)
						self.replaybutton.config(state=DISABLED)
					else:
						self.logbutton.config(state=NORMAL)
						self.replaybutton.config(state=NORMAL)


					if gomoku.player1.var_playerType.get()=="AI-Model":
						self.CbModel1.config(state="readonly")
						self.overrule_button_player_1.config(state=NORMAL)
						self.label_value_number_of_training_loops_p1.config(state=NORMAL)

					else:
						self.CbModel1.config(state=DISABLED)
						self.overrule_button_player_1.config(state=DISABLED)
						self.label_value_number_of_training_loops_p1.config(state=DISABLED)

					if gomoku.player2.var_playerType.get()=="AI-Model":
						self.CbModel2.config(state="readonly")
						self.overrule_button_player_2.config(state=NORMAL)
						self.overrule_button_player_2_tab2.config(state=NORMAL)
						self.label_value_number_of_training_loops_p2.config(state=NORMAL)
					else:
						self.CbModel2.config(state=DISABLED)
						self.overrule_button_player_2.config(state=DISABLED)
						self.overrule_button_player_2_tab2.config(state=DISABLED)
						self.label_value_number_of_training_loops_p2.config(state=DISABLED)

					if self.var_start_from_file.get():
						self.label_load_state.grid()
						self.load_state_entry.grid()
						self.button_browse_state_file.grid()
					else:
						self.label_load_state.grid_remove()
						self.load_state_entry.grid_remove()
						self.button_browse_state_file.grid_remove()
		
					recognition_possible=(gomoku.player1.var_playerType.get()=="Human" or gomoku.player2.var_playerType.get()=="Human")and (gomoku.player1.var_playerType.get()=="AI-Model" or gomoku.player2.var_playerType.get()=="AI-Model" or gomoku.player1.var_playerType.get()=="Test Algorithm" or gomoku.player2.var_playerType.get()=="Test Algorithm")
					if recognition_possible and not self.var_start_from_file.get():
						self.use_recognition_button.config(state=NORMAL)
						self.label_recognition.config(state=NORMAL)
					else:
						self.use_recognition_button.config(state=DISABLED)
						self.label_recognition.config(state=DISABLED)
					#tab 1, delaybutton#
					if (gomoku.player1.var_playerType.get()=="AI-Model" or gomoku.player2.var_playerType.get()=="AI-Model" ) or (gomoku.player1.var_playerType.get()=="Test Algorithm" or gomoku.player2.var_playerType.get()=="Test Algorithm"):
						self.delaybutton.config(state=NORMAL)
					else:
						self.delaybutton.config(state=DISABLED)
					#tab1, music button#
					if gomoku.player1.var_playerType.get()=="Human" or gomoku.player2.var_playerType.get()=="Human":
						self.music_button.config(state=NORMAL)
					else:
						self.music_button.config(state=DISABLED)

					#starting player
					if gomoku.player1.var_playerType.get()==gomoku.player2.var_playerType.get() and gomoku.player1.var_playerType=="Test Algorithm": #option not relevant
						self.playerstartLabel.config(state=DISABLED)
						self.CbStartingPlayer.config(state=DISABLED)
					else:
						self.playerstartLabel.config(state="normal")
						self.CbStartingPlayer.config(state="readonly")

					if self.var_start_from_file.get()!=last_value_load_board_from_file and self.var_start_from_file.get()==True:
						self.var_rep.set(False) #can't be used simultanously because if you would save a replay file, it wouldn't be complete (the moves that are loaded are gone)
			
						last_value_load_board_from_file=self.var_start_from_file.get()
						last_value_repvar=self.var_rep.get()

					if self.var_rep.get()!=last_value_repvar and self.var_rep.get()==True:
						self.var_start_from_file.set(False)

						last_value_load_board_from_file=self.var_start_from_file.get()
						last_value_repvar=self.var_rep.get()

					list_artificial_players=["AI-Model","Test Algorithm"]
					if gomoku.player1.var_playerType.get() not in list_artificial_players and gomoku.player2.var_playerType.get() not in list_artificial_players:
						self.button_show_overruling.config(state=NORMAL)
					else:
						self.button_show_overruling.config(state=DISABLED)

					if not self.var_rep.get() and not self.var_start_from_file.get():
						self.label_info_load_save_replay.config(state=DISABLED)
					else:
						self.label_info_load_save_replay.config(state=NORMAL)

					if gomoku.player2.var_playerType.get()=="Human":
						self.train_description.config(state=DISABLED) #a human will never play the game 3000 times to train the model
					else:
						self.train_description.config(state=NORMAL)

					if gomoku.player2.var_playerType.get()=="AI-Model":
						self.CbModelTrain2.config(state="readonly")
						self.label_value_number_of_training_loops_tab2_p2.config(state=NORMAL)
					else:
						self.CbModelTrain2.config(state=DISABLED)
						self.label_value_number_of_training_loops_tab2_p2.config(state=DISABLED)

					self.show_number_of_training_loops_comboboxes()
					self.refresh_training_stats()
				except Exception as e:
					pass

	def refresh_training_stats(self):
		global last_selected_model #used to keep track of which model is selected, because it is unselected when selecting something in the  combobox
		try:
			for i in self.self.Lb1.curselection():
				last_selected_model=self.self.Lb1.get(i)

			model_class=modelmanager_instance.get_model(last_selected_model)
			self.var_number_of_training_loops.set(f"{model_class.get_number_of_training_loops("training loops")} (against H:{model_class.get_number_of_training_loops("training loops against Human")}, T'A':{model_class.get_number_of_training_loops("training loops against Test Algorithm")}, AI:{model_class.get_number_of_training_loops("training loops against AI-Model")} )")

			if self.Cb_choose_stats.get()== "Total":
				self.var_losses.set(model_class.get_number_of_losses("total end stats"))
				self.var_wins.set(model_class.get_number_of_wins("total end stats"))
				self.var_ties.set(model_class.get_number_of_ties("total end stats"))
			elif self.Cb_choose_stats.get()== "Games":
				self.var_losses.set(model_class.get_number_of_losses("games end stats"))
				self.var_wins.set(model_class.get_number_of_wins("games end stats"))
				self.var_ties.set(model_class.get_number_of_ties("games end stats"))
			elif self.Cb_choose_stats.get()== "Training":
				self.var_losses.set(model_class.get_number_of_losses("training loops end stats"))
				self.var_wins.set(model_class.get_number_of_wins("training loops end stats"))
				self.var_ties.set(model_class.get_number_of_ties("training loops end stats"))
	
			total_sum=self.var_losses.get()+self.var_ties.get()+self.var_wins.get()
			if total_sum>0:
				for relative_value,value in zip([self.var_relative_value_losses,self.var_relative_value_wins,self.var_relative_value_ties],[self.var_losses,self.var_wins,self.var_ties]):
					relative_value.set(str(np.round(((value.get()/total_sum)*100),2))+"%")  
			else:
				self.var_relative_value_losses.set("N/A")
				self.var_relative_value_wins.set("N/A")
				self.var_relative_value_ties.set("N/A")
		except Exception as e:
			pass

	def show_number_of_training_loops_comboboxes(self):
		gomoku.player1.var_number_of_training_loops_comboboxes.set("training loops: "+str(modelmanager_instance.get_model(gomoku.player1.var_model.get()).get_number_of_training_loops("training loops")))
	
		gomoku.player2.var_number_of_training_loops_comboboxes.set("training loops: "+str(modelmanager_instance.get_model(gomoku.player2.var_model.get()).get_number_of_training_loops("training loops")))
	

	# style2=ttk.Style()
	# style2.configure("TButton", font=(self.style_numbers[0], self.style_numbers[1]),bg=self.style_numbers[2],ipadx=self.style_numbers[3],ipady=self.style_numbers[4],pady=15)#font=georgia, size=10;bg=white
	# style2.configure("TRadiobutton",fg="white",bg="green")
	# style2.configure("TEntry",fg="white",bg="green")
	# style2.configure("TLabel", font=(self.style_numbers[0], self.style_numbers[1]),fg="white",bg="green")#font=georgia, size=10
	# style2.configure("TCheckbutton", font=(self.style_numbers[0], self.style_numbers[1]),fg="white",bg="green")#font=georgia, size=10

def set_game_instance(new_instance):
	global game_instance
	game_instance = new_instance

class FramePlay (Frame,GomokuApp):#the methods of gomokuapp need to be callable from the frame
	def __init__(self, master):
		super().__init__(master,width=WIDTH,height=HEIGHT)

		self.button_1 = Button(self, text="New Game", command=self.start_new_game)
		self.button_1.grid(row=0, column=0, sticky="w", padx=distance_from_left_side)
		self.checkbox_show_dialog=Checkbutton(self, text="Show dialog before starting next game", variable=Gamesettings.var_show_dialog)
		self.checkbox_show_dialog.grid(row=0, column=1, sticky="w")

		self.player1typelabel = Label(self, text="Player 1(black)")
		self.player1typelabel.grid(row=2, column=0, sticky="w", padx=distance_from_left_side)
		self.player2typelabel = Label(self, text="Player 2(white)")
		self.player2typelabel.grid(row=2, column=1, sticky="w", padx=distance_from_left_side)

		self.radiobutton1 = Radiobutton(self, text="Human", variable=gomoku.player1.var_playerType, value="Human", command=lambda: self.set_player_type(0))
		self.radiobutton1.grid(row=3, column=0, sticky="w", padx=distance_from_left_side)
		self.radiobutton2 = Radiobutton(self, text="Test Algorithm", variable=gomoku.player1.var_playerType, value="Test Algorithm", command=lambda: self.set_player_type(0))
		self.radiobutton2.grid(row=4, column=0, sticky="w", padx=distance_from_left_side)
		self.radiobutton3 = Radiobutton(self, text="AI-Model", variable=gomoku.player1.var_playerType, value="AI-Model", command=lambda: self.set_player_type(0))
		self.radiobutton3.grid(row=5, column=0, sticky="w", padx=distance_from_left_side)

		self.radiobutton4 = Radiobutton(self, text="Human", variable=gomoku.player2.var_playerType, value="Human", command=lambda: self.set_player_type(1))
		self.radiobutton4.grid(row=3, column=1, sticky="w")
		self.radiobutton5 = Radiobutton(self, text="Test Algorithm", variable=gomoku.player2.var_playerType, value="Test Algorithm", command=lambda: self.set_player_type(1))
		self.radiobutton5.grid(row=4, column=1, sticky="w")
		self.radiobutton6 = Radiobutton(self, text="AI-Model", variable=gomoku.player2.var_playerType, value="AI-Model", command=lambda: self.set_player_type(1))
		self.radiobutton6.grid(row=5, column=1, sticky="w")

		self.CbModel1 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player1.var_model)
		self.CbModel2 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player2.var_model)

		self.CbModel1.grid(row=6, column=0, sticky="w",padx=distance_from_left_side)
		self.CbModel2.grid(row=6, column=1,sticky="w",padx=distance_from_left_side)

		self.label_value_number_of_training_loops_p1 = Label(self, textvariable=gomoku.player1.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_p1.grid(row=8, column=0, sticky="w",padx=distance_from_left_side)

		self.label_value_number_of_training_loops_p2 = Label(self, textvariable=gomoku.player2.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_p2.grid(row=8, column=1, sticky="w")


		self.overrule_button_player_1=Checkbutton(self, text="Allow overrule", variable=gomoku.player1.var_allow_overrule)
		self.overrule_button_player_1.grid(row=9, column=0, sticky="w",padx=distance_from_left_side)

		self.overrule_button_player_2=Checkbutton(self, text="Allow overrule", variable=gomoku.player2.var_allow_overrule)
		self.overrule_button_player_2.grid(row=9, column=1, sticky="w")


		self.gamerunslabel = Label(self, text="Number of games: ")
		self.gamerunslabel.grid(row=10, column=0, sticky="w",padx=distance_from_left_side)
		self.gamerunsentry = Entry(self, textvariable=Gamesettings.var_game_runs)
		self.gamerunsentry.grid(row=10, column=1, sticky="w")


		self.playerstartLabel = Label(self, text="Player to start: ")
		self.playerstartLabel.grid(row=11, column=0, sticky="w", padx=distance_from_left_side)
		self.CbStartingPlayer = Combobox(self, state="readonly", values=["Player 1", "Player 2"], textvariable=Gamesettings.var_startingPlayer)
		self.CbStartingPlayer.current(0)
		self.CbStartingPlayer.grid(row=11, column=1, sticky="w")

		#column 0
		self.logbutton = Checkbutton(self, text="Create log file", variable=Gamesettings.var_log) 
		self.logbutton.grid(row=12, column=0, sticky="w",padx=distance_from_left_side)
		self.replaybutton = Checkbutton(self, text="Save replays(1)", variable=Gamesettings.var_rep) 
		self.replaybutton.grid(row=13, column=0, sticky="w",padx=distance_from_left_side)
		self.delaybutton = Checkbutton(self, text="Use AI Delay", variable=Gamesettings.var_delay)
		self.delaybutton.grid(row=14, column=0, sticky="w",padx=distance_from_left_side)

		#column1
		self.music_button=Checkbutton(self, text="Play music", variable=Gamesettings.var_play_music)
		self.music_button.grid(row=12, column=1, sticky="w")
		self.button_show_overruling=Checkbutton(self, text="Show overruling", variable=Gamesettings.var_show_overruling)
		self.button_show_overruling.grid(row=13, column=1, sticky="w")
		self.use_recognition_button=Checkbutton(self, text="use recognition(in development)*", variable=Gamesettings.var_use_recognition)
		self.use_recognition_button.grid(row=14, column=1, sticky="w")


		self.label_recognition=Label(self, text="*only turn on when you have a physical board, a webcam and the other repository.",wraplength=WIDTH-15)
		self.label_recognition.grid(row=15, column=0, sticky="w",columnspan=2, padx=distance_from_left_side)


		self.bottomframe = Frame(self, highlightbackground="blue", highlightthickness=3, borderwidth=1)
		self.bottomframe.grid(row=16, column=0, sticky="w",columnspan=3, padx=distance_from_left_side, pady=15)

		self.start_from_file_button=Checkbutton(self.bottomframe, text="Load game situation(2)", variable=Gamesettings.var_start_from_file)
		self.start_from_file_button.grid(row=0, column=0, sticky="w")
		self.label_unvalid_file=Label(self.bottomframe, text="")
		self.label_unvalid_file.grid(row=0, column=1, sticky="e",columnspan=2)

		self.label_load_state=Label(self.bottomframe, text="Choose file board state: ")
		self.label_load_state.grid(row=1, column=0, sticky="w")
		self.load_state_entry = Entry(self.bottomframe, textvariable=Gamesettings.state_board_path, width=50)
		self.load_state_entry.grid(row=2, column=0, sticky="w",columnspan=2)
		self.button_browse_state_file = Button(self.bottomframe, text="...", command=lambda: self.browse_state_files())
		self.button_browse_state_file.grid(row=2, column=2, sticky="w")
		
		self.label_info_load_save_replay=Label(self,wraplength=WIDTH-15, text="(1)(2)The save replay function can't be used when loading a board, because that would create a wrong replay file.")
		self.label_info_load_save_replay.grid(row=17, column=0, sticky="w",columnspan=2,pady=5,padx=distance_from_left_side)

class FrameTrain(Frame, GomokuApp):
	def __init__(self, master):
		super().__init__(master,width=WIDTH, height=HEIGHT)
		#row 0
		self.button_2 = Button(self, text="Train", command=lambda: self.start_new_training())
		self.button_2.grid(row=0, column=1, sticky="e")

		#column 0
		self.label_model=Label(self, text="AI-Model: ")
		self.label_model.grid(row=1, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		self.CbModelTrain1 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player1.var_model)
		self.CbModelTrain1.grid(row=2, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		self.label_value_number_of_training_loops_tab2_p1 =Label(self, textvariable=gomoku.player1.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_tab2_p1.grid(row=3, column=0, sticky="w",padx=distance_from_left_side,pady=1)
		self.overrule_button_player_1_tab2=Checkbutton(self, text="Allow overrule", variable=gomoku.player1.var_allow_overrule)
		self.overrule_button_player_1_tab2.grid(row=7, column=0, sticky="w",padx=distance_from_left_side)


		self.train_opponent_label = Label(self, text="Train model against:")
		self.train_opponent_label.grid(row=1, column=1, sticky="w")

		self.human_training_button=Radiobutton(self, text="Human", variable=gomoku.player2.var_playerType, value="Human")
		self.human_training_button.grid(row=2, column=1,sticky="w")
		self.radiobutton7 = Radiobutton(self, text="Test Algorithm", variable=gomoku.player2.var_playerType, value="Test Algorithm")
		self.radiobutton7.grid(row=3, column=1, sticky="w")
		self.radiobutton8 = Radiobutton(self, text="AI-Model", variable=gomoku.player2.var_playerType, value="AI-Model")
		self.radiobutton8.grid(row=4, column=1, sticky="w")

		self.CbModelTrain2 = Combobox(self, state="readonly", values=modelmanager_instance.list_models,textvariable=gomoku.player2.var_model)
		self.CbModelTrain2.grid(row=5, column=1, sticky="w")
		self.label_value_number_of_training_loops_tab2_p2 = Label(self, textvariable=gomoku.player2.var_number_of_training_loops_comboboxes)
		self.label_value_number_of_training_loops_tab2_p2.grid(row=6, column=1, sticky="w")
		self.overrule_button_player_2_tab2=Checkbutton(self, text="Allow overrule", variable=gomoku.player2.var_allow_overrule)
		self.overrule_button_player_2_tab2.grid(row=7, column=1, sticky="w")

		self.gamerunslabel = Label(self, text="Number of games: ")
		self.gamerunslabel.grid(row=8, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.gamerunsentry2 = Entry(self, textvariable=Gamesettings.var_game_runs)
		self.gamerunsentry2.grid(row=9, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.replaybutton2 = Checkbutton(self, text="Save replays", variable=Gamesettings.var_rep)
		self.replaybutton2.grid(row=10, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.show_graphs_checkbutton=Checkbutton(self, text="Show graphs*", variable=Gamesettings.var_show_graphs)
		self.show_graphs_checkbutton.grid(row=11, column=0, sticky="w",pady=2,padx=distance_from_left_side)

		self.train_description = Label(self, text="It is recommended to run at least 3 000 games per training session.", font=(style_numbers[0], style_numbers[1]), wraplength=WIDTH-15)
		self.train_description.grid(row=12, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

		self.info_show_graphs=Label(self, text="*Don't forget to MANUALLY close the graphs at the end of each training session if you enable it.",foreground="red",wraplength=WIDTH-15)
		self.info_show_graphs.grid(row=13, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

class FrameReplay(Frame,GomokuApp):
	def __init__(self, master):
		super().__init__(master,width=WIDTH,height=HEIGHT)

		self.replaylabel = Label(self, text="Choose the replay file: ")
		self.replaylabel.grid(row=0, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.replayentry = Entry(self, textvariable=Gamesettings.replay_path, width=30)
		self.replayentry.grid(row=1, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.button_4 = Button(self, text="...", command=lambda: self.browse_files())
		self.button_4.grid(row=1, column=1, sticky="w")
		self.delaybutton2 = Checkbutton(self, text="Use AI Delay", variable=Gamesettings.var_delay)
		self.delaybutton2.grid(row=2, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.button_5 = Button(self, text="Play", command=lambda: self.start_new_replay())
		self.button_5.grid(row=3, column=0, sticky="w",pady=2,padx=distance_from_left_side)

		self.label_info_replay_file_loaded=Label(self, text="",foreground="red",wraplength=WIDTH-20,font=(style_numbers[0],style_numbers[1]))
		self.label_info_replay_file_loaded.grid(row=4, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

class FrameModels(Frame,GomokuApp):
	def __init__(self,master):
		super().__init__(master,width=WIDTH,height=HEIGHT)

		#todo: the values aren't displayed correctly, fix this

		self.var_losses=IntVar()
		self.var_losses.set(0)
		self.var_wins=IntVar()
		self.var_wins.set(0)
		self.var_ties=IntVar()
		self.var_ties.set(0)

		self.var_relative_value_losses = StringVar()
		self.var_relative_value_losses.set("0%")

		self.var_relative_value_wins = StringVar()
		self.var_relative_value_wins.set("0%")

		self.var_relative_value_ties = StringVar()
		self.var_relative_value_ties.set("0%")

		self.var_choose_stats = StringVar()

		self.var_name_model = StringVar()

		self.var_number_of_training_loops=StringVar()
		self.var_number_of_training_loops.set("0 (against H:0,T'A':0, AI:0 )")


		self.Lb1 = Listbox(self)

		models = modelmanager_instance.get_list_models()
		i  = 0
		for model in models:
			self.Lb1.insert(i, model.split('\\')[-1])
			i+=1
		self.Lb1.grid(row=0, column=2,padx=distance_from_left_side)

		if "standaard" in models or "Standaard" in models:
			for item in models:
				if item=="standaard"or item=="Standaard":
					self.Lb1.selection_set(models.index(item))
					self.Lb1.activate(models.index(item))
					last_selected_model=item
		else:
			self.Lb1.selection_set(0)
			self.Lb1.activate(0)
			last_selected_model=models[0]

		self.frame_buttons=Frame(self)
		self.frame_buttons.grid(row=0, column=0, columnspan=2,sticky='e')

		self.button_NewModel = Button(self.frame_buttons, text="Make New Model",  command=lambda: self.create_new_model())
		self.button_NewModel.grid(row=0, column=1,sticky="n",pady=2,padx=distance_from_left_side)
		self.nameModelLabel = Label(self.frame_buttons, text="Name of model: ")
		self.nameModelLabel.grid(row=1, column=0, sticky="w",pady=2,padx=distance_from_left_side)
		self.nameModelEntry = Entry(self.frame_buttons, textvariable=self.var_name_model)
		self.nameModelEntry.grid(row=1, column=1, sticky="w",pady=2,padx=distance_from_left_side)
		self.nameModelEntry.bind("<Return>",lambda event: self.create_new_model())#push enter to create a new model (easier)

		self.button_DeleteModel = Button(self.frame_buttons, text="Delete Model",  command=lambda: self.delete_model())
		self.button_DeleteModel.grid(row=0, column=0,sticky="n")

		self.label_number_of_training_loops = Label(self, text="Training loops: ")
		self.label_number_of_training_loops.grid(row=4, column=0, sticky="w",padx=(distance_from_left_side,0),pady=(30,10))
		self.label_value_number_of_training_loops_tab4 = Label(self, textvariable=self.var_number_of_training_loops)
		self.label_value_number_of_training_loops_tab4.grid(row=4, column=1, sticky="w",pady=(30,10))

		self.stats_list=["Total","Games","Training"]
		self.Cb_choose_stats= Combobox(self, state="readonly", values=self.stats_list, textvariable=self.var_choose_stats)
		self.Cb_choose_stats.current(0)
		self.Cb_choose_stats.grid(row=5, column=0, sticky="w",pady=2,padx=distance_from_left_side)


		self.label_losses=Label(self, text="Losses: ")
		self.label_losses.grid(row=6, column=0, sticky="w")
		self.label_value_losses_tab4 = Label(self, textvariable=self.var_losses)
		self.label_value_losses_tab4.grid(row=6, column=1, sticky="w")
		self.label_relative_value_losses=Label(self, textvariable=self.var_relative_value_losses)
		self.label_relative_value_losses.grid(row=6, column=2, sticky="w")

		self.label_wins=Label(self, text="Wins: ")
		self.label_wins.grid(row=7, column=0, sticky="w",padx=distance_from_left_side)
		self.label_value_wins_tab4 = Label(self, textvariable=self.var_wins)
		self.label_value_wins_tab4.grid(row=7, column=1, sticky="w")
		self.label_relative_value_wins=Label(self, textvariable=self.var_relative_value_wins)
		self.label_relative_value_wins.grid(row=7, column=2, sticky="w")

		self.label_ties=Label(self, text="Ties: ")
		self.label_ties.grid(row=8, column=0, sticky="w",padx=distance_from_left_side)
		self.label_value_ties_tab4 = Label(self, textvariable=self.var_ties)
		self.label_value_ties_tab4.grid(row=8, column=1, sticky="w")
		self.label_relative_value_ties=Label(self, textvariable=self.var_relative_value_ties)
		self.label_relative_value_ties.grid(row=8, column=2, sticky="w")

		self.frame_stats_buttons=Frame(self)
		self.frame_stats_buttons.grid(row=9, column=0, columnspan=3,pady=15)
		self.button_reset_stats=Button(self.frame_stats_buttons, text="Reset Stats", command=lambda: self.reset_all_stats())
		self.button_reset_stats.grid(row=0, column=0)
		self.button_reset_end_states=Button(self.frame_stats_buttons, text="Reset End States", command=lambda: self.reset_end_states())
		self.button_reset_end_states.grid(row=0, column=1)