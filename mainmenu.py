import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import gomoku
from ai import GomokuAI
gomoku_ai=GomokuAI(15)#board_size
import filereader
import stats
from PIL import Image, ImageTk
from lezen_stukken_en_trivia import TE_DETECTEREN_KLEUR, initialiseer_spelbord_json_bestanden
from filereader import log_info_overruling
#todo: make it look nice
#add sound effects

WIDTH = 340 #origineel 230
HEIGHT = 315 #origineel 315
game_instance = gomoku.GomokuGame(filereader.create_gomoku_game("consts.json"))

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

# Configureer de stijl voor de TNotebook.Tab
style2.configure('TNotebook.Tab', background='green')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Play gomoku')
tabControl.add(tab2, text='Train')
tabControl.add(tab3, text='Replay old games')
tabControl.add(tab4, text='load a situation')
tabControl.grid(row=0, sticky="w")

style_numbers = ["georgia", 10, "white", 12, 2]#font, size, color, bold, underline

input_canvas = Canvas(root, relief="groove", borderwidth=0, highlightthickness=0)
input_canvas.grid(row=1, padx=2, pady=2)
p1 = StringVar()
p2 = StringVar()
p1.set("Human")
p2.set("MM-AI")
game_runs = StringVar()
game_runs.set("1")
delayvar = BooleanVar()
delayvar.set(False)
logvar = BooleanVar()
logvar.set(False)
repvar = BooleanVar()
repvar.set(False)
replay_path = StringVar()
replay_path.set("")
var_allow_overrule=BooleanVar()
var_allow_overrule.set(True)
var_human_training=BooleanVar()
var_human_training.set(False)
load_situation_path=StringVar()#todo: add full functionality
load_situation_path.set(None)

def set_player_type(playerid):
    if playerid == 0:
        newtype = p1.get()
    else:
        newtype = p2.get()
    gomoku.players[playerid].set_player(newtype, playerid)

def set_game_instance(new_instance):
    global game_instance
    game_instance = new_instance

def browes_files_load_situation():
    file_path = filedialog.askopenfilename(filetypes=[("txt File", "*.txt")])

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("Json File", "*.json")])
    replay_path.set(file_path)

def load_situation():
    load_situation=True
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

def load_board_from_file(): #todo: add full functionality (load board from file)
    with open("specific_situation.txt", "r") as file:
        board = [[0] * 15 for _ in range(15)] # 0 = empty, 1 = player 1, 2 = player 2. De waarden corresponderen aan de kleuren.
        for rij in range(15):
            print(rij)
            line = file.readline()
            print(line)
            for kolom in range(15): # idx=1, i=eerste karakter van de lijn
                
                board[rij][kolom]=int(line[kolom])



        for row in board:
            print(row)
def schrijf_bool_naar_tekstbestand():
    with open("bool_overrule.txt", "w") as f:
        f.write(str(var_allow_overrule.get()))
        if var_allow_overrule.get():
            print("overruling of the model is turned on")
        else:
            print("overruling of the model is turned off")

def start_new_game(is_training=False, moves:dict=None):
    schrijf_bool_naar_tekstbestand()
    log_info_overruling("\n\n\nnew session begins:")
    #if load_situation:
        #board=[]
        #todo:implement further #board=...
      #  board=load_board=
        

   
    try:
        initialiseer_spelbord_json_bestanden()
    except:
        raise Exception("Fout in functie: initialiseer_spelbord_json_bestanden")
    try:
        if is_training:
            if not var_human_training.get():
                p1.set("MM-AI")
                set_player_type(0)
            else:
                p1.set("Human")
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
            #todo: add code here #draw_board
            try:
                gomoku.run(game_instance, i, is_training, repvar.get(), moves) #kan als hoofdprogramma beschouwd worden (��n spel is ��n run)
            except Exception as e:
                print("error in gomoku.run, herschrijf die functie.")
                raise Exception("De error is waarschijnlijk te wijten aan een foute zet, controleer het lezen van de json bestanden die het bord opslaan." , str(e))
            
            gomoku_ai.decrease_learning_rate()

    except ValueError:
        print("Most likely: Game runs value invalid, try again.")
    
    game_over()

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
button_1 = ttk.Button(tab1, text="New Game", command=lambda: start_new_game(False), style="TButton")
button_1.grid(row=0, column=0, sticky="w")
player1typelabel = ttk.Label(tab1,style="TLabel", text="Player 1")
player1typelabel.grid(row=2, column=0, sticky="w")
player2typelabel = ttk.Label(tab1, text="Player 2", style="TLabel")
player2typelabel.grid(row=2, column=1, sticky="w")

radiobutton1 = ttk.Radiobutton(tab1, text="Human", variable=p1, value="Human", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton1.grid(row=3, column=0, sticky="w")
radiobutton2 = ttk.Radiobutton(tab1, text="TestAI", variable=p1, value="AI", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton2.grid(row=4, column=0, sticky="w")
radiobutton3 = ttk.Radiobutton(tab1, text="MM-AI", variable=p1, value="MM-AI", command=lambda: set_player_type(0),style="TRadiobutton")
radiobutton3.grid(row=5, column=0, sticky="w")
radiobutton4 = ttk.Radiobutton(tab1, text="Human", variable=p2, value="Human", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton4.grid(row=3, column=1, sticky="w")
radiobutton5 = ttk.Radiobutton(tab1, text="TestAI", variable=p2, value="AI", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton5.grid(row=4, column=1, sticky="w")
radiobutton6 = ttk.Radiobutton(tab1, text="MM-AI", variable=p2, value="MM-AI", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton6.grid(row=5, column=1, sticky="w")

gamerunslabel = ttk.Label(tab1, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=6, column=0, sticky="w")
gamerunsentry = ttk.Entry(tab1, textvariable=game_runs,style="TEntry")
gamerunsentry.grid(row=6, column=1, sticky="w")

delaybutton = ttk.Checkbutton(tab1, text="Use AI Delay", variable=delayvar,style="TCheckbutton")
delaybutton.grid(row=7, column=0, sticky="w")
logbutton = ttk.Checkbutton(tab1, text="Create log file", variable=logvar,style="TCheckbutton") 
logbutton.grid(row=8, column=0, sticky="w")
replaybutton = ttk.Checkbutton(tab1, text="Save replays", variable=repvar,style="TCheckbutton") 
replaybutton.grid(row=9, column=0, sticky="w")
overrule_button=ttk.Checkbutton(tab1, text="Allow overrule", variable=var_allow_overrule,style="TCheckbutton")
overrule_button.grid(row=10, column=0, sticky="w")
button_3 = ttk.Button(input_canvas, text="Quit Game", style="TButton", command=lambda: quit_game())
button_3.grid(row=1, column=0, sticky="e")


ttk.Label(tab2)
button_2 = ttk.Button(tab2, text="Train", style="TButton", command=lambda: start_new_game(True))
button_2.grid(row=0, column=0, sticky="w")
train_opponent_label = ttk.Label(tab2, text="Train against:", style="TLabel")
train_opponent_label.grid(row=1, column=0, sticky="w")
radiobutton7 = ttk.Radiobutton(tab2, text="MM-AI", variable=p2, value="MM-AI", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton7.grid(row=2, column=0, sticky="w")
radiobutton8 = ttk.Radiobutton(tab2, text="TestAI", variable=p2, value="AI", command=lambda: set_player_type(1),style="TRadiobutton")
radiobutton8.grid(row=3, column=0, sticky="w")
gamerunslabel = ttk.Label(tab2, text="Number of games: ",style="TLabel")
gamerunslabel.grid(row=4, column=0, sticky="w")
gamerunsentry2 = ttk.Entry(tab2, textvariable=game_runs,style="TEntry")
gamerunsentry2.grid(row=5, column=0, sticky="w")
replaybutton2 = ttk.Checkbutton(tab2, text="Save replays", variable=repvar,style="TCheckbutton")
replaybutton2.grid(row=6, column=0, sticky="w")
overrule_button=ttk.Checkbutton(tab2, text="Allow overrule", variable=var_allow_overrule,style="TCheckbutton")
overrule_button.grid(row=7, column=0, sticky="w")
human_training_button=ttk.Checkbutton(tab2, text="training against human", variable=var_human_training,style="TCheckbutton")
human_training_button.grid(row=6, column=1,sticky="w")
train_description = Label(tab2, text="It is recommended to run at least 3 000 games per training session.", font=(style_numbers[0], style_numbers[1]), wraplength=WIDTH-5, justify=LEFT)#origineel width-5
train_description.grid(row=8, column=0, sticky="w")


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

ttk.Label(tab4) #todo: implement further functionality
label_load_situation=ttk.Label(tab4, text="Choose the file from which to load a situation: ",style="TLabel")
label_load_situation.grid(row=0, column=0, sticky="w")
load_situation_entry = ttk.Entry(tab4, textvariable=load_situation_path, width=30,style="TEntry")
load_situation_entry.grid(row=1, column=0, sticky="w")
button_6 = ttk.Button(tab4, text="...",style="TButton", command=lambda: browes_files_load_situation())
button_6.grid(row=1, column=1, sticky="w")
button_7 = ttk.Button(tab4, text="Load Situation", style="TButton", command=lambda: load_situation())
button_7.grid(row=3, column=0)

def mainmenu_run():
    root.mainloop()
