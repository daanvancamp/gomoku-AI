import pygame
from time import sleep


path_wachten_muziek=r".\wait_music.mp3"

def initialiseer_muziek():
    # Initialiseer pygame mixer
    pygame.mixer.init(buffer=100000,allowedchanges=0) #voorkom haperingen
    pygame.mixer.music.load(path_wachten_muziek)#add to memory

def start_music_delayed(delay=1):
    sleep(delay) #blokkeert enkel thread
    try:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.play()
    except:
        try:
            pygame.mixer.music.load(path_wachten_muziek)
            pygame.mixer.music.fadeout(1000)

            pygame.mixer.music.play()
        except:
            pass