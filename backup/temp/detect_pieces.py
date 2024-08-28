import json
from typing import List, Tuple, Dict, Any
from threading import Thread

path_pieces_before_move=r".\board_gomoku\board_before_move.json"
path_pieces_after_move=r".\board_gomoku\board_after_move.json"

COLOR_TO_DETECT:str = "Blauw"

def recognize_move():
    moves_human=get_relevant_move()
    print("human_moves:",moves_human)
    thread_check_delay=Thread(target=check_delay_data)
    thread_check_delay.start()
    for i in moves_human:
        try:
            int(i[0])
            int(i[1])

        except:
            raise Exception("The coordinates are not integers. Please try again. (x,y)")
    try:
        if len(moves_human)==0:
            raise Exception("No moves were found")

        elif len(moves_human)==1:
            print("1 zet, super")
            x,y=moves_human[0]
            answer=input("Is this move correct? :",x,y)
            #=debugging
            if answer=="ja" or answer=="" or answer.lower().strip()=="yes":
                pass
            else:
                raise Exception("")
            return x,y

        elif moves_human is None:
            raise Exception("Geen zetten, of variabele niet gedeclareerd")
        else:
            raise Exception("Meerdere zetten")

        
    except Exception as e:
        print("something went wrong with the recognition of the pieces:",e)
        return (None,None)


def initialize_board_json_files():
    global path_pieces_before_move,path_pieces_after_move
    relevant_pieces=[]
    paths=[path_pieces_after_move,path_pieces_before_move]

    for pad in paths:
        try:
            with open(pad, 'w') as json_file:
                json.dump({'stukken': relevant_pieces}, json_file)#zie lees_van_json
        except PermissionError:
            print("Please close the file and try again")

def check_delay_data():
    global path_pieces_after_move
    data=read_from_json_file(path_pieces_after_move)
    if data: #eerste keer zal dit nog geen waarde hebben
        from datetime import datetime
        current_timestamp=datetime.now().isoformat()

        current_time=current_timestamp.split("T")[1]
        current_date=current_timestamp.split("T")[0]

        current_hours=int(current_time.split(":")[0])
        current_minutes=int(current_time.split(":")[1])
        current_seconds=float(current_time.split(":")[2])

        current_year=int(current_date.split("-")[0])
        current_month=int(current_date.split("-")[1])
        current_day=int(current_date.split("-")[2])

        current_timestamp_seconds=current_seconds+current_minutes*60+current_hours*3600

        print(data)
        time=data["timestamp"]
        date=time.split("T")[0]
        time=time.split("T")[1]

        year=int(date.split("-")[0])
        month=int(date.split("-")[1])
        day=int(date.split("-")[2])

        hours=int(time.split(":")[0])
        minutes=int(time.split(":")[1])
        seconds=float(time.split(":")[2])
        timestamp=seconds+minutes*60+hours*3600

        max_delay=3
        date_difference=(year!=current_year) or (month!=current_month) or (day!=current_day)
        time_difference= current_timestamp_seconds>timestamp+max_delay

        if date_difference or time_difference:
            raise Exception("Rewrite program, too much delay")
        else:
            print("delay is ok")
    
def read_from_json_file(path)-> List[Tuple[int, int]]:
    try:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
    except PermissionError:
        print("Please close the file and try again")
        return None

    return data["stukken"]#zie json.dump in schrijf_relevante_stukken_weg (dictionary naar lijst van tuples)

def get_relevant_move () -> List[Tuple[int, int]]:
    global path_pieces_after_move,path_pieces_before_move
    pieces_after_move=read_from_json_file(path_pieces_after_move)
    pieces_before_move=read_from_json_file(path_pieces_before_move)
    relevant_pieces=[]

    if pieces_after_move is None:
        pieces_after_move = []
    if pieces_before_move is None:
        raise Exception("error, rewrite function")
    
    for i in pieces_after_move: 
        if i not in pieces_before_move:
            relevant_pieces.append(i)
    if relevant_pieces is None:
        raise Exception("error, rewrite function")

    return relevant_pieces

def write_relevant_pieces_to_file(pad)->None:
    relevant_pieces = []
    data=read_detected_pieces()
    print("huidige_stukken:",data)
    
    if data:
        all_pieces = set((stuk['color'], stuk['coordinates'][0], stuk['coordinates'][1]) for stuk in data['pieces'])
    
        for kleur, x, y in all_pieces:
            if (kleur, x, y) not in relevant_pieces and kleur == COLOR_TO_DETECT:
                relevant_pieces.append((x, y))
        if len(relevant_pieces) > 0:
            print(f"Relevante stukken: {relevant_pieces}")
            try:
                with open(pad, 'w') as json_file:
                    json.dump({'stukken': relevant_pieces}, json_file)
            except PermissionError:
                print("Please close the file and try again")

        if relevant_pieces is None:
            print("Geen stukken van de relevante kleur gevonden, controleer beeldherkenning indien je fysiek wel een zet hebt uitgevoerd.")
    else:
        print("Geen stukken van de relevante kleur gevonden, controleer beeldherkenning indien je fysiek wel een zet hebt uitgevoerd.")

def write_relevant_pieces_before_move_to_file () :
    path_relevant_pieces_before_move=r".\bord_gomoku\bord_voor_zet.json"
    write_relevant_pieces_to_file(path_relevant_pieces_before_move)

def write_relevant_pieces_after_move_to_file () :
    path_relevant_pieces_after_move=r".\bord_gomoku\bord_na_zet.json"
    write_relevant_pieces_to_file(path_relevant_pieces_after_move)


def read_detected_pieces() -> Dict[str, Any]:
    file_path = r'..\vijf_op_een_rij_beeldherkenning\detected_pieces.json'
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except PermissionError:
        print("Please close the file and try again")
        return {}



