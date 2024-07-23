
import os
from threading import Thread
import mainmenu
from lezen_stukken_en_trivia import initialiseer_muziek

def main():
    mainmenu.mainmenu_run()
def controleer_bestandspaden():
    paden=[r".\bord_gomoku\bord_na_zet.json",r".\bord_gomoku\bord_voor_zet.json",r"..\vijf_op_een_rij_beeldherkenning\vijf_op_een_rij_beeldherkenning\detected_pieces.json","bool_overrule.txt","consts.json","wachten_muziek.mp3","logging_overruling.txt"]
    for bestandspad in paden:
        if not os.path.exists(bestandspad):
            raise Exception("The file doesn't exist",bestandspad)

if __name__ == '__main__':
    controleer_bestandspaden()
    initialiseer_muziek()
    main()
