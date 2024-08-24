import pygame
from time import sleep


path_wachten_muziek=r".\wait_music.mp3"

def initialiseer_muziek():
    # Initialiseer pygame mixer
    pygame.mixer.init(buffer=100000,allowedchanges=0) #voorkom haperingen
    pygame.mixer.music.load(path_wachten_muziek)#add to memory

def start_music_delayed(tijd=1):
    sleep(tijd) #blokkeert enkel thread
    try:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.play()
    except:
        try:
            pygame.mixer.music.load(path_wachten_muziek)#tijdelijk #todo: werk weg door initialiseer_muziek te verbeteren of een andere wijziging toe te passen
            pygame.mixer.music.fadeout(1000)

            pygame.mixer.music.play()
        except:
            raise Exception("Fout bij het starten van de muziek. Controleer of het bestand wel bestaat en niet geopend is in een ander programma.")