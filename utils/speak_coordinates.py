import pyttsx3

def speak_coordinates(x, y):
    engine = pyttsx3.init()
    message = f"move at row {x + 1}, column {y + 1}."

    engine.say(message)
    engine.runAndWait()