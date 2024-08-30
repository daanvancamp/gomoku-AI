# controller.py
class BaseController:
    def __init__(self, view):
        self.view = view
        self.view.controller = self


        
