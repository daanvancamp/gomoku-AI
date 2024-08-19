import json
import datetime
import os

def empty_file(filename):
    try:
        with open(filename, 'w') as file:
            file.write("")
    except PermissionError:
        print("Please close the file and try again")


def log_info_overruling(message):
    path_logging_overruling=r".\logs\logging_overruling.txt"
    try:
        with open(path_logging_overruling, "a") as file:
            file.write(message+"\n") #newline
    except PermissionError:
        print("Please close the file and try again")
        
def create_gomoku_game(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            gomoku_config = data.get("gomoku", [])[0]
            values = []
            for key, value in gomoku_config.items():
                if type(value) is str:
                    value = string_to_color(value)
                values.append(value)
            return values
    except PermissionError:
        print("Please close the file and try again")

def load_scores(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file).get("scores", [])
    except PermissionError:
        print("Please close the file and try again")

def load(filename):
    try:
        return json.load(filename)
    except PermissionError:
        print("Please close the file and try again")

def string_to_color(in_col):
    # Remove parentheses
    new_col = in_col.replace('(', '')
    new_col = new_col.replace(')', '')
    # Split the string into individual RGB values
    rgb = new_col.split(', ')
    return int(rgb[0]), int(rgb[1]), int(rgb[2])

def save_replay(p1, p2):
    remove_last = False
    if len(p2) < len(p1):
        p2.append((-1, -1))
        remove_last = True
    all_moves = []
    for p1_move, p2_move in zip(p1, p2):
        all_moves.append(('1', p1_move))
        all_moves.append(('2', p2_move))
    if remove_last:
        all_moves.pop()
    moves_sequence = {"moves": []}
    for index, (player, move) in enumerate(all_moves, start=1):
        moves_sequence["moves"].append({
            "player": player,
            "position": str(tuple(move))
        })
    outfile = f"data/replays/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    try:
        with open(outfile, "w") as of:
            json.dump(moves_sequence, of, indent=4)
    except PermissionError:
        print("Please close the file and try again")

def load_replay(file):
    try:
        with open(file, 'r') as j:
            moves_data = json.loads(j.read())
        moves = {}
        for move in moves_data["moves"]:
            player = int(move["player"])
            position = tuple(map(int, move["position"].strip("()").split(", ")))
            moves[position] = player
        return moves
    except (KeyError, json.decoder.JSONDecodeError):
        print("Error loading replay file.")
    except PermissionError:
        print("Please close the file and try again")
    except:
        print("no such file or directory exists, try again, choose a correct json file")
    return None
