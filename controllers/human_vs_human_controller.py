import game.game
import ui.main_window
from .basecontrollers import controller
from configuration.config import *

class Human_vs_HumanController(controller.BaseController):
    def __init__(self, view: "ui.main_window.GomokuApp"):
        super().__init__(view)
        self.set_up_game(("Human", "Human"))

        self.view.window_mode = ui.main_window.WindowMode.human_move


    def human_put_piece(self, row, col):
        self.game.put_piece(row, col)
        self.view.draw_pieces(self.game.board.board)
        self.check_and_handle_winner()
