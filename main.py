from datetime import datetime
import os
from threading import Thread
from filereader import log_info_overruling
import mainmenu
from music import initialiseer_muziek

#todo: make the error messages more clear, sometimes they are wrong, search "raise Exception"
#todo: add a label to the main menu to show the number of training loops instead of just a number
#todo: move the reset stats en reset end stats button to the bottom center
#todo: delete the get_player_type and set_player_type functions
#todo: add padding to the main menu
def main():
    mainmenu.mainmenu_run()
    
def check_paths():
    #glob.glob searches file in directory
    pad_gedetecteerde_stukken=r'..\vijf_op_een_rij_beeldherkenning\detected_pieces.json'

    #paden=[r".\bord_gomoku\bord_na_zet.json",r".\bord_gomoku\bord_voor_zet.json", pad_gedetecteerde_stukken,"consts.json","wachten_muziek.mp3","logging_overruling.txt"]
    #for bestandspad in paden:
    #    if not os.path.exists(bestandspad):
    #        raise Exception("The file doesn't exist",bestandspad)
    #temporarily disabled, will be implemented in the future
def start_recognition():
    pass

def log_new_run():
    log_info_overruling("\n\n\n\n\ndate and time: "+datetime.now().isoformat())
    log_info_overruling("\nnew run of the code begins:")

if __name__ == '__main__':
    log_new_run()
    check_paths()
    initialiseer_muziek()
    main()
