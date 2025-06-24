# game.py

from graphics_manager import GraphicsManager
from tetromino import Tetromino
from sand_pile import SandPile
import constants

import time


class Game:
    """
    This class is a controller. It initializes the game and runs the main game loop.
    It authorizes decisions to the model.
    """

    def __init__(self):
        """
        Creates the Game object.
        This constructor then creates a
            Graphics Manager,
            SandPile,
            and the Active Tetromino.
        """
        self.graphics_manager = GraphicsManager()
        self.active_tetromino = Tetromino(constants.ShapeType.S, constants.ColorType.YELLOW)
        self.graphics_manager.create_tetromino_tile_grid_and_group(self.active_tetromino)

    def start_game_loop(self):
        """ This is the actual game loop which causes the game to happen. """
        while True:


            self.graphics_manager.update_display(self.active_tetromino)
            time.sleep(constants.GAME_LOOP_DELAY)
