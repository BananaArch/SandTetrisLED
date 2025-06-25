# game.py

from graphics_manager import GraphicsManager
from tetromino_view import TetrominoView
from sand_pile_view import SandPileView
from tetromino import Tetromino
from sand_pile import SandPile
import constants

import adafruit_lis3dh

import board
import busio
import math
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

        # --- Initialize hardware ---

        i2c = busio.I2C(board.SCL, board.SDA)  # Setup I2C for the accelerometer
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=constants.MATRIX_PORTAL_LIS3DH_ADDRESS)  # Creates accelerometer object
        self.lis3dh.range = adafruit_lis3dh.RANGE_2_G  # Sets a range of 2G for sensitivity
        self.lis3dh.set_tap(1, constants.TAP_THRESHOLD) # 1 sets single tap

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

        # --- Create our models classes/objects ---
        self.active_tetromino = Tetromino(constants.ShapeType.T, constants.ColorType.YELLOW)
        self.sand_pile = SandPile(self.sand_pile_view.sand_state_bitmap)

        # -- Create variables related with the game-loop
        self.last_frame_time = time.monotonic()
        self.is_game_over = False



    def _get_all_inputs(self):
        """
        Gathers all player inputs from the accelerometer for the current frame.

        Returns:
            dict: A dictionary containing the state of all inputs, e.g.,
                  {'shaken': bool, 'tapped': bool, 'tilt_angle': float}
        """

        # --- Shake ---
        # The .shake() method returns True if the acceleration exceeds a threshold.
        was_shaken = self.lis3dh.shake(shake_threshold=constants.SHAKE_THRESHOLD)

        # --- Double Tap ---
        # The .tapped property is True for one frame after a tap is detected,
        # then it resets to False automatically.
        was_tapped = self.lis3dh.tapped

        # --- Tilt Angle ---
        # Get the raw x, y, z acceleration values.
        try:
            ax, ay, az = self.lis3dh.acceleration
        except OSError:
            # Sometimes I2C can fail, return a neutral angle
            return {"shaken": False, "tapped": False, "tilt_angle": 0.0}

        # Calculate the angle in radians using atan2.
        # We use -ay and ax. The specific axes might need to be tweaked
        # depending on your board's physical orientation.
        angle_rad = math.atan2(-ay, ax)

        # Convert radians to degrees for easier use.
        angle_deg = math.degrees(angle_rad)

        # Return all inputs in a clean dictionary
        return {
            "shaken": was_shaken,
            "tapped": was_tapped,
            "tilt_angle": angle_deg
        }

    def _is_tetromino_collision(self):
        """
        Helper method for _update_all_models method.
        returns whether a tetromino is colliding
        """
        pass

    def _update_all_models(self, dt: float, inputs):
        """ Helper method for game loop. We must update all models: Tetromino, SandPile, etc. before we can update the Views. """

        # --- UPDATE TETROMINO MODEL FIRST ---

        if (inputs["tapped"]):
            self.active_tetromino.rotate()

        proposed_tetromino_coords = self.active_tetromino.get_next_position(dt, inputs["tilt_angle"])

        new_x = proposed_tetromino_coords[0]
        new_y = proposed_tetromino_coords[1]

        if new_y > constants.GAME_HEIGHT - 6:
            new_y = 0
            self.active_tetromino.decrement_fall_rate()

        if new_x < 0:
            new_x = 0
        elif new_x > constants.GAME_WIDTH:
            new_x = constants.GAME_WIDTH

        self.active_tetromino.execute_approved_move(new_x, new_y)
        pass

        # --- UPDATE SAND MODEL ---

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

    def start_game_loop(self):
        """ This is the actual game loop which causes the game to happen. """

        # Game Logic
        while not self.is_game_over:

            # Step 1: Calculate the time since the last frame.
            # This will be passed into every model's update method.

            start_frame_time = time.monotonic()
            dt = start_frame_time - self.last_frame_time
            self.last_frame_time = start_frame_time

            # Step 2: Read all inputs.
            # We must do this before updating the models.

            inputs = self._get_all_inputs()
            print(inputs)

            # Step 3: Update all Models.
            # We must do this before rendering anything.

            self._update_all_models(dt, inputs)

            # Step 4: Update all Graphics (Views).

            self._update_all_views()

            # Step 5: Wait until next tick.

            frame_time = time.monotonic() - start_frame_time  # elapsed frame time
            sleep_time = constants.TICK_RATE - frame_time

            if sleep_time > 0:
                time.sleep(sleep_time)

        # Game Over Logic
        while True:
            pass
