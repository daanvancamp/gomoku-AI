import sys
from threading import Thread
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ai
import filereader
import stats
from PIL import Image, ImageTk
from lezen_stukken_en_muziek import TE_DETECTEREN_KLEUR, initialiseer_spelbord_json_bestanden
from filereader import log_info_overruling
import modelmanager
import gomoku

#todo: make the GUI fullscreen, add webcam view
#todo: make it look nice, make it bigger

WIDTH = 500 #origineel 230
HEIGHT = 700 #origineel 315

gomoku_ai = ai.GomokuAI(15)#board_size
game_instance = gomoku.GomokuGame(filereader.create_gomoku_game("consts.json"))
modelmanager_instance = modelmanager.ModelManager()

root = Tk()
root.geometry(str(WIDTH) + "x" + str(HEIGHT))
root.title("Gomoku -- Main Menu")
if TE_DETECTEREN_KLEUR=="Blauw":
    root.configure(bg="blue")
elif TE_DETECTEREN_KLEUR=="Rood":
    root.configure(bg="red")
else:
    raise Exception("Unknown color, change the color of the background here... Add if statement and you're done.")

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
game_runs = StringVar()
game_runs.set("1")
delayvar = BooleanVar()
delayvar.set(False)
logvar = BooleanVar()
logvar.set(False)
repvar = BooleanVar()
repvar.set(True)
replay_path = StringVar()
replay_path.set("")
var_allow_overrule=BooleanVar()
var_allow_overrule.set(True)

var_start_from_file=BooleanVar()
var_start_from_file.set(False)
state_board_path=StringVar()
state_board_path.set(r".\test_situations\specific_situation.txt")
name_model=StringVar()
var_model_player1=StringVar()
var_model_player2=StringVar()
var_use_recognition=BooleanVar()
var_use_recognition.set(False)
var_model_player1.set("standaard")
var_model_player2.set("standaard")
var_startingPlayer=StringVar()

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
    file_path = filedialog.askopenfilename(filetypes=[("txt File", "*.txt")])
    state_board_path.set(file_path)

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("Json File", "*.json")])
    replay_path.set(file_path)
   
def replay():
    p1.set("replay")
    set_player_type(0)
    p2.set("replay")
    set_player_type(1)
    game_runs.set("1")
    moves = filereader.load_replay(replay_path.get())
    if moves is not None:
        start_new_game(False, moves)


def run():
    gomoku.run(game_instance)

def load_board_from_file()->list[list[int]]:
    print("Load " + state_board_path.get())
    with open(state_board_path.get(), "r") as file:
        board = [[0] * 15 for _ in range(15)] # 0 = empty, 1 = player 1, 2 = player 2.
        for row in range(15):
            line = file.readline()
            for col in range(15):      
                board[row][col]=int(line[col])
    return board

def start_new_game():
    global allow_overrule, use_recognition, current_player, player1, player2
    
    log_info_overruling("\n\n\nnew session begins:")
    
    allow_overrule = var_allow_overrule.get()
    use_recognition = var_use_recognition.get()

    if var_startingPlayer.get() == "Player 1":
        gomoku.current_player = gomoku.player1
    else:
        gomoku.current_player = gomoku.player2

    try:
        initialiseer_spelbord_json_bestanden()
    except:
        raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")
    try:
        game_instance.ai_delay = delayvar.get()
        stats.should_log = logvar.get()
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
                runs = int(game_runs.get())
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
            
            if var_start_from_file.get():
                try:
                    board = load_board_from_file()
                    print("Bord geladen")
                    for row in board:
                        print(row)
                    game_instance.set_board(board)
                except Exception as e:
                    print("error in gomoku.run, herschrijf die functie.")
                    raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))

            try:
                gomoku.runGame(game_instance, i, False) #kan als hoofdprogramma beschouwd worden (één spel is één run)
            except Exception as e:
                print("error in gomoku.run, herschrijf die functie.")
                raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))
            print("voor if")
                    
    except ValueError:
        print("Most likely: Game runs value invalid, try again.")
    
    game_over()


def start_new_training():
    global allow_overrule, use_recognition, current_player, player1, player2
    
    log_info_overruling("\n\n\nnew session begins:")
    
    allow_overrule = var_allow_overrule.get()
    use_recognition = var_use_recognition.get()

    if var_startingPlayer.get() == "Player 1":
        gomoku.current_player = gomoku.player1
    else:
        gomoku.current_player = gomoku.player2

    try:
        initialiseer_spelbord_json_bestanden()
    except:
        raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")
    try:
        print("training mode")
        gomoku.player1.set_player_type("AI-Model")
        gomoku.player1.load_model(var_model_player1.get())
        
        gomoku.player2.set_player_type(var_playerType2.get())
        if (gomoku.player2.get_player_type() == "AI-Model" ):
            gomoku.player2.load_model(var_model_player2.get())        
        
        valid_number = False
        while not valid_number:
            try:
                runs = int(game_runs.get())
                valid_number=True
            except:
                print("invalid number, try again")

        game_instance.ai_delay = delayvar.get()
        stats.should_log = logvar.get()
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
            
            if var_start_from_file.get():
                try:
                    board = load_board_from_file()
                    print("Bord geladen")
                    for row in board:
                        print(row)
                    game_instance.set_board(board)
                except Exception as e:
                    print("error in gomoku.run, herschrijf die functie.")
                    raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))

            try:
                gomoku.runTraining(game_instance, i, True) #kan als hoofdprogramma beschouwd worden (één spel is één run)
            except Exception as e:
                print("error in gomoku.run, herschrijf die functie.")
                raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))
            print("voor if")

            for i in range(10):
                print("training round done...")
            gomoku_ai.decrease_learning_rate()#todo: calculate decrease rate based on number of training rounds
            print("players:",p1,p2)
            if gomoku.player1.get_player_type() == "AI-Model":
                modelmanager_instance.log_number_of_training_loops(var_model_player1.get(), 1)#add one to the number of training loops
            elif gomoku.player2.get_player_type() == "AI-Model":
                modelmanager_instance.log_number_of_training_loops(var_model_player2.get(), 1)#add one to the number of training loops
                    
            else:
                pass                   
    except ValueError:
        print("Most likely: Game runs value invalid, try again.")
    
    game_over()



def start_new_replay(moves:dict=None):
    global allow_overrule, use_recognition, current_player, player1, player2,p1,p2
    
    log_info_overruling("\n\n\nnew session begins:")
    
    allow_overrule = var_allow_overrule.get()
    use_recognition = var_use_recognition.get()

    if var_startingPlayer.get() == "Player 1":
        gomoku.current_player = gomoku.player1
    else:
        gomoku.current_player = gomoku.player2

    try:
        initialiseer_spelbord_json_bestanden()
    except:
        raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")
    try:
        print("training mode")
        p1.set("AI-Model")
        set_player_type(0)
        valid_number = False
        while not valid_number:
            try:
                runs = int(game_runs.get())
                valid_number=True
            except:
                print("invalid number, try again")

        game_instance.ai_delay = delayvar.get()
        stats.should_log = logvar.get()
        stats.setup_logging(p1.get(), p2.get())
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
            
            if var_start_from_file.get():
                try:
                    board = load_board_from_file()
                    print("Bord geladen")
                    for row in board:
                        print(row)
                    game_instance.set_board(board)
                except Exception as e:
                    print("error in gomoku.run, herschrijf die functie.")
                    raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))

            try:               
                gomoku.runReplay(game_instance, i, moves) #kan als hoofdprogramma beschouwd worden (��n spel is ��n run)
            except Exception as e:
                print("error in gomoku.run, herschrijf die functie.")
                raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))
            print("voor if")

            for i in range(10):
                print("training round done...")
            gomoku_ai.decrease_learning_rate()#todo: calculate decrease rate based on number of training rounds
            print("players:",p1,p2)
            if p1.get() == "AI-Model":
                modelmanager_instance.log_number_of_training_loops(gomoku.player1.get_model_name(), 1)#add one to the number of training loops
            elif p2.get() == "AI-Model":
                modelmanager_instance.log_number_of_training_loops(gomoku.player2.get_model_name(), 1)#add one to the number of training loops 
            else:
                pass                   
    except ValueError:
        print("Most likely: Game runs value invalid, try again.")
    
    game_over()


def create_new_model():
    modelmanager_instance.create_new_model(name_model.get())
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

#style_numbers = ["georgia", 10, "white", 12, 2]#font, size, color, bold, underline (already defined)
style2=ttk.Style()
style2.configure("TButton", font=(style_numbers[0], style_numbers[1]),bg=style_numbers[2],ipadx=style_numbers[3],ipady=style_numbers[4],pady=15)#font=georgia, size=10;bg=white
style2.configure("TRadiobutton",fg="white",bg="green")
style2.configure("TEntry",fg="white",bg="green")
style2.configure("TLabel", font=(style_numbers[0], style_numbers[1]),fg="white",bg="green")#font=georgia, size=10
style2.configure("TCheckbutton", font=(style_numbers[0], style_numbers[1]),fg="white",bg="green")#font=georgia, size=10

### TABS ###
ttk.Label(tab1)


def toggle_visibility_write_last_active_tab_to_file():
    global last_active_tab
    tab_text ="Play gomoku"
    while True:
        try:
            old_tab_text= tab_text
            current_tab = tabControl.index(tabControl.select())
            tab_text = tabControl.tab(current_tab, "text")
            if tab_text=="Train" and old_tab_text!=tab_text:
                game_runs.set("3000")
            elif tab_text=="Play gomoku" and old_tab_text!=tab_text:
                game_runs.set("1")
            last_active_tab=tab_text
        except Exception as e:
            pass
            
        ##TAB 1##
        if var_playerType1.get()=="AI-Model":
            CbModel1.grid(row=6,column=0)

        else:
            CbModel1.grid_remove()

        if var_playerType2.get()=="AI-Model":
            CbModel2.grid(row=6,column=1)
        else:
            CbModel2.grid_remove()

        ##tab 2##
        if var_playerType2.get()=="AI-Model":
            CbModelTrain2.grid(row=6, column=0, sticky="w")
        else:
            CbModelTrain2.grid_remove()


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

Thread_visibility=Thread(target=toggle_visibility_write_last_active_tab_to_file)
Thread_visibility.start()

gamerunslabel = ttk.Label(tab1, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=7, column=0, sticky="w")
gamerunsentry = ttk.Entry(tab1, textvariable=game_runs,style="TEntry")
gamerunsentry.grid(row=7, column=1, sticky="w")

playerstartLabel = ttk.Label(tab1, text="Player to start: ",style="TLabel")
playerstartLabel.grid(row=8, column=0, sticky="w")

CbStartingPlayer = ttk.Combobox(tab1, state="readonly", values=["Player 1", "Player 2"], textvariable=var_startingPlayer)
CbStartingPlayer.current(0)
CbStartingPlayer.grid(row=8, column=1, sticky="w")

delaybutton = ttk.Checkbutton(tab1, text="Use AI Delay", variable=delayvar,style="TCheckbutton")
delaybutton.grid(row=9, column=0, sticky="w")
logbutton = ttk.Checkbutton(tab1, text="Create log file", variable=logvar,style="TCheckbutton") 
logbutton.grid(row=10, column=0, sticky="w")
replaybutton = ttk.Checkbutton(tab1, text="Save replays", variable=repvar,style="TCheckbutton") 
replaybutton.grid(row=11, column=0, sticky="w")
overrule_button=ttk.Checkbutton(tab1, text="Allow overrule", variable=var_allow_overrule,style="TCheckbutton")
overrule_button.grid(row=12, column=0, sticky="w")
use_recognition_button=ttk.Checkbutton(tab1, text="use recognition*", variable=var_use_recognition,style="TCheckbutton")
use_recognition_button.grid(row=13, column=0, sticky="w")
label_recognition=ttk.Label(tab1, text="*only turn on when you have a physical board, a webcam and the other repository: ",style="TLabel",wraplength=300)
label_recognition.grid(row=14, column=0, sticky="w",columnspan=2)


bottomframe = Frame(tab1, highlightbackground="blue", highlightthickness=1, borderwidth=1)
bottomframe.grid(row=16, column=0, sticky="w",columnspan=3, padx=5, pady=15)

start_from_file_button=ttk.Checkbutton(bottomframe, text="Load game situation", variable=var_start_from_file,style="TCheckbutton")
start_from_file_button.grid(row=0, column=0, sticky="w")
label_load_state=ttk.Label(bottomframe, text="Choose file board state: ",style="TLabel")
label_load_state.grid(row=1, column=0, sticky="w")
load_state_entry = ttk.Entry(bottomframe, textvariable=state_board_path, width=30,style="TEntry")
load_state_entry.grid(row=2, column=0, sticky="w")
button_browse_state_file = ttk.Button(bottomframe, text="...",style="TButton", command=lambda: browse_state_files())
button_browse_state_file.grid(row=2, column=1, sticky="w")


button_3 = ttk.Button(input_canvas, text="Quit Game", style="TButton", command=lambda: quit_game())
button_3.grid(row=1, column=0, sticky="e")

ttk.Label(tab2)
CbModelTrain1 = ttk.Combobox(tab2, state="readonly", values=list_models,textvariable=var_model_player1)
CbModelTrain1.grid(row=0, column=0, sticky="w")
button_2 = ttk.Button(tab2, text="Train", style="TButton", command=lambda: start_new_training())
button_2.grid(row=1, column=0, sticky="w")
train_opponent_label = ttk.Label(tab2, text="Train model against:", style="TLabel")
train_opponent_label.grid(row=2, column=0, sticky="w")
radiobutton7 = ttk.Radiobutton(tab2, text="Test Algorithm", variable=var_playerType2, value="Test Algorithm")
radiobutton7.grid(row=3, column=0, sticky="w")
radiobutton8 = ttk.Radiobutton(tab2, text="AI-Model", variable=var_playerType2, value="AI-Model", style="TRadiobutton")
radiobutton8.grid(row=4, column=0, sticky="w")
human_training_button=ttk.Radiobutton(tab2, text="Human", variable=var_playerType2, value="Human", style="TRadiobutton")
human_training_button.grid(row=5, column=0,sticky="w")
CbModelTrain2 = ttk.Combobox(tab2, state="readonly", values=list_models,textvariable=var_model_player2)
CbModelTrain2.grid(row=6, column=0, sticky="w")
gamerunslabel = ttk.Label(tab2, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=7, column=0, sticky="w")
gamerunsentry2 = ttk.Entry(tab2, textvariable=game_runs,style="TEntry")
gamerunsentry2.grid(row=8, column=0, sticky="w")
replaybutton2 = ttk.Checkbutton(tab2, text="Save replays", variable=repvar,style="TCheckbutton")
replaybutton2.grid(row=9, column=0, sticky="w")
overrule_button=ttk.Checkbutton(tab2, text="Allow overrule", variable=var_allow_overrule,style="TCheckbutton")
overrule_button.grid(row=10, column=0, sticky="w")

train_description = Label(tab2, text="It is recommended to run at least 3 000 games per training session.", font=(style_numbers[0], style_numbers[1]), wraplength=WIDTH-5, justify=LEFT)#origineel width-5
train_description.grid(row=11, column=0, sticky="w")

ttk.Label(tab3)
replaylabel = ttk.Label(tab3, text="Choose the replay file: ",style="TLabel")
replaylabel.grid(row=0, column=0, sticky="w")
replayentry = ttk.Entry(tab3, textvariable=replay_path, width=30,style="TEntry")
replayentry.grid(row=1, column=0, sticky="w")
button_4 = ttk.Button(tab3, text="...",style="TButton", command=lambda: browse_files())
button_4.grid(row=1, column=1, sticky="w")
delaybutton2 = ttk.Checkbutton(tab3, text="Use AI Delay", variable=delayvar, style="TCheckbutton")
delaybutton2.grid(row=2, column=0, sticky="w")
button_5 = ttk.Button(tab3, text="Play", style="TButton", command=lambda: replay())
button_5.grid(row=3, column=0)


ttk.Label(tab4) 
Lb1 = Listbox(tab4)
models = modelmanager_instance.get_list_models()
i  = 0
for model in models:
    Lb1.insert(i, model.split('\\')[-1])
    i+=1
Lb1.grid(row=1, column=1)

nameModelLabel = ttk.Label(tab4, text="Name of model: ",style="TLabel")
nameModelLabel.grid(row=2, column=0, sticky="w")
nameModelEntry = ttk.Entry(tab4, textvariable=name_model,style="TEntry")
nameModelEntry.grid(row=2, column=1, sticky="w")
nameModelEntry.bind("<Return>",lambda event: create_new_model())#push enter to make a new model (easier)
button_NewModel = ttk.Button(tab4, text="Make New Model", style="TButton", command=lambda: create_new_model())
button_NewModel.grid(row=3, column=0)
button_DeleteModel = ttk.Button(tab4, text="Delete Model", style="TButton", command=lambda: delete_model())
button_DeleteModel.grid(row=3, column=1)

def mainmenu_run():
    root.mainloop()
