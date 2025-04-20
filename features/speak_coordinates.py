import pyttsx3

def speak_coordinates(x, y,player_type):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate * 0.7)
    message = f"{player_type} row {x + 1}, column {y + 1}."

    engine.say(message)
    engine.runAndWait()