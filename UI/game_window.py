import numpy as np
from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from threading import Thread
import cv2
import pygame
import os
from game import playboard_processor,gomoku

class Game_Window(Tk):
    def __init__(self,instance:gomoku.GomokuGame):
        super().__init__()
        self.game_instance = instance
        self.root_play_game = None
        self.game_mode = None
        self.vid = None
        self.Playboard_processor = playboard_processor.PlayBoardProcessor(self.game_instance)
        self.initialize_fullscreen_GUI()
    
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
                
        if self.game_instance.use_recognition and self.vid is None:
            self.vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        else:
            self.vid = None

        self.wins_player1 = 0
        self.wins_player2 = 0
        self.draws = 0

    def initialize_fullscreen_GUI(self):
        self.initialize_session()

        if self.root_play_game is None:
            self.root_play_game = Tk()
            self.root_play_game.bind("<Escape>", lambda event: self.stop_game())
            self.root_play_game.bind("<q>", lambda event: self.quit_program())
            self.root_play_game.bind("<space>", lambda event: self.skip_current_round())

            self.var_current_player=StringVar(master=self.root_play_game)
            self.var_current_player.set("Current player: " + str(gomoku.current_player.id))
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
            self.vid=cv2.VideoCapture(1, cv2.CAP_DSHOW)
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

        self.show_webcam_view(self.label_webcam_image)
        coordinates=self.Playboard_processor.get_move()

        if coordinates:
            (x,y)=coordinates[0]
            self.root_play_game.after(0,self.label_recognition_info.config(text="Your move was successfully recognized: " + str(x) + "," + str(y) + ".",fg="green"))
            try:
                gomoku.handle_human_move(self.game_instance, x, y , gomoku.players, gomoku.p1_moves, gomoku.p2_moves)
            except:
                gomoku.handle_human_move(self.game_instance, x, y, gomoku.players)
        else:
            self.root_play_game.after(0,self.label_recognition_info.config(text="No move was recognized, try again later.",fg="red"))
            return #don't do anything

        


    

