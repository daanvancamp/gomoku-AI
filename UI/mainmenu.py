import random
import sys
from threading import Thread
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import filereader
import stats
from PIL import Image, ImageTk
from filereader import log_info_overruling
import modelmanager
import gomoku
import numpy as np
from UI import game_window

WIDTH = 540
HEIGHT = 500

game_instance = gomoku.GomokuGame(filereader.create_gomoku_game("consts.json"))
game_instance.GUI = game_window.Game_Window(game_instance)
modelmanager_instance = modelmanager.ModelManager()


root = Tk()
root.geometry(str(WIDTH) + "x" + str(HEIGHT))
root.title("Gomoku -- Main Menu")
root.configure(background="#357EC7")
root.attributes("-topmost", True)
root.bind("<Escape>", lambda event: quit_game())
root.bind("<q>", lambda event: quit_game())

try:
    root.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('res/ico.png')))
except TclError:
    print("icoon kon niet geladen worden.")
    pass

style2 = ttk.Style()
style2.theme_use('default')
style2.configure('TNotebook.Tab', background="#357EC7")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Play gomoku')
tabControl.add(tab2, text='Train')
tabControl.add(tab3, text='Replay old games')
tabControl.add(tab4, text=' Models')
tabControl.grid(row=0, sticky="w")

style_numbers = ["georgia", 10, "white", 12, 2]#font, size, color, bold, underline

input_canvas = Canvas(root, relief="groove", borderwidth=0, highlightthickness=0,bg="#357EC7")
input_canvas.grid(row=1, padx=2, pady=2)
var_playerType1 = StringVar()
var_playerType2 = StringVar()
var_playerType1.set("Human")
var_playerType2.set("AI-Model")
var_game_runs = StringVar()
var_game_runs.set("1")
var_delay = BooleanVar()
var_delay.set(False)
var_log = BooleanVar()
var_log.set(False)
var_rep = BooleanVar()
var_rep.set(True)
replay_path = StringVar()
replay_path.set(r".\data\replays")
var_allow_overrule_player_1=BooleanVar()
var_allow_overrule_player_1.set(True)
var_allow_overrule_player_2=BooleanVar()
var_allow_overrule_player_2.set(True)
var_play_music=BooleanVar()
var_play_music.set(False)
var_show_overruling=BooleanVar()
var_show_overruling.set(True)
var_show_graphs=BooleanVar()
var_show_graphs.set(False)
var_show_dialog=BooleanVar()
var_show_dialog.set(False)

var_losses=IntVar()
var_losses.set(0)
var_wins=IntVar()
var_wins.set(0)
var_ties=IntVar()
var_ties.set(0)

var_relative_value_losses = StringVar()
var_relative_value_losses.set("0%")

var_relative_value_wins = StringVar()
var_relative_value_wins.set("0%")

var_relative_value_ties = StringVar()
var_relative_value_ties.set("0%")

var_choose_stats=StringVar()

var_start_from_file=BooleanVar()
var_start_from_file.set(False)
state_board_path=StringVar()
state_board_path.set(r".\test_situations\specific_situation.txt")
var_name_model=StringVar()
var_model_player1=StringVar()
var_model_player2=StringVar()
var_use_recognition=BooleanVar()
var_use_recognition.set(False)
var_model_player1.set("standaard")
var_model_player2.set("standaard")
var_startingPlayer=StringVar()
var_startingPlayer.set("Player 1")

var_number_of_training_loops=StringVar()
var_number_of_training_loops.set("0 (against H:0,T'A':0, AI:0 )")
var_number_of_training_loops_comboboxes_p1=StringVar()
var_number_of_training_loops_comboboxes_p1.set(0)
var_number_of_training_loops_comboboxes_p2=StringVar()
var_number_of_training_loops_comboboxes_p2.set(0)

var_layers=IntVar()
var_layers.set(3)
def set_player_type(player_id):
    if player_id == 1:
        newtype = var_playerType1.get()
    else:
        newtype = var_playerType2.get()
    gomoku.players[player_id-1].TYPE=newtype

def set_game_instance(new_instance):
    global game_instance
    game_instance = new_instance

def browse_state_files():
    file_path = filedialog.askopenfilename(filetypes=[("txt File", "*.txt")],initialdir=r".\test_situations")
    state_board_path.set(file_path)

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("Json File", "*.json")],initialdir=r".\data\replays")
    replay_path.set(file_path)
   

def run():
    gomoku.run(game_instance)

def load_board_from_file()->list[list[int]]:
    try:
        with open(state_board_path.get(), "r") as file:
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


def start_new_game():
    global game_instance
    log_info_overruling("\n\n\nnew session begins:")
    
    game_instance.use_recognition = var_use_recognition.get()
    game_instance.play_music = var_play_music.get()
    game_instance.show_overruling = var_show_overruling.get()
    game_instance.record_replay = var_rep.get()
    game_instance.show_dialog = var_show_dialog.get()

    game_instance.ai_delay = var_delay.get()
    stats.should_log = var_log.get()
    
        
    gomoku.player1.TYPE=var_playerType1.get()
    gomoku.player2.TYPE=var_playerType2.get()

    if (gomoku.player1.TYPE=="Human" or gomoku.player2.TYPE=="Human") and not game_instance.use_recognition:
        game_instance.show_hover_effect=True
    else:
        game_instance.show_hover_effect=False

    stats.setup_logging(gomoku.player1.TYPE, gomoku.player2.TYPE)

    if gomoku.player1.TYPE == "AI-Model":
        gomoku.player1.load_model(var_model_player1.get())
        gomoku.player1.set_allow_overrule(var_allow_overrule_player_1.get())
    if gomoku.player2.TYPE == "AI-Model":
        gomoku.player2.load_model(var_model_player2.get())
        gomoku.player2.set_allow_overrule(var_allow_overrule_player_2.get())

    if var_startingPlayer.get() == "Player 1":
        gomoku.current_player = gomoku.player1
    else:
        gomoku.current_player = gomoku.player2
        
    root.wm_state('iconic')

        
    valid_number = False

    while not valid_number:
        try:
            runs = int(var_game_runs.get())
            valid_number=True
        except:
            print("invalid number, try again")

    game_instance.game_mode=game_instance.game_modes[0]
    game_instance.GUI.initialize_fullscreen_GUI()
    for i in range(runs):
        log_info_overruling("run "+str(i+1)+" begins:")
        stats.log_message(f"Game  {i+1} begins.")

        game_instance.current_game = i+1
        game_instance.last_round = (i+1 == runs)
        board_loaded=None
        if var_start_from_file.get():
            board = load_board_from_file()
            if board is not None:
                board_loaded=True
            else:
                label_unvalid_file.config(text="Board file not valid, try again with another file.")
                board_loaded=False
            game_instance.set_board(board)

        if (board_loaded and var_start_from_file.get()) or not var_start_from_file.get():
            try:
                gomoku.runGame(game_instance, i) #main function
                if game_instance.stop_game:
                    break
            except Exception as e:
                print("error in gomoku.run")
                raise Exception("There is an error in the main function/loop, it can be anything." , str(e))
        else:
            print("Please select a valid file that contains the board in the following format and try again:")
            for i in range(15):
                for b in range(15):
                    print(random.randint(0,2), end="")
                print("\n",end="")
            print("The board can only contain 0, 1, or 2. 0 = empty, 1 = player 1, 2 = player 2.")
    game_over()

def start_new_training():
    global game_instance
    log_info_overruling("\n\n\nnew session begins:")
    
    game_instance.use_recognition = False
    game_instance.play_music = False
    game_instance.show_overruling=False
    game_instance.record_replay=True
    game_instance.show_graphs=var_show_graphs.get()

    gomoku.player1.TYPE="AI-Model"
    gomoku.player2.TYPE=var_playerType2.get()
    
    if gomoku.player1.TYPE=="Human" or gomoku.player2.TYPE=="Human":
        game_instance.show_hover_effect=True
    else:
        game_instance.show_hover_effect=False

    gomoku.player1.load_model(var_model_player1.get())#player 1 is always an AI-Model when training
    gomoku.player1.set_allow_overrule(var_allow_overrule_player_1.get())

    if gomoku.player2.TYPE == "AI-Model":
        gomoku.player2.load_model(var_model_player2.get())
        gomoku.player2.set_allow_overrule(var_allow_overrule_player_2.get())

    if var_startingPlayer.get() == "Player 1":
        gomoku.current_player = gomoku.player1
    else:
        gomoku.current_player = gomoku.player2


    try:
        valid_number = False
        while not valid_number:
            try:
                runs = int(var_game_runs.get())
                valid_number=True
            except:
                print("invalid number, try again")

        game_instance.ai_delay = False #never wait when training
        stats.should_log = var_log.get()
        stats.setup_logging(gomoku.player1.TYPE, gomoku.player2.TYPE)
        root.wm_state('iconic')

        game_instance.game_mode=game_instance.game_modes[1]
        game_instance.GUI.initialize_fullscreen_GUI()

        for i in range(runs):
            log_info_overruling("run "+str(i+1)+" begins:")
            
            stats.log_message(f"Game  {i+1} begins.")
            game_instance.current_game = i+1
            game_instance.last_round = (i+1 == runs)
            try:
                gomoku.runTraining(game_instance, i) #main function
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
    game_over()


def start_new_replay():
    global game_instance
    game_instance.show_hover_effect=False
    game_instance.show_dialog = var_show_dialog.get()


    log_info_overruling("\n\n\nnew session begins:")
   
    moves = filereader.load_replay(replay_path.get())

    if moves is None:
        replay_loaded=False
    else:
        replay_loaded=True
    
    if replay_loaded:
        label_info_replay_file_loaded.config(text="Replay file succesfully loaded",fg="green")

        game_instance.use_recognition = False
        game_instance.play_music = False

        gomoku.player1.TYPE = "Replay"
        gomoku.player2.TYPE = "Replay"

        gomoku.current_player = gomoku.player1

        game_instance.ai_delay = var_delay.get()
        stats.should_log = var_log.get()
        stats.setup_logging(gomoku.player1.TYPE, gomoku.player2.TYPE)
        root.wm_state('iconic')

        game_instance.game_mode=game_instance.game_modes[2]
        game_instance.GUI.initialize_fullscreen_GUI()

        try:
            gomoku.runReplay(game_instance,moves) #main function
        except Exception as e:
            print("error in gomoku.run, herschrijf die functie.")
            raise Exception("There is an error in the main function/loop, it can be anything." , str(e)) 
    else:
        print("Try again, please select a valid json file and make sure that it's not opened")
        label_info_replay_file_loaded.config(text="Try again, please select a valid json file and make sure that it's not opened in another program",fg="red")
        
    game_over()

def game_over():
    global game_instance
    if game_instance.GUI.root_play_game is not None:
        game_instance.GUI.hide_GUI()
    root.wm_state('normal')
    game_instance.current_game = 0
    if game_instance.quit_program:
        quit_game()

def create_new_model():
    modelmanager_instance.create_new_model(var_name_model.get())
    refresh_models()
    refresh_training_stats()

def delete_model():
    global last_selected_model
    for i in Lb1.curselection():
        modelmanager_instance.delete_model(Lb1.get(i))
    refresh_models()
    last_selected_model=Lb1.get(0)
    refresh_training_stats()
        
def reset_all_stats():
    global last_selected_model
    for i in Lb1.curselection():
        modelmanager_instance.get_model(Lb1.get(i)).reset_stats(True)
    if Lb1.curselection()==():
        modelmanager_instance.get_model(last_selected_model).reset_stats(True)
    refresh_models()
    refresh_training_stats()

def reset_end_states():
    global last_selected_model
    for i in Lb1.curselection():
        modelmanager_instance.get_model(Lb1.get(i)).reset_end_states()
    if Lb1.curselection()==():
        modelmanager_instance.get_model(last_selected_model).reset_end_states()
    refresh_models()
    refresh_training_stats()
def refresh_models():
    Lb1.delete(0,END)
    i = 0
    models = modelmanager_instance.get_list_models()
    for model in models:
        Lb1.insert(i, model)
        i+=1
    CbModel1.configure(values=models)
    CbModel2.configure(values=models)
    CbModelTrain1.configure(values=models)
    CbModelTrain2.configure(values=models)

def quit_game():
    sys.exit()#end the program

def maintain_GUI():
    #add delay to this loop if the program stutters or crashes on your computer
    tab_text = "Play gomoku"
    last_value_repvar=True
    last_value_load_board_from_file=False
    while True:
        try:

            old_tab_text= tab_text
            current_tab = tabControl.index(tabControl.select())
            tab_text = tabControl.tab(current_tab, "text")
            if tab_text=="Train" and old_tab_text!=tab_text:
                var_game_runs.set("3000")
            elif tab_text=="Play gomoku" and old_tab_text!=tab_text:
                var_game_runs.set("1")
                var_delay.set(False)
            elif tab_text=="Replay old games" and old_tab_text!=tab_text:
                var_delay.set(True)

            if tab_text=="Train":
                label_shortcuts.config(text="In game shortcuts: esc = return to this menu, q = terminate program")
            elif tab_text=="Replay old games":
                label_shortcuts.config(text="In game shortcuts: esc = return to this menu, q = terminate program")
            elif tab_text=="Play gomoku":
                label_shortcuts.config(text="In game shortcuts: esc = return to this menu, q = terminate program , space = skip the current round")

            ##TAB 1##
            if var_playerType1.get() == "Human" and var_playerType2.get() == "Human":
                var_log.set(False)
                var_rep.set(False)
                logbutton.config(state=DISABLED)
                replaybutton.config(state=DISABLED)
            else:
                logbutton.config(state=NORMAL)
                replaybutton.config(state=NORMAL)


            if var_playerType1.get()=="AI-Model":
                CbModel1.config(state="readonly")
                overrule_button_player_1.config(state=NORMAL)
                label_value_number_of_training_loops_p1.config(state=NORMAL)

            else:
                CbModel1.config(state=DISABLED)
                overrule_button_player_1.config(state=DISABLED)
                label_value_number_of_training_loops_p1.config(state=DISABLED)

            if var_playerType2.get()=="AI-Model":
                CbModel2.config(state="readonly")
                overrule_button_player_2.config(state=NORMAL)
                overrule_button_player_2_tab2.config(state=NORMAL)
                label_value_number_of_training_loops_p2.config(state=NORMAL)
            else:
                CbModel2.config(state=DISABLED)
                overrule_button_player_2.config(state=DISABLED)
                overrule_button_player_2_tab2.config(state=DISABLED)
                label_value_number_of_training_loops_p2.config(state=DISABLED)

            if var_start_from_file.get():
                label_load_state.grid()
                load_state_entry.grid()
                button_browse_state_file.grid()
            else:
                label_load_state.grid_remove()
                load_state_entry.grid_remove()
                button_browse_state_file.grid_remove()
        
            recognition_possible=(var_playerType1.get()=="Human" or var_playerType2.get()=="Human")and (var_playerType1.get()=="AI-Model" or var_playerType2.get()=="AI-Model" or var_playerType1.get()=="Test Algorithm" or var_playerType2.get()=="Test Algorithm")
            if recognition_possible and not var_start_from_file.get():
                use_recognition_button.config(state=NORMAL)
                label_recognition.config(state=NORMAL)
            else:
                use_recognition_button.config(state=DISABLED)
                label_recognition.config(state=DISABLED)
            #tab 1, delaybutton#
            if (var_playerType1.get()=="AI-Model" or var_playerType2.get()=="AI-Model" ) or (var_playerType1.get()=="Test Algorithm" or var_playerType2.get()=="Test Algorithm"):
                delaybutton.config(state=NORMAL)
            else:
                delaybutton.config(state=DISABLED)
            #tab1, music button#
            if var_playerType1.get()=="Human" or var_playerType2.get()=="Human":
                music_button.config(state=NORMAL)
            else:
                music_button.config(state=DISABLED)

            #starting player
            if var_playerType1.get()==var_playerType2.get() and var_playerType1=="Test Algorithm": #option not relevant
                playerstartLabel.config(state=DISABLED)
                CbStartingPlayer.config(state=DISABLED)
            else:
                playerstartLabel.config(state="normal")
                CbStartingPlayer.config(state="readonly")

            if var_start_from_file.get()!=last_value_load_board_from_file and var_start_from_file.get()==True:
                var_rep.set(False) #can't be used simultanously because if you would save a replay file, it wouldn't be complete (the moves that are loaded are gone)
            
                last_value_load_board_from_file=var_start_from_file.get()
                last_value_repvar=var_rep.get()

            if var_rep.get()!=last_value_repvar and var_rep.get()==True:
                var_start_from_file.set(False)

                last_value_load_board_from_file=var_start_from_file.get()
                last_value_repvar=var_rep.get()

            list_artificial_players=["AI-Model","Test Algorithm"]
            if var_playerType1.get() not in list_artificial_players and var_playerType2.get() not in list_artificial_players:
                button_show_overruling.config(state=NORMAL)
            else:
                button_show_overruling.config(state=DISABLED)

            if not var_rep.get() and not var_start_from_file.get():
                label_info_load_save_replay.config(state=DISABLED)
            else:
                label_info_load_save_replay.config(state=NORMAL)

            if var_playerType2.get()=="Human":
                train_description.config(state=DISABLED) #a human will never play the game 3000 times to train the model
            else:
                train_description.config(state=NORMAL)

            if var_playerType2.get()=="AI-Model":
                CbModelTrain2.config(state="readonly")
                label_value_number_of_training_loops_tab2_p2.config(state=NORMAL)
            else:
                CbModelTrain2.config(state=DISABLED)
                label_value_number_of_training_loops_tab2_p2.config(state=DISABLED)

            show_number_of_training_loops_comboboxes()
            refresh_training_stats()
        except Exception as e:
            pass

def refresh_training_stats():
    global last_selected_model #used to keep track of which model is selected, because it is unselected when selecting something in the  combobox
    try:
        for i in Lb1.curselection():
            last_selected_model=Lb1.get(i)

        model_class=modelmanager_instance.get_model(last_selected_model)
        var_number_of_training_loops.set(f"{model_class.get_number_of_training_loops("training loops")} (against H:{model_class.get_number_of_training_loops("training loops against Human")}, T'A':{model_class.get_number_of_training_loops("training loops against Test Algorithm")}, AI:{model_class.get_number_of_training_loops("training loops against AI-Model")} )")

        if Cb_choose_stats.get()== "Total":
            var_losses.set(model_class.get_number_of_losses("total end stats"))
            var_wins.set(model_class.get_number_of_wins("total end stats"))
            var_ties.set(model_class.get_number_of_ties("total end stats"))
        elif Cb_choose_stats.get()== "Games":
            var_losses.set(model_class.get_number_of_losses("games end stats"))
            var_wins.set(model_class.get_number_of_wins("games end stats"))
            var_ties.set(model_class.get_number_of_ties("games end stats"))
        elif Cb_choose_stats.get()== "Training":
            var_losses.set(model_class.get_number_of_losses("training loops end stats"))
            var_wins.set(model_class.get_number_of_wins("training loops end stats"))
            var_ties.set(model_class.get_number_of_ties("training loops end stats"))
    
        total_sum=var_losses.get()+var_ties.get()+var_wins.get()
        if total_sum>0:
            for relative_value,value in zip([var_relative_value_losses,var_relative_value_wins,var_relative_value_ties],[var_losses,var_wins,var_ties]):
                relative_value.set(str(np.round(((value.get()/total_sum)*100),2))+"%")  
        else:
            var_relative_value_losses.set("N/A")
            var_relative_value_wins.set("N/A")
            var_relative_value_ties.set("N/A")
    except Exception as e:
        pass

def show_number_of_training_loops_comboboxes():
    var_number_of_training_loops_comboboxes_p1.set("training loops: "+str(modelmanager_instance.get_model(var_model_player1.get()).get_number_of_training_loops("training loops")))
    
    var_number_of_training_loops_comboboxes_p2.set("training loops: "+str(modelmanager_instance.get_model(var_model_player2.get()).get_number_of_training_loops("training loops")))
    
Thread_maintain_GUI=Thread(target=maintain_GUI,daemon=True)#end when main program ends
Thread_maintain_GUI.start()

style2=ttk.Style()
style2.configure("TButton", font=(style_numbers[0], style_numbers[1]),bg=style_numbers[2],ipadx=style_numbers[3],ipady=style_numbers[4],pady=15)#font=georgia, size=10;bg=white
style2.configure("TRadiobutton",fg="white",bg="green")
style2.configure("TEntry",fg="white",bg="green")
style2.configure("TLabel", font=(style_numbers[0], style_numbers[1]),fg="white",bg="green")#font=georgia, size=10
style2.configure("TCheckbutton", font=(style_numbers[0], style_numbers[1]),fg="white",bg="green")#font=georgia, size=10

distance_from_left_side=10
### TABS ###
ttk.Label(tab1)

button_1 = ttk.Button(tab1, text="New Game", command=lambda: start_new_game(), style="TButton")
button_1.grid(row=0, column=0, sticky="w", padx=distance_from_left_side)
checkbox_show_dialog=ttk.Checkbutton(tab1, text="Show dialog before starting next game", variable=var_show_dialog,style="TCheckbutton")
checkbox_show_dialog.grid(row=0, column=1, sticky="w")

player1typelabel = ttk.Label(tab1,style="TLabel", text="Player 1(black)")
player1typelabel.grid(row=2, column=0, sticky="w", padx=distance_from_left_side)
player2typelabel = ttk.Label(tab1, text="Player 2(white)", style="TLabel")
player2typelabel.grid(row=2, column=1, sticky="w", padx=distance_from_left_side)

radiobutton1 = ttk.Radiobutton(tab1, text="Human", variable=var_playerType1, value="Human", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton1.grid(row=3, column=0, sticky="w", padx=distance_from_left_side)
radiobutton2 = ttk.Radiobutton(tab1, text="Test Algorithm", variable=var_playerType1, value="Test Algorithm", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton2.grid(row=4, column=0, sticky="w", padx=distance_from_left_side)
radiobutton3 = ttk.Radiobutton(tab1, text="AI-Model", variable=var_playerType1, value="AI-Model", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton3.grid(row=5, column=0, sticky="w", padx=distance_from_left_side)

radiobutton4 = ttk.Radiobutton(tab1, text="Human", variable=var_playerType2, value="Human", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton4.grid(row=3, column=1, sticky="w")
radiobutton5 = ttk.Radiobutton(tab1, text="Test Algorithm", variable=var_playerType2, value="Test Algorithm", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton5.grid(row=4, column=1, sticky="w")
radiobutton6 = ttk.Radiobutton(tab1, text="AI-Model", variable=var_playerType2, value="AI-Model", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton6.grid(row=5, column=1, sticky="w")

list_models = modelmanager_instance.get_list_models()
CbModel1 = ttk.Combobox(tab1, state="readonly", values=list_models,textvariable=var_model_player1)
CbModel2 = ttk.Combobox(tab1, state="readonly", values=list_models,textvariable=var_model_player2)

CbModel1.grid(row=6, column=0, sticky="w",padx=distance_from_left_side)
CbModel2.grid(row=6, column=1,sticky="w",padx=distance_from_left_side)

label_value_number_of_training_loops_p1 = ttk.Label(tab1, textvariable=var_number_of_training_loops_comboboxes_p1,style="TLabel")
label_value_number_of_training_loops_p1.grid(row=8, column=0, sticky="w",padx=distance_from_left_side)

label_value_number_of_training_loops_p2 = ttk.Label(tab1, textvariable=var_number_of_training_loops_comboboxes_p2,style="TLabel")
label_value_number_of_training_loops_p2.grid(row=8, column=1, sticky="w")


overrule_button_player_1=ttk.Checkbutton(tab1, text="Allow overrule", variable=var_allow_overrule_player_1,style="TCheckbutton")
overrule_button_player_1.grid(row=9, column=0, sticky="w",padx=distance_from_left_side)

overrule_button_player_2=ttk.Checkbutton(tab1, text="Allow overrule", variable=var_allow_overrule_player_2,style="TCheckbutton")
overrule_button_player_2.grid(row=9, column=1, sticky="w")


gamerunslabel = ttk.Label(tab1, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=10, column=0, sticky="w",padx=distance_from_left_side)
gamerunsentry = ttk.Entry(tab1, textvariable=var_game_runs,style="TEntry")
gamerunsentry.grid(row=10, column=1, sticky="w")


playerstartLabel = ttk.Label(tab1, text="Player to start: ",style="TLabel")
playerstartLabel.grid(row=11, column=0, sticky="w", padx=distance_from_left_side)
CbStartingPlayer = ttk.Combobox(tab1, state="readonly", values=["Player 1", "Player 2"], textvariable=var_startingPlayer)
CbStartingPlayer.current(0)
CbStartingPlayer.grid(row=11, column=1, sticky="w")

#column 0
logbutton = ttk.Checkbutton(tab1, text="Create log file", variable=var_log,style="TCheckbutton") 
logbutton.grid(row=12, column=0, sticky="w",padx=distance_from_left_side)
replaybutton = ttk.Checkbutton(tab1, text="Save replays(1)", variable=var_rep,style="TCheckbutton") 
replaybutton.grid(row=13, column=0, sticky="w",padx=distance_from_left_side)
delaybutton = ttk.Checkbutton(tab1, text="Use AI Delay", variable=var_delay,style="TCheckbutton")
delaybutton.grid(row=14, column=0, sticky="w",padx=distance_from_left_side)

#column1
music_button=ttk.Checkbutton(tab1, text="Play music", variable=var_play_music,style="TCheckbutton")
music_button.grid(row=12, column=1, sticky="w")
button_show_overruling=ttk.Checkbutton(tab1, text="Show overruling", variable=var_show_overruling,style="TCheckbutton")
button_show_overruling.grid(row=13, column=1, sticky="w")
use_recognition_button=ttk.Checkbutton(tab1, text="use recognition(experimental)*", variable=var_use_recognition,style="TCheckbutton")
use_recognition_button.grid(row=14, column=1, sticky="w")


label_recognition=ttk.Label(tab1, text="*only turn on when you have a physical board, a webcam and the other repository.",style="TLabel",wraplength=WIDTH-15)
label_recognition.grid(row=15, column=0, sticky="w",columnspan=2, padx=distance_from_left_side)


bottomframe = Frame(tab1, highlightbackground="blue", highlightthickness=3, borderwidth=1)
bottomframe.grid(row=16, column=0, sticky="w",columnspan=3, padx=distance_from_left_side, pady=15)

start_from_file_button=ttk.Checkbutton(bottomframe, text="Load game situation(2)", variable=var_start_from_file,style="TCheckbutton")
start_from_file_button.grid(row=0, column=0, sticky="w")
label_unvalid_file=ttk.Label(bottomframe, text="",style="TLabel")
label_unvalid_file.grid(row=0, column=1, sticky="e",columnspan=2)

label_load_state=ttk.Label(bottomframe, text="Choose file board state: ",style="TLabel")
label_load_state.grid(row=1, column=0, sticky="w")
load_state_entry = ttk.Entry(bottomframe, textvariable=state_board_path, width=50,style="TEntry")
load_state_entry.grid(row=2, column=0, sticky="w",columnspan=2)
button_browse_state_file = ttk.Button(bottomframe, text="...",style="TButton", command=lambda: browse_state_files())
button_browse_state_file.grid(row=2, column=2, sticky="w")


button_3 = ttk.Button(input_canvas, text="Quit Game(ESC/Q)", style="TButton", command=lambda: quit_game())
button_3.grid(row=1, column=0)
label_shortcuts=Label(input_canvas, text="In game shortcuts: esc = return to this menu, q = terminate program , space = skip the current round",wraplength=WIDTH-15,bg="#357EC7",font=(style_numbers[0],style_numbers[1]),fg="white")
label_shortcuts.grid(row=2, column=0)

label_info_load_save_replay=ttk.Label(tab1,wraplength=WIDTH-15, text="(1)(2)The save replay function can't be used when loading a board, because that would create a wrong replay file.",style="TLabel")
label_info_load_save_replay.grid(row=17, column=0, sticky="w",columnspan=2,pady=5,padx=distance_from_left_side)

ttk.Label(tab2)
#row 0
button_2 = ttk.Button(tab2, text="Train", style="TButton", command=lambda: start_new_training())
button_2.grid(row=0, column=1, sticky="e")

#column 0
label_model=ttk.Label(tab2, text="AI-Model: ",style="TLabel")
label_model.grid(row=1, column=0, sticky="w",padx=distance_from_left_side,pady=1)
CbModelTrain1 = ttk.Combobox(tab2, state="readonly", values=list_models,textvariable=var_model_player1)
CbModelTrain1.grid(row=2, column=0, sticky="w",padx=distance_from_left_side,pady=1)
label_value_number_of_training_loops_tab2_p1 = ttk.Label(tab2, textvariable=var_number_of_training_loops_comboboxes_p1,style="TLabel")
label_value_number_of_training_loops_tab2_p1.grid(row=3, column=0, sticky="w",padx=distance_from_left_side,pady=1)
overrule_button_player_1_tab2=ttk.Checkbutton(tab2, text="Allow overrule", variable=var_allow_overrule_player_1,style="TCheckbutton")
overrule_button_player_1_tab2.grid(row=4, column=0, sticky="w",padx=distance_from_left_side)


train_opponent_label = ttk.Label(tab2, text="Train model against:", style="TLabel")
train_opponent_label.grid(row=1, column=1, sticky="w")

human_training_button=ttk.Radiobutton(tab2, text="Human", variable=var_playerType2, value="Human", style="TRadiobutton")
human_training_button.grid(row=2, column=1,sticky="w")
radiobutton7 = ttk.Radiobutton(tab2, text="Test Algorithm", variable=var_playerType2, value="Test Algorithm")
radiobutton7.grid(row=3, column=1, sticky="w")
radiobutton8 = ttk.Radiobutton(tab2, text="AI-Model", variable=var_playerType2, value="AI-Model", style="TRadiobutton")
radiobutton8.grid(row=4, column=1, sticky="w")

CbModelTrain2 = ttk.Combobox(tab2, state="readonly", values=list_models,textvariable=var_model_player2)
CbModelTrain2.grid(row=5, column=1, sticky="w")
label_value_number_of_training_loops_tab2_p2 = ttk.Label(tab2, textvariable=var_number_of_training_loops_comboboxes_p2,style="TLabel")
label_value_number_of_training_loops_tab2_p2.grid(row=6, column=1, sticky="w")
overrule_button_player_2_tab2=ttk.Checkbutton(tab2, text="Allow overrule", variable=var_allow_overrule_player_2,style="TCheckbutton")
overrule_button_player_2_tab2.grid(row=7, column=1, sticky="w")

gamerunslabel = ttk.Label(tab2, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=8, column=0, sticky="w",pady=2,padx=distance_from_left_side)
gamerunsentry2 = ttk.Entry(tab2, textvariable=var_game_runs,style="TEntry")
gamerunsentry2.grid(row=9, column=0, sticky="w",pady=2,padx=distance_from_left_side)
replaybutton2 = ttk.Checkbutton(tab2, text="Save replays", variable=var_rep,style="TCheckbutton")
replaybutton2.grid(row=10, column=0, sticky="w",pady=2,padx=distance_from_left_side)
show_graphs_checkbutton=ttk.Checkbutton(tab2, text="Show graphs*", variable=var_show_graphs,style="TCheckbutton")
show_graphs_checkbutton.grid(row=11, column=0, sticky="w",pady=2,padx=distance_from_left_side)



train_description = Label(tab2, text="It is recommended to run at least 3 000 games per training session.", font=(style_numbers[0], style_numbers[1]), wraplength=WIDTH-15)
train_description.grid(row=12, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

info_show_graphs=ttk.Label(tab2, text="*Don't forget to MANUALLY close the graphs at the end of each training session if you enable it.",style="TLabel",foreground="red",wraplength=WIDTH-15)
info_show_graphs.grid(row=13, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)

ttk.Label(tab3)
replaylabel = ttk.Label(tab3, text="Choose the replay file: ",style="TLabel")
replaylabel.grid(row=0, column=0, sticky="w",pady=2,padx=distance_from_left_side)
replayentry = ttk.Entry(tab3, textvariable=replay_path, width=30,style="TEntry")
replayentry.grid(row=1, column=0, sticky="w",pady=2,padx=distance_from_left_side)
button_4 = ttk.Button(tab3, text="...",style="TButton", command=lambda: browse_files())
button_4.grid(row=1, column=1, sticky="w")
delaybutton2 = ttk.Checkbutton(tab3, text="Use AI Delay", variable=var_delay, style="TCheckbutton")
delaybutton2.grid(row=2, column=0, sticky="w",pady=2,padx=distance_from_left_side)
button_5 = ttk.Button(tab3, text="Play", style="TButton", command=lambda: start_new_replay())
button_5.grid(row=3, column=0, sticky="w",pady=2,padx=distance_from_left_side)
checkbox_show_dialog_tab3=ttk.Checkbutton(tab3, text="Show dialog before starting next game", variable=var_show_dialog,style="TCheckbutton")
checkbox_show_dialog_tab3.grid(row=3, column=1, sticky="w")

label_info_replay_file_loaded=Label(tab3, text="",foreground="red",wraplength=WIDTH-20,font=(style_numbers[0],style_numbers[1]))
label_info_replay_file_loaded.grid(row=4, column=0, sticky="w",columnspan=2,padx=distance_from_left_side)


ttk.Label(tab4)
Lb1 = Listbox(tab4)

models = modelmanager_instance.get_list_models()
i  = 0
for model in models:
    Lb1.insert(i, model.split('\\')[-1])
    i+=1
Lb1.grid(row=0, column=2,padx=distance_from_left_side)

if "standaard" in models or "Standaard" in models:
    for item in models:
        if item=="standaard"or item=="Standaard":
            Lb1.selection_set(models.index(item))
            Lb1.activate(models.index(item))
            last_selected_model=item
else:
    Lb1.selection_set(0)
    Lb1.activate(0)
    last_selected_model=models[0]

frame_buttons=ttk.Frame(tab4)
frame_buttons.grid(row=0, column=0, columnspan=2,sticky='e')

button_NewModel = ttk.Button(frame_buttons, text="Make New Model", style="TButton", command=lambda: create_new_model())
button_NewModel.grid(row=0, column=1,sticky="n",pady=2,padx=distance_from_left_side)
nameModelLabel = ttk.Label(frame_buttons, text="Name of model: ",style="TLabel")
nameModelLabel.grid(row=1, column=0, sticky="w",pady=2,padx=distance_from_left_side)
nameModelEntry = ttk.Entry(frame_buttons, textvariable=var_name_model,style="TEntry")
nameModelEntry.grid(row=1, column=1, sticky="w",pady=2,padx=distance_from_left_side)
nameModelEntry.bind("<Return>",lambda event: create_new_model())#push enter to create a new model (easier)

button_DeleteModel = ttk.Button(frame_buttons, text="Delete Model", style="TButton", command=lambda: delete_model())
button_DeleteModel.grid(row=0, column=0,sticky="n")



label_number_of_training_loops = ttk.Label(tab4, text="Training loops: ",style="TLabel")
label_number_of_training_loops.grid(row=4, column=0, sticky="w",padx=(distance_from_left_side,0),pady=(30,10))
label_value_number_of_training_loops_tab4 = ttk.Label(tab4, textvariable=var_number_of_training_loops,style="TLabel")
label_value_number_of_training_loops_tab4.grid(row=4, column=1, sticky="w",pady=(30,10))

stats_list=["Total","Games","Training"]
Cb_choose_stats= ttk.Combobox(tab4, state="readonly", values=stats_list, textvariable=var_choose_stats)
Cb_choose_stats.current(0)
Cb_choose_stats.grid(row=5, column=0, sticky="w",pady=2,padx=distance_from_left_side)


label_losses=ttk.Label(tab4, text="Losses: ",style="TLabel")
label_losses.grid(row=6, column=0, sticky="w")
label_value_losses_tab4 = ttk.Label(tab4, textvariable=var_losses,style="TLabel")
label_value_losses_tab4.grid(row=6, column=1, sticky="w")
label_relative_value_losses=ttk.Label(tab4, textvariable=var_relative_value_losses,style="TLabel")
label_relative_value_losses.grid(row=6, column=2, sticky="w")

label_wins=ttk.Label(tab4, text="Wins: ",style="TLabel")
label_wins.grid(row=7, column=0, sticky="w",padx=distance_from_left_side)
label_value_wins_tab4 = ttk.Label(tab4, textvariable=var_wins,style="TLabel")
label_value_wins_tab4.grid(row=7, column=1, sticky="w")
label_relative_value_wins=ttk.Label(tab4, textvariable=var_relative_value_wins,style="TLabel")
label_relative_value_wins.grid(row=7, column=2, sticky="w")

label_ties=ttk.Label(tab4, text="Ties: ",style="TLabel")
label_ties.grid(row=8, column=0, sticky="w",padx=distance_from_left_side)
label_value_ties_tab4 = ttk.Label(tab4, textvariable=var_ties,style="TLabel")
label_value_ties_tab4.grid(row=8, column=1, sticky="w")
label_relative_value_ties=ttk.Label(tab4, textvariable=var_relative_value_ties,style="TLabel")
label_relative_value_ties.grid(row=8, column=2, sticky="w")

frame_stats_buttons=ttk.Frame(tab4)
frame_stats_buttons.grid(row=9, column=0, columnspan=3,pady=15)
button_reset_stats=ttk.Button(frame_stats_buttons, text="Reset Stats", style="TButton", command=lambda: reset_all_stats())
button_reset_stats.grid(row=0, column=0)
button_reset_end_states=ttk.Button(frame_stats_buttons, text="Reset End States", style="TButton", command=lambda: reset_end_states())
button_reset_end_states.grid(row=0, column=1)

def mainmenu_run():
    root.mainloop()
