from . import replay_controller

# controller.py
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.replay_controller = replay_controller.ReplayController(view)

    def initialize_replay(self, file_name):
        self.replay_controller.load_game(file_name)
        
        