import pyttsx3

def speak_coordinates(x, y,player_type):
    engine = pyttsx3.init()
    message = f"{player_type} put piece on row {x + 1}, column {y + 1}."

    engine.say(message)
    engine.runAndWait()