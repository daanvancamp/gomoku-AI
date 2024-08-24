from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from threading import Thread
import cv2
import pygame
import os
from game import playboard_processor,gomoku

class Game_Window(Frame):
    def __init__(self,instance:gomoku.GomokuGame,master):
        super().__init__()
        self.grid()
        self.config(bg="black")
        self.game_instance = instance
        self.game_mode = None
        self.vid = None
        self.Playboard_processor = playboard_processor.PlayBoardProcessor(self.game_instance)

        self.wins_player1 = 0
        self.wins_player2 = 0
        self.draws = 0

        self.initialize_game_window()
    
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
                self.bind("<Key>", lambda event: self.on_key_press())
                while not self.key_pressed:
                    self.update()

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
                
        if self.game_instance.use_recognition and self.vid is None:
            self.vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        else:
            self.vid = None

        self.wins_player1 = 0
        self.wins_player2 = 0
        self.draws = 0

    def initialize_game_window(self):

        self.bind("<Escape>", lambda event: self.stop_game())
        self.bind("<q>", lambda event: self.quit_program())
        self.bind("<space>", lambda event: self.skip_current_round())

        self.var_current_player=StringVar(master=self)
        self.var_current_player.set("Current player: " + str(gomoku.current_player.id))
        self.var_wins_player1 = IntVar(master=self)
        self.var_wins_player2 = IntVar(master=self)
        self.var_draws = IntVar(master=self)

        self.var_wins_player1.set(self.wins_player1)
        self.var_wins_player2.set(self.wins_player2)
        self.var_draws.set(self.draws)

        self.var_current_game=StringVar(master=self)

        self.var_current_game_mode=StringVar(master=self)

        #self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.config(bg="#357EC7")

        font_labels=("Arial", 18)
        distance_from_left_side=20

        self.frame_info=Frame(self,bg="#357EC7")
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

        self.label_recognition_info=Label(self,text="", bg="#357EC7",fg="white", font=font_labels)
        self.label_recognition_info.grid(row=0, column=1,sticky="n")

        self.embed_pygame = Frame(self, width=self.game_instance.WIDTH, height=self.game_instance.HEIGHT)
        self.embed_pygame.grid(row=0, column=1,rowspan=2)

        self.button_capture_image = Button(self, text="Capture Image (in development)", command=self.determine_move,width=25, bg="green",fg="white", font=font_labels)
        self.button_capture_image.grid(row=1, column=1,sticky="s",pady=(0,90))
            
        size_webcam_frame=500
        self.frame_webcam=Frame(self,bg="#357EC7")
        self.frame_webcam.grid(row=0, rowspan=2,column=2,sticky="e")

        self.label_webcam_image=Label(self.frame_webcam,text="Webcam photo view (in development)", bg="#357EC7",fg="white", font=font_labels)
        self.label_webcam_image.grid(row=0, column=0,sticky="e",padx=10)

        self.label_webcam_video=Label(self.frame_webcam,text="Webcam view", bg="#357EC7",fg="white", font=font_labels,width=size_webcam_frame,height=size_webcam_frame)
        self.label_webcam_video.grid(row=1, column=0,sticky="e")

        self.list_recognition_widgets=[self.label_webcam_video,self.label_webcam_image,self.button_capture_image,self.label_recognition_info,self.frame_webcam,self.button_capture_image]
        if not self.game_instance.use_recognition:
            for widget in self.list_recognition_widgets:
                widget.grid_remove()
            self.columnconfigure(2, weight=0)
            
        self.widgets_to_hide_replay=[self.current_player_label,self.current_game_label,self.frame_stats]
        if self.game_mode==self.game_instance.game_modes[2]:#when replaying
            for widget in self.widgets_to_hide_replay:
                widget.grid_remove()

        os.environ['SDL_WINDOWID'] = str(self.embed_pygame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        pygame.display.init()
        self.game_instance.screen = pygame.display.set_mode((self.game_instance.WIDTH, self.game_instance.HEIGHT))
        self.draw_board(self.game_instance)

        self.pygame_loop()
    
    def restart_game_window(self):
        self.initialize_session()

        if self.game_mode==self.game_instance.game_modes[2]:#when replaying
            for widget in self.widgets_to_hide_replay:
                widget.grid_remove()
        else:
            for widget in self.widgets_to_hide_replay:
                widget.grid()

        if self.game_instance.use_recognition:
            self.columnconfigure(2, weight=1)
            for widget in self.list_recognition_widgets:
                if not widget.winfo_viewable():
                    widget.grid()
        else:
            self.columnconfigure(2, weight=0)
            for widget in self.list_recognition_widgets:
                if widget.winfo_viewable():
                    widget.grid_remove()

        self.var_current_game_mode.set("Game mode: " + self.game_mode)
        self.label_current_game_mode.update()

        pygame.display.init()
        self.game_instance.screen = pygame.display.set_mode((self.game_instance.WIDTH, self.game_instance.HEIGHT))
    
        self.pygame_loop()

    def refresh_labels(self):
        if gomoku.current_player.TYPE == "Human":
            player_text="Human         "
        elif gomoku.current_player.TYPE == "AI-Model":
            player_text="AI-Model      "
        else:
            player_text="Test Algorithm"

        self.var_current_player.set("Current player: " + str(gomoku.current_player.id) + " : " + player_text)
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
        self.update()
        self.after(100, self.pygame_loop)

        if self.game_instance.use_recognition:
            self.after(150,lambda: self.show_webcam_view(self.label_webcam_video))
    
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
            self.vid=cv2.VideoCapture(1, cv2.CAP_DSHOW)
            self.show_webcam_view(label)
            
        try:

            frame=self.crop_to_square(frame)

            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
  
            captured_image = Image.fromarray(opencv_image) 
  
            photo_image = ImageTk.PhotoImage(image=captured_image,master=self)
  
            label.photo_image = photo_image 
  
            self.after(0,label.config(image=photo_image)) 
        except:
            pass

    def determine_move(self):
        if self.game_instance.play_music:
            Thread(target=lambda:pygame.mixer.music.fadeout(1000)).start()#don't block the main thread

        self.show_webcam_view(self.label_webcam_image)
        coordinates=self.Playboard_processor.get_move()

        if coordinates:
            (x,y)=coordinates[0]
            self.after(0,self.label_recognition_info.config(text="Your move was successfully recognized: " + str(x) + "," + str(y) + ".",fg="green"))
            try:
                gomoku.handle_human_move(self.game_instance, x, y , gomoku.players, gomoku.p1_moves, gomoku.p2_moves)
            except:
                gomoku.handle_human_move(self.game_instance, x, y, gomoku.players)
        else:
            self.after(0,self.label_recognition_info.config(text="No move was recognized, try again later.",fg="red"))
            return #don't do anything

    def draw_board(self,instance:gomoku.GomokuGame,last_move_model=None):
        instance.screen.fill(instance.BOARD_COL)#screen needs to be cleared before drawing
        cell_size = instance.CELL_SIZE#cell_size=30
        radius_big_circle=cell_size//2 - 5#radius_big_circle=15
        radius_small_circle=cell_size//3 - 5#radius_small_circle=10
        radius_smallest_circle=cell_size//4 - 5#radius_smallest_circle=5
        red=(255,0,0) #R=255, G=0, B=0
        green=(0,255,0)
        cyan=(0,255,255)
        magenta=(255,0,255)

        if not instance.use_recognition:
            color_show_overruling=green
            color_mark_last_move=red
        else:
            color_show_overruling=cyan
            color_mark_last_move=magenta

        cells_to_mark=[(7,7),(11,11),(3,3),(3,11),(11,3)]
        for row in range(instance.GRID_SIZE):#grid_size=15
            for col in range(instance.GRID_SIZE):
                if (row,col) in cells_to_mark:
                    pygame.draw.rect(instance.screen, instance.LINE_COL, (col * cell_size, row * cell_size, cell_size, cell_size), 2)
                else:
                    pygame.draw.rect(instance.screen, instance.LINE_COL, (col * cell_size, row * cell_size, cell_size, cell_size), 1)


                if instance.board[row][col] == 1:
                    if (row,col)==last_move_model and gomoku.mark_last_move_model:
                        pygame.draw.circle(instance.screen, instance.P1COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)
                        pygame.draw.circle(instance.screen, color_mark_last_move, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_small_circle)

                        if instance.show_overruling and gomoku.player1.ai.overruled_last_move:
                            pygame.draw.circle(instance.screen, color_show_overruling, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)
                    else:
                        pygame.draw.circle(instance.screen, instance.P1COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)

                elif instance.board[row][col] == 2:
                    if (row,col)==last_move_model and gomoku.mark_last_move_model:
                        pygame.draw.circle(instance.screen, instance.P2COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)
                        pygame.draw.circle(instance.screen, color_mark_last_move, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_small_circle)
                        if instance.show_overruling and gomoku.player2.ai.overruled_last_move:
                            pygame.draw.circle(instance.screen, color_show_overruling, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)
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

            if instance.GRID_SIZE > row >= 0 == instance.board[row][col] and 0 <= col < instance.GRID_SIZE:
                if instance.board[row][col] == 0:#cell is empty
                    cell_size = instance.CELL_SIZE
                    pygame.draw.circle(instance.screen, instance.HOVER_COLOR, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_big_circle)
                    if gomoku.current_player.id==1:
                        pygame.draw.circle(instance.screen, instance.P1COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)
                    elif gomoku.current_player.id==2:
                        pygame.draw.circle(instance.screen, instance.P2COL, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), radius_smallest_circle)

        


    

