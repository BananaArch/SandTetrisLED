# game.py

from graphics_manager import GraphicsManager
from tetromino_view import TetrominoView
from sand_pile_view import SandPileView
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

        # --- Create our view classes/objects ---
        self.graphics_manager = GraphicsManager()
        self.active_tetromino_view = TetrominoView(
            sprite_sheet_bitmap = self.graphics_manager.sprite_sheet_bitmap,
            sprite_sheet_palette = self.graphics_manager.sprite_sheet_palette,
            root_group = self.graphics_manager.root_group,
        )
        self.sand_pile_view = SandPileView(
            sprite_sheet_palette = self.graphics_manager.sprite_sheet_palette,
            root_group = self.graphics_manager.root_group,
        )

        # Create our models
        self.active_tetromino = Tetromino(constants.ShapeType.T, constants.ColorType.YELLOW)

        self.last_frame_time = time.monotonic()

    def start_game_loop(self):
        """ This is the actual game loop which causes the game to happen. """
        while True:

            # Step 1: Calculate the time since the last frame.
            # This will be passed into every model's update method.

            start_frame_time = time.monotonic()
            dt = start_frame_time - self.last_frame_time
            self.last_frame_time = start_frame_time

            # Step 2: Update all Models.
            # We must do this before rendering anything.

            self._update_all_models(dt)

            # Step 3: Update all Graphics (Views).

            self._update_all_views()

            # Step 4: Wait until next tick.

            frame_time = time.monotonic() - start_frame_time  # elapsed frame time
            sleep_time = constants.TICK_RATE - frame_time

            if sleep_time > 0:
                time.sleep(sleep_time)

    def _update_all_models(self, dt: float):
        """ Helper method for game loop. We must update all models: Tetromino, SandPile, etc. before we can update the Views. """
        proposed_tetromino_coords = self.active_tetromino.get_next_position(dt, 0)
        new_x = proposed_tetromino_coords[0]
        new_y = proposed_tetromino_coords[1]

        if new_y > constants.GAME_HEIGHT - 12:
            new_y = constants.GAME_HEIGHT - 12
        self.active_tetromino.execute_approved_move(new_x, new_y)
        pass

    def _update_all_views(self):
        """ Helper method to render everything, and update all the view classes: TetrominoView, SandPileView, etc. """

        self.graphics_manager.begin_frame()  # Tells the graphics manager to pause refereshes

        # Update Tetromino View First
        # Notice we do not pass in Tetromino because that would break
        #   the MVC architecture. The view cannot talk to the model.
        self.active_tetromino_view.update(
            self.active_tetromino.get_shape_data(),
            self.active_tetromino.color_type,
            self.active_tetromino.x,
            self.active_tetromino.y,
        )

        self.graphics_manager.end_frame() # Tells the graphics manager: we're done... time to show the result
