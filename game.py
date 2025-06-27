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
import random

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

        self.last_accel_x, self.last_accel_y, self.last_accel_z = self.lis3dh.acceleration

        # --- Create our view classes/objects ---
        self.graphics_manager = GraphicsManager()

        self.active_tetromino_view = TetrominoView(
            sprite_sheet_bitmap=self.graphics_manager.sprite_sheet_bitmap,
            sprite_sheet_palette=self.graphics_manager.sprite_sheet_palette,
            root_group=self.graphics_manager.root_group,
        )
        self.sand_pile_view = SandPileView(
            sprite_sheet_palette=self.graphics_manager.sprite_sheet_palette,
            root_group=self.graphics_manager.root_group,
        )

        # --- Create our models classes/objects ---
        self.active_tetromino = Tetromino(self._get_random_shape(), self._get_random_color())
        self.sand_pile = SandPile(self.sand_pile_view.sand_state_bitmap)

        self.next_shape = self._get_random_shape()
        self.next_color = self._get_random_color()

        # -- Create variables related with the game-loop
        self.last_frame_time = time.monotonic()
        self.is_game_over = False

        self.num_tetrominoes_dropped = 0

    # --- Methods ---

    def _get_random_shape(self):
        return random.choice(constants.SHAPE_TYPE_POPULATION)

    def _get_random_color(self):
        return random.choice(constants.COLOR_TYPE_POPULATION_WEIGHTED)

    def _get_all_inputs(self):
        """
        Gathers all player inputs from the accelerometer for the current frame.

        Returns:
            dict: A dictionary containing the state of all inputs, e.g.,
                  {'shaken': bool, 'tapped': bool, 'tilt_angle': float}
        """
        was_tapped = False # Default value
        was_shaken = False # Default value

        try:
            # Get the current raw acceleration values
            ax, ay, az = self.lis3dh.acceleration

            # --- NEW: Non-Blocking Shake Detection ---
            # Calculate the change (delta) in acceleration since the last frame
            delta_x = ax - self.last_accel_x
            delta_y = ay - self.last_accel_y
            delta_z = az - self.last_accel_z

            # Update the stored values for the next frame
            self.last_accel_x, self.last_accel_y, self.last_accel_z = ax, ay, az

            # Calculate the magnitude of the change. This is the "jerk".
            jerk_magnitude = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

            # Compare the jerk to a threshold. You will need to tune this value
            # in your constants.py file. Start with a value around 25-30.
            if jerk_magnitude > constants.SHAKE_THRESHOLD:
                was_shaken = True

            # --- Tap Detection ---
            was_tapped = self.lis3dh.tapped

            # --- Tilt Angle ---
            angle_rad = math.atan2(-ay, ax)
            angle_deg = math.degrees(angle_rad)

        except OSError:
            # If I2C fails, return neutral inputs
            return {"shaken": False, "tapped": False, "tilt_angle": 0.0}

        # Return all inputs in a clean dictionary
        return {
            "shaken": was_shaken,
            "tapped": was_tapped,
            "tilt_angle": angle_deg
        }

    def _is_tetromino_collision(self, proposed_x: int, proposed_y: int):
        """
        Helper method for _update_all_models method.
        returns whether a tetromino is colliding.

        Checks whether the active Tetromino at the proposed new position would collide
        with the ground or existing sand. This does not check if it hits the wall.

        Args:
            proposed_x (int): The proposed new x-coordinate for the active tetromino.
            proposed_y (int): The proposed new y-coordinate for the active tetromino.
        """

        # Get the vertical space that is empty in the tetromino's shape
        bottom_padding = self.active_tetromino.get_bottom_padding()

        # Calculate the total height of the tetromino shape in pixels
        shape_total_height = constants.TETROMINO_SHAPE_DATA_SIZE * constants.MINO_SIZE
        bottom_edge_position = proposed_y + (shape_total_height - 1) - bottom_padding

        if bottom_edge_position >= constants.GAME_HEIGHT:
            return True

        # TODO: Check sand collision here

        return False

    def _tetromino_hits_wall(self, proposed_x: int) -> bool:
        """
        Determines whether the active tetromino would collide with the left or right wall
        of the game board at the proposed horizontal position.

        Args:
            proposed_x (int): The proposed new x-coordinate for the active tetromino.

        Returns:
            bool: True if the tetromino would collide with the wall, False otherwise.
        """

        # Get the amount of horizontal space on the left and right that is empty in the tetromino's shape
        left_padding = self.active_tetromino.get_left_padding()
        right_padding = self.active_tetromino.get_right_padding()

        # Calculate the total width of the tetromino shape in pixels
        shape_total_width = constants.TETROMINO_SHAPE_DATA_SIZE * constants.MINO_SIZE

        # Calculate the far left and far right boundaries of the tetromino at the proposed position
        left_edge_position = proposed_x + left_padding
        right_edge_position = proposed_x + (shape_total_width - 1) - right_padding

        # Determine whether the tetromino goes beyond the left or right wall
        hits_left_wall = left_edge_position < 0
        hits_right_wall = right_edge_position >= constants.GAME_WIDTH

        return hits_left_wall or hits_right_wall

    def _handle_rotations(self):
        original_orientation = self.active_tetromino.orientation
        original_x = self.active_tetromino.x
        original_y = self.active_tetromino.y

        self.active_tetromino.rotate()

        if self._is_tetromino_collision(original_x, original_y):
            self.active_tetromino.set_orientation(original_orientation)

        elif self._tetromino_hits_wall(original_x):
            shift_found = False

            for shift in range(1, constants.MAX_SHIFTS + 1):
                self.active_tetromino.x = original_x - shift
                if not self._tetromino_hits_wall(self.active_tetromino.x):
                    shift_found = True
                    break

                self.active_tetromino.x = original_x + shift
                if not self._tetromino_hits_wall(self.active_tetromino.x):
                    shift_found = True
                    break

            if not shift_found:
                self.active_tetromino.set_orientation(original_orientation)
                self.active_tetromino.x = original_x

    def _update_all_models(self, dt: float, inputs):

        if inputs["tapped"]:
            self._handle_rotations()

        old_x = self.active_tetromino.x
        old_y = self.active_tetromino.y
        new_x, new_y = self.active_tetromino.get_next_position(dt, inputs["tilt_angle"])

        colliding = self._is_tetromino_collision(new_x, new_y)
        hits_wall = self._tetromino_hits_wall(new_x)


        if colliding:

            new_y = 0
            new_x = constants.TETROMINO_START_X

            self.sand_pile.convert_tetromino_to_sand(self.active_tetromino, self.graphics_manager.sprite_sheet_bitmap)
            self.active_tetromino.decrement_fall_rate()

            self.active_tetromino.set_shape_type(self.next_shape)
            self.active_tetromino.set_color_type(self.next_color)

            self.next_shape = self._get_random_shape()

            if random.random() < constants.NEXT_COLOR_CHANCE:
                self.next_color = self._get_random_color()

            self.num_tetrominoes_dropped += 1

        elif hits_wall:
            new_x = old_x

        self.active_tetromino.execute_approved_move(new_x, new_y)

    def _update_all_views(self):
        self.graphics_manager.begin_frame()

        self.active_tetromino_view.update(
            self.active_tetromino.get_shape_data(),
            self.active_tetromino.color_type,
            self.active_tetromino.x,
            self.active_tetromino.y,
        )

        self.graphics_manager.end_frame()

    def start_game_loop(self):
        while not self.is_game_over:
            start_frame_time = time.monotonic()
            dt = start_frame_time - self.last_frame_time
            self.last_frame_time = start_frame_time

            inputs = self._get_all_inputs()
            self._update_all_models(dt, inputs)
            self._update_all_views()

            frame_time = time.monotonic() - start_frame_time
            sleep_time = constants.TICK_RATE - frame_time

            if sleep_time > 0:
                time.sleep(sleep_time)

        while True:
            pass
