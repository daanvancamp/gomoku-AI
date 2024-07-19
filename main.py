
import os
from threading import Thread
import mainmenu
from lezen_stukken_en_trivia import initialiseer_muziek
from GUI_timer import initialiseer_timer

def main():
    mainmenu.mainmenu_run()

def controleer_bestandspaden():
    paden=[r".\bord_gomoku\bord_na_zet.json",r".\bord_gomoku\bord_voor_zet.json",r"C:\Users\daanv\source\repos\vijf_op_een_rij_beeldherkenning\vijf_op_een_rij_beeldherkenning\detected_pieces.json"]
    for bestandspad in paden:
        if not os.path.exists(bestandspad):
            print("Het JSON-bestand bestaat niet. Maak het aan en probeer het opnieuw.")
            raise Exception("JSON-bestand bestaat niet, los het op door het programma dat leest van de webcam te runnen, of pas het pad in het programma aan.",bestandspad)


if __name__ == '__main__':
    #thread_GUI_timer=Thread(target=initialiseer_timer,daemon=True)
    #thread_GUI_timer.start()
    #bevat bugs voorlopig
    initialiseer_timer()
    controleer_bestandspaden()
    initialiseer_muziek()
    main()
