import sys
from threading import Thread
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import filereader
import stats
from PIL import Image, ImageTk
from detect_pieces import initialiseer_spelbord_json_bestanden
from filereader import log_info_overruling
import modelmanager
import gomoku

#todo: make the GUI fullscreen, add webcam view
#todo: make it look nice, make it bigger

WIDTH = 400 #origineel 230
HEIGHT = 500 #origineel 315

game_instance = gomoku.GomokuGame(filereader.create_gomoku_game("consts.json"))
modelmanager_instance = modelmanager.ModelManager()


root = Tk()
root.geometry(str(WIDTH) + "x" + str(HEIGHT))
root.title("Gomoku -- Main Menu")
root.configure(background='green')
root.attributes("-topmost", True)

try:
    root.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('res/ico.png')))
except TclError:
    print("icoon kon niet geladen worden.")
    pass

# Maak een Style object aan
style2 = ttk.Style()
style2.theme_use('default')
style2.configure('TNotebook.Tab', background='green')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Play gomoku')
tabControl.add(tab2, text='Train')
tabControl.add(tab3, text='Replay old games')
tabControl.add(tab4, text='Define model')
tabControl.grid(row=0, sticky="w")

style_numbers = ["georgia", 10, "white", 12, 2]#font, size, color, bold, underline

input_canvas = Canvas(root, relief="groove", borderwidth=0, highlightthickness=0)
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

var_number_of_training_loops=IntVar()
var_number_of_training_loops.set(0)
var_number_of_training_loops_comboboxes_p1=IntVar()
var_number_of_training_loops_comboboxes_p1.set(0)
var_number_of_training_loops_comboboxes_p2=IntVar()
var_number_of_training_loops_comboboxes_p2.set(0)

def set_player_type(player_id):
    if player_id == 1:
        newtype = var_playerType1.get()
    else:
        newtype = var_playerType2.get()
    gomoku.players[player_id-1].set_player_type(newtype)

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

    if var_playerType1.get() == "AI-Model":
        gomoku.player1.load_model(var_model_player1.get())
        gomoku.player1.set_allow_overrule(var_allow_overrule_player_1.get())
    if var_playerType2.get() == "AI-Model":
        gomoku.player2.load_model(var_model_player2.get())
        gomoku.player2.set_allow_overrule(var_allow_overrule_player_2.get())
    if var_startingPlayer.get() == "Player 1":
        gomoku.current_player = gomoku.player1
    else:
        gomoku.current_player = gomoku.player2
    
    try:
        initialiseer_spelbord_json_bestanden()
    except:
        raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")

    game_instance.ai_delay = var_delay.get()
    stats.should_log = var_log.get()
    stats.setup_logging(var_playerType1.get(), var_playerType2.get())
        
    gomoku.player1.set_player_type(var_playerType1.get())
    gomoku.player2.set_player_type(var_playerType2.get())

    if (gomoku.player1.get_player_type() == "AI-Model" ):
        gomoku.player1.load_model(var_model_player1.get())
    if (gomoku.player2.get_player_type() == "AI-Model" ):
        gomoku.player2.load_model(var_model_player2.get())

    root.wm_state('iconic')
        
    valid_number = False

    while not valid_number:
        try:
            runs = int(var_game_runs.get())
            valid_number=True
        except:
            print("invalid number, try again")

    for i in range(runs):
        log_info_overruling("run "+str(i+1)+" begins:")
        try:
            initialiseer_spelbord_json_bestanden()#geen stukken op bord
        except:
            raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")
            
        stats.log_message(f"Game  {i+1} begins.")
        game_instance.current_game = i+1
        game_instance.last_round = (i+1 == runs)
        board_loaded=None
        if var_start_from_file.get():
            board = load_board_from_file()
            if board is not None:
                board_loaded=True
            else:
                board_loaded=False
            game_instance.set_board(board)
        if (board_loaded and var_start_from_file.get()) or not var_start_from_file.get():
            try:
                gomoku.runGame(game_instance, i, var_rep.get()) #kan als hoofdprogramma beschouwd worden (één spel is één run)
            except Exception as e:
                print("error in gomoku.run")
                raise Exception("There is an error in the main function/loop, it can be anything." , str(e))
        else:
            print("Please select a valid file that contains the board in the following format and try again:")
            for i in range(15):
                for b in range(15):
                    print(0, end="")
                print("\n",end="")
            print("The board can only contain 0, 1, or 2. 0 = empty, 1 = player 1, 2 = player 2.")
    
    game_over()


def start_new_training():
    global game_instance
    log_info_overruling("\n\n\nnew session begins:")
    
    game_instance.use_recognition = False
    game_instance.play_music = False

    gomoku.player1.set_player_type("AI-Model")
    gomoku.player2.set_player_type(var_playerType2.get())
    
    gomoku.player1.load_model(var_model_player1.get())#player 1 is always an AI-Model when training
    gomoku.player1.set_allow_overrule(var_allow_overrule_player_1.get())

    if gomoku.player2.get_player_type() == "AI-Model":
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
        stats.setup_logging(gomoku.player1.get_player_type(), gomoku.player2.get_player_type())
        root.wm_state('iconic')
        for i in range(runs):
            log_info_overruling("run "+str(i+1)+" begins:")
            try:
                initialiseer_spelbord_json_bestanden()#geen stukken op bord
            except:
                raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")
            
            stats.log_message(f"Game  {i+1} begins.")
            game_instance.current_game = i+1
            game_instance.last_round = (i+1 == runs)
            try:
                gomoku.runTraining(game_instance, i, True) #kan als hoofdprogramma beschouwd worden (één spel is één run)
            except Exception as e:
                print("error in gomoku.run, herschrijf die functie.")
                raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))

            if gomoku.player1.get_player_type() == "AI-Model":
                #gomoku.Player1 is an object of the class Player, ai is an object of the class gomokuAI and ai.decrease_learning_rate() is a method of the class gomokuAI
                gomoku.Player1.ai.decrease_learning_rate()#todo: calculate decrease rate based on number of training rounds
                modelmanager_instance.log_number_of_training_loops(var_model_player1.get(), 1,gomoku.player2.get_player_type())#add one to the number of training loops
            if gomoku.player2.get_player_type() == "AI-Model":
                #gomoku.Player2 is an object of the class Player, ai is an object of the class gomokuAI and ai.decrease_learning_rate() is a method of the class gomokuAI
                gomoku.Player2.ai.decrease_learning_rate()
                modelmanager_instance.log_number_of_training_loops(var_model_player2.get(), 1,gomoku.player1.get_player_type())#add one to the number of training loops
                #arguments: model_name, number_of_additional_training_loops, opponent
              
    except ValueError:
        print("Most likely: Game runs value invalid, try again.")
    
    game_over()


def start_new_replay():
    global game_instance
    
    log_info_overruling("\n\n\nnew session begins:")
   
    moves = filereader.load_replay(replay_path.get())

    if moves is None:
        replay_loaded=False
    else:
        replay_loaded=True
        print(moves)
    
    if replay_loaded:
        game_instance.use_recognition = False
        game_instance.play_music = False

        gomoku.player1.TYPE = "Replay"
        gomoku.player2.TYPE = "Replay"

        gomoku.current_player = gomoku.player1

        game_instance.ai_delay = var_delay.get()
        stats.should_log = var_log.get()
        stats.setup_logging(str(gomoku.player1), str(gomoku.player2))
        root.wm_state('iconic')

        try:
            initialiseer_spelbord_json_bestanden()#geen stukken op bord
        except:
            raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")
           
        try:               
            gomoku.runReplay(game_instance, moves) #kan als hoofdprogramma beschouwd worden (��n spel is ��n run)
        except Exception as e:
            print("error in gomoku.run, herschrijf die functie.")
            raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e)) 
    else:
        print("Try again, please select a valid json file")
    game_over()
    root.wm_state('normal')
def create_new_model():
    modelmanager_instance.create_new_model(var_name_model.get())
    refresh_models()

def delete_model():
    for i in Lb1.curselection():
        modelmanager_instance.delete_model(Lb1.get(i))
    refresh_models()
        
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
def game_over():
    root.wm_state('normal')
    game_instance.current_game = 0

def quit_game():
    sys.exit()#beeindig het programma volledig

def maintain_GUI():
    #delete this optional thread if the program stutters or crashes on your computer
    tab_text = "Play gomoku"
    last_value_repvar=True
    last_value_load_board_from_file=False
    while True:
        sleep(0.1)
        try:
            old_tab_text= tab_text
            current_tab = tabControl.index(tabControl.select())
            tab_text = tabControl.tab(current_tab, "text")
            if tab_text=="Train" and old_tab_text!=tab_text:
                var_game_runs.set("3000")
            elif tab_text=="Play gomoku" and old_tab_text!=tab_text:
                var_game_runs.set("1")
        except:
            pass
            
        ##TAB 1##
        if var_playerType1.get() == "Human" and var_playerType2.get() == "Human":
            var_log.set(False)
            var_rep.set(False)
            logbutton.grid_remove()
            replaybutton.grid_remove()
        else:
            logbutton.grid()
            replaybutton.grid()


        if var_playerType1.get()=="AI-Model":
            CbModel1.grid()
            overrule_button_player_1.grid()
            label_value_number_of_training_loops_p1.grid()

        else:
            CbModel1.grid_remove()
            overrule_button_player_1.grid_remove()
            label_value_number_of_training_loops_p1.grid_remove()

        if var_playerType2.get()=="AI-Model":
            CbModel2.grid()
            overrule_button_player_2.grid()
            overrule_button_player_2_tab2.grid()
            label_value_number_of_training_loops_p2.grid()
        else:
            CbModel2.grid_remove()
            overrule_button_player_2.grid_remove()
            overrule_button_player_2_tab2.grid_remove()
            label_value_number_of_training_loops_p2.grid_remove()

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
            use_recognition_button.grid()
            label_recognition.grid()
        else:
            use_recognition_button.grid_remove()
            label_recognition.grid_remove()
        #tab 1, delaybutton#
        if (var_playerType1.get()=="AI-Model" or var_playerType2.get()=="AI-Model" ) or (var_playerType1.get()=="Test Algorithm" or var_playerType2.get()=="Test Algorithm"):
            delaybutton.grid()
        else:
            delaybutton.grid_remove()
        #tab1, music button#
        if var_playerType1.get()=="Human" or var_playerType2.get()=="Human":
            music_button.grid()
        else:
            music_button.grid_remove()

        #starting player
        if var_playerType1.get()==var_playerType2.get() and var_playerType1=="Test Algorithm": #option not relevant
            playerstartLabel.grid_remove()
            CbStartingPlayer.grid_remove()
        else:
            playerstartLabel.grid()
            CbStartingPlayer.grid()

        if var_start_from_file.get()!=last_value_load_board_from_file and var_start_from_file.get()==True:
            var_rep.set(False) #can't be used simultanously because if you would save a replay file, it wouldn't be complete (the moves that are loaded are gone)
            
            last_value_load_board_from_file=var_start_from_file.get()
            last_value_repvar=var_rep.get()
        if var_rep.get()!=last_value_repvar and var_rep.get()==True:
            var_start_from_file.set(False)

            last_value_load_board_from_file=var_start_from_file.get()
            last_value_repvar=var_rep.get()

        if var_playerType2.get()=="Human":
            train_description.grid_remove() #a human will never play the game 3000 times to train the model
        else:
            train_description.grid()
        if var_playerType2.get()=="AI-Model":
            CbModelTrain2.grid()
        else:
            CbModelTrain2.grid_remove()
        

        show_number_of_training_loops()
        show_number_of_training_loops_comboboxes()


def show_number_of_training_loops():
    for i in Lb1.curselection():
        model=Lb1.get(i)
    try:
        var_number_of_training_loops.set(modelmanager_instance.get_total_number_of_training_loops(model))
    except:
        pass

def show_number_of_training_loops_comboboxes():
    var_number_of_training_loops_comboboxes_p1.set(modelmanager_instance.get_total_number_of_training_loops(var_model_player1.get()))
    
    var_number_of_training_loops_comboboxes_p2.set(modelmanager_instance.get_total_number_of_training_loops(var_model_player2.get()))
    
Thread_maintain_GUI=Thread(target=maintain_GUI,daemon=True)#end when main program ends
Thread_maintain_GUI.start()

#style_numbers = ["georgia", 10, "white", 12, 2]#font, size, color, bold, underline (already defined)
style2=ttk.Style()
style2.configure("TButton", font=(style_numbers[0], style_numbers[1]),bg=style_numbers[2],ipadx=style_numbers[3],ipady=style_numbers[4],pady=15)#font=georgia, size=10;bg=white
style2.configure("TRadiobutton",fg="white",bg="green")
style2.configure("TEntry",fg="white",bg="green")
style2.configure("TLabel", font=(style_numbers[0], style_numbers[1]),fg="white",bg="green")#font=georgia, size=10
style2.configure("TCheckbutton", font=(style_numbers[0], style_numbers[1]),fg="white",bg="green")#font=georgia, size=10

### TABS ###
ttk.Label(tab1)

button_1 = ttk.Button(tab1, text="New Game", command=lambda: start_new_game(), style="TButton")
button_1.grid(row=0, column=0, sticky="w")
player1typelabel = ttk.Label(tab1,style="TLabel", text="Player 1(black)")
player1typelabel.grid(row=2, column=0, sticky="w")
player2typelabel = ttk.Label(tab1, text="Player 2(white)", style="TLabel")
player2typelabel.grid(row=2, column=1, sticky="w")

radiobutton1 = ttk.Radiobutton(tab1, text="Human", variable=var_playerType1, value="Human", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton1.grid(row=3, column=0, sticky="w")
radiobutton2 = ttk.Radiobutton(tab1, text="Test Algorithm", variable=var_playerType1, value="Test Algorithm", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton2.grid(row=4, column=0, sticky="w")
radiobutton3 = ttk.Radiobutton(tab1, text="AI-Model", variable=var_playerType1, value="AI-Model", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton3.grid(row=5, column=0, sticky="w")
radiobutton4 = ttk.Radiobutton(tab1, text="Human", variable=var_playerType2, value="Human", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton4.grid(row=3, column=1, sticky="w")
radiobutton5 = ttk.Radiobutton(tab1, text="Test Algorithm", variable=var_playerType2, value="Test Algorithm", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton5.grid(row=4, column=1, sticky="w")
radiobutton6 = ttk.Radiobutton(tab1, text="AI-Model", variable=var_playerType2, value="AI-Model", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton6.grid(row=5, column=1, sticky="w")

list_models = modelmanager_instance.get_list_models()
CbModel1 = ttk.Combobox(tab1, state="readonly", values=list_models,textvariable=var_model_player1)
CbModel2 = ttk.Combobox(tab1, state="readonly", values=list_models,textvariable=var_model_player2)

CbModel1.grid(row=6, column=0)
CbModel2.grid(row=6, column=1)

label_value_number_of_training_loops_p1 = ttk.Label(tab1, textvariable=var_number_of_training_loops_comboboxes_p1,style="TLabel")
label_value_number_of_training_loops_p1.grid(row=8, column=0, sticky="w")

label_value_number_of_training_loops_p2 = ttk.Label(tab1, textvariable=var_number_of_training_loops_comboboxes_p2,style="TLabel")
label_value_number_of_training_loops_p2.grid(row=8, column=1, sticky="w")


overrule_button_player_1=ttk.Checkbutton(tab1, text="Allow overrule", variable=var_allow_overrule_player_1,style="TCheckbutton")
overrule_button_player_1.grid(row=9, column=0, sticky="w")

overrule_button_player_2=ttk.Checkbutton(tab1, text="Allow overrule", variable=var_allow_overrule_player_2,style="TCheckbutton")
overrule_button_player_2.grid(row=9, column=1, sticky="w")


gamerunslabel = ttk.Label(tab1, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=10, column=0, sticky="w")
gamerunsentry = ttk.Entry(tab1, textvariable=var_game_runs,style="TEntry")
gamerunsentry.grid(row=10, column=1, sticky="w")

playerstartLabel = ttk.Label(tab1, text="Player to start: ",style="TLabel")
playerstartLabel.grid(row=11, column=0, sticky="w")
CbStartingPlayer = ttk.Combobox(tab1, state="readonly", values=["Player 1", "Player 2"], textvariable=var_startingPlayer)
CbStartingPlayer.current(0)
CbStartingPlayer.grid(row=11, column=1, sticky="w")

#column 0
logbutton = ttk.Checkbutton(tab1, text="Create log file", variable=var_log,style="TCheckbutton") 
logbutton.grid(row=12, column=0, sticky="w")
replaybutton = ttk.Checkbutton(tab1, text="Save replays(1)", variable=var_rep,style="TCheckbutton") 
replaybutton.grid(row=13, column=0, sticky="w")
delaybutton = ttk.Checkbutton(tab1, text="Use AI Delay", variable=var_delay,style="TCheckbutton")
delaybutton.grid(row=14, column=0, sticky="w")

#column1
music_button=ttk.Checkbutton(tab1, text="Play music", variable=var_play_music,style="TCheckbutton")
music_button.grid(row=12, column=1, sticky="w")
use_recognition_button=ttk.Checkbutton(tab1, text="use recognition*", variable=var_use_recognition,style="TCheckbutton")
use_recognition_button.grid(row=13, column=1, sticky="w")


label_recognition=ttk.Label(tab1, text="*only turn on when you have a physical board, a webcam and the other repository: ",style="TLabel",wraplength=300)
label_recognition.grid(row=15, column=0, sticky="w",columnspan=2)


bottomframe = Frame(tab1, highlightbackground="blue", highlightthickness=3, borderwidth=1)
bottomframe.grid(row=16, column=0, sticky="w",columnspan=3, padx=5, pady=15)

start_from_file_button=ttk.Checkbutton(bottomframe, text="Load game situation(2)", variable=var_start_from_file,style="TCheckbutton")
start_from_file_button.grid(row=0, column=0, sticky="w")
label_load_state=ttk.Label(bottomframe, text="Choose file board state: ",style="TLabel")
label_load_state.grid(row=1, column=0, sticky="w")
load_state_entry = ttk.Entry(bottomframe, textvariable=state_board_path, width=30,style="TEntry")
load_state_entry.grid(row=2, column=0, sticky="w")
button_browse_state_file = ttk.Button(bottomframe, text="...",style="TButton", command=lambda: browse_state_files())
button_browse_state_file.grid(row=2, column=1, sticky="w")


button_3 = ttk.Button(input_canvas, text="Quit Game(ESC/Q)", style="TButton", command=lambda: quit_game())
button_3.grid(row=1, column=0, sticky="e")
root.bind("<Escape>", lambda event: quit_game())
root.bind("<q>", lambda event: quit_game())

label_info_load_save_replay=ttk.Label(tab1,wraplength=300, text="(1)(2)The save replay function can't be used when loading a board, because that would create a wrong replay file ",style="TLabel")
label_info_load_save_replay.grid(row=17, column=0, sticky="w",columnspan=2,pady=5)

ttk.Label(tab2)
#row 0
button_2 = ttk.Button(tab2, text="Train", style="TButton", command=lambda: start_new_training())
button_2.grid(row=0, column=1, sticky="e")

#column 0
label_model=ttk.Label(tab2, text="AI-Model: ",style="TLabel")
label_model.grid(row=1, column=0, sticky="w",padx=10,pady=1)
CbModelTrain1 = ttk.Combobox(tab2, state="readonly", values=list_models,textvariable=var_model_player1)
CbModelTrain1.grid(row=2, column=0, sticky="w",padx=10,pady=1)
label_value_number_of_training_loops_tab2_p1 = ttk.Label(tab2, textvariable=var_number_of_training_loops_comboboxes_p1,style="TLabel")
label_value_number_of_training_loops_tab2_p1.grid(row=3, column=0, sticky="w")
overrule_button_player_1_tab2=ttk.Checkbutton(tab2, text="Allow overrule", variable=var_allow_overrule_player_1,style="TCheckbutton")
overrule_button_player_1_tab2.grid(row=4, column=0, sticky="w")


train_opponent_label = ttk.Label(tab2, text="Train model against:", style="TLabel")
train_opponent_label.grid(row=1, column=1, sticky="w")
radiobutton7 = ttk.Radiobutton(tab2, text="Test Algorithm", variable=var_playerType2, value="Test Algorithm")
radiobutton7.grid(row=2, column=1, sticky="w")
radiobutton8 = ttk.Radiobutton(tab2, text="AI-Model", variable=var_playerType2, value="AI-Model", style="TRadiobutton")
radiobutton8.grid(row=3, column=1, sticky="w")
human_training_button=ttk.Radiobutton(tab2, text="Human", variable=var_playerType2, value="Human", style="TRadiobutton")
human_training_button.grid(row=4, column=1,sticky="w")
CbModelTrain2 = ttk.Combobox(tab2, state="readonly", values=list_models,textvariable=var_model_player2)
CbModelTrain2.grid(row=5, column=1, sticky="w")
label_value_number_of_training_loops_tab2_p2 = ttk.Label(tab2, textvariable=var_number_of_training_loops_comboboxes_p2,style="TLabel")
label_value_number_of_training_loops_tab2_p2.grid(row=6, column=1, sticky="w")
overrule_button_player_2_tab2=ttk.Checkbutton(tab2, text="Allow overrule", variable=var_allow_overrule_player_2,style="TCheckbutton")
overrule_button_player_2_tab2.grid(row=7, column=1, sticky="w")

gamerunslabel = ttk.Label(tab2, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=8, column=0, sticky="w",pady=2)
gamerunsentry2 = ttk.Entry(tab2, textvariable=var_game_runs,style="TEntry")
gamerunsentry2.grid(row=9, column=0, sticky="w")
replaybutton2 = ttk.Checkbutton(tab2, text="Save replays", variable=var_rep,style="TCheckbutton")
replaybutton2.grid(row=10, column=0, sticky="w")


train_description = Label(tab2, text="It is recommended to run at least 3 000 games per training session.", font=(style_numbers[0], style_numbers[1]), wraplength=WIDTH-5, justify=LEFT)#origineel width-5
train_description.grid(row=11, column=0, sticky="w",columnspan=2)

ttk.Label(tab3)
replaylabel = ttk.Label(tab3, text="Choose the replay file: ",style="TLabel")
replaylabel.grid(row=0, column=0, sticky="w")
replayentry = ttk.Entry(tab3, textvariable=replay_path, width=30,style="TEntry")
replayentry.grid(row=1, column=0, sticky="w")
button_4 = ttk.Button(tab3, text="...",style="TButton", command=lambda: browse_files())
button_4.grid(row=1, column=1, sticky="w")
delaybutton2 = ttk.Checkbutton(tab3, text="Use AI Delay", variable=var_delay, style="TCheckbutton")
delaybutton2.grid(row=2, column=0, sticky="w")
button_5 = ttk.Button(tab3, text="Play", style="TButton", command=lambda: start_new_replay())
button_5.grid(row=3, column=0)


ttk.Label(tab4)
Lb1 = Listbox(tab4)

models = modelmanager_instance.get_list_models()
i  = 0
for model in models:
    Lb1.insert(i, model.split('\\')[-1])
    i+=1
Lb1.grid(row=1, column=1)

for item in models:
    if item=="standaard"or item=="Standaard":
        Lb1.selection_set(models.index(item))
        Lb1.activate(models.index(item))

nameModelLabel = ttk.Label(tab4, text="Name of model: ",style="TLabel")
nameModelLabel.grid(row=2, column=0, sticky="w")
nameModelEntry = ttk.Entry(tab4, textvariable=var_name_model,style="TEntry")
nameModelEntry.grid(row=2, column=1, sticky="w")
nameModelEntry.bind("<Return>",lambda event: create_new_model())#push enter to make a new model (easier)
button_NewModel = ttk.Button(tab4, text="Make New Model", style="TButton", command=lambda: create_new_model())
button_NewModel.grid(row=3, column=0)
button_DeleteModel = ttk.Button(tab4, text="Delete Model", style="TButton", command=lambda: delete_model())
button_DeleteModel.grid(row=3, column=1)

label_number_of_training_loops = ttk.Label(tab4, text="Training loops: ",style="TLabel")
label_number_of_training_loops.grid(row=4, column=0, sticky="w")
label_value_number_of_training_loops_tab4 = ttk.Label(tab4, textvariable=var_number_of_training_loops,style="TLabel")
label_value_number_of_training_loops_tab4.grid(row=4, column=1, sticky="w")

Thread(target=show_number_of_training_loops, daemon=True).start()

def mainmenu_run():
    root.mainloop()
