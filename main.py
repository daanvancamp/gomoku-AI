
from datetime import datetime
import os
from threading import Thread
from filereader import log_info_overruling
import mainmenu
from lezen_stukken_en_muziek import initialiseer_muziek

def main():
    mainmenu.mainmenu_run()
    
def controleer_bestandspaden():
    #glob.glob searches file in directory
    pad_gedetecteerde_stukken=r'..\vijf_op_een_rij_beeldherkenning\detected_pieces.json'

    #paden=[r".\bord_gomoku\bord_na_zet.json",r".\bord_gomoku\bord_voor_zet.json", pad_gedetecteerde_stukken,"bool_overrule.txt","consts.json","wachten_muziek.mp3","logging_overruling.txt"]
    #for bestandspad in paden:
    #    if not os.path.exists(bestandspad):
    #        raise Exception("The file doesn't exist",bestandspad)
    print("even verwijderd")

def log_new_run():
    log_info_overruling("\n\n\n\n\n\ndate and time: "+datetime.now().isoformat())
    log_info_overruling("\nnew run of the code begins:")

if __name__ == '__main__':
    log_new_run()
    controleer_bestandspaden()
    initialiseer_muziek()
    main()
