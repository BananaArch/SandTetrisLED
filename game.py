# game.py

from graphics_manager import GraphicsManager
from tetromino_view import TetrominoView
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

        # Create our view classes/objects
        self.graphics_manager = GraphicsManager()
        self.active_tetromino_view = TetrominoView(
            self.graphics_manager.sprite_sheet_bitmap,
            self.graphics_manager.sprite_sheet_palette,
            self.graphics_manager.root_group
        )

        # Create our models
        self.active_tetromino = Tetromino(constants.ShapeType.T, constants.ColorType.GREEN)

    def start_game_loop(self):
        """ This is the actual game loop which causes the game to happen. """
        while True:

            # Step 1: Update all Models.
            # We must do this before rendering anything.

            self._update_all_models()

            # Step 2: Update all Graphics (Views).

            self._update_all_views()

            # Step 3: Wait until next tick.

            time.sleep(constants.GAME_LOOP_DELAY)

    def _update_all_models(self):
        """ Helper method for game loop. We must update all models: Tetromino, SandPile, etc. before we can update the Views. """

        pass

    def _update_all_views(self):
        """ Helper method to render everything, and update all the view classes: TetrominoView, SandPileView, etc. """

        self.graphics_manager.begin_frame()  # Tells the graphics manager to pause refereshes

        # Update Tetromino View First
        # Notice we do not pass in Tetromino because that would break
        #   the MVC architecture. The view cannot talk to the model.
        self.active_tetromino_view.update(
            self.active_tetromino.shape_data,
            self.active_tetromino.color_type,
            self.active_tetromino.x,
            self.active_tetromino.y,
        )

        self.graphics_manager.end_frame() # Tells the graphics manager: we're done... time to show the result
