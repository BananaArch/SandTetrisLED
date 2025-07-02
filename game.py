# game.py

from inputs_manager import InputsManager
from graphics_manager import GraphicsManager
from tetromino_view import TetrominoView
from sand_pile_view import SandPileView
from tetromino import Tetromino
from sand_pile import SandPile
import constants

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

        # --- Create our InputsManager sub-controller class/object ---
        self.inputs_manager = InputsManager()

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
        self.time_since_tapped = 0.0

        self.num_tetrominoes_dropped = 0



    # --- Methods ---



    def _get_random_shape(self):
        return random.choice(constants.SHAPE_TYPE_POPULATION)

    def _get_random_color(self):
        return random.choice(constants.COLOR_TYPE_POPULATION_WEIGHTED)



    def _is_tetromino_collision(self, proposed_x: int, proposed_y: int):
        """
        Helper method for _update_all_models method.
        returns whether a tetromino is colliding.

        Checks whether the active Tetromino at the proposed new position would collide
        with the ground or existing sand. This does not check if it hits the wall.
        The _tetromino_hits_wall method deals witht his.

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

        # iterate through 4x4 grid of minos

        shape_data = self.active_tetromino.get_shape_data()

        for index, mino_value in enumerate(shape_data):

            if mino_value == 0:  # there is no mino there
                continue  # we skip it

            shape_x = index % constants.TETROMINO_SHAPE_DATA_SIZE  # gets the 2D x coordinate of the 1D shape_data
            shape_y = index // constants.TETROMINO_SHAPE_DATA_SIZE  # gets the 2D y coordinate of the 1D shape_data

            # if there is a mino there, iterate through all pixels of that mino
            for x_offset in range(constants.MINO_SIZE):
                for y_offset in range(constants.MINO_SIZE):

                    absolute_pixel_x = proposed_x + shape_x * constants.MINO_SIZE + x_offset
                    absolute_pixel_y = proposed_y + shape_y * constants.MINO_SIZE + y_offset

                    sand_bitmap_x = absolute_pixel_x
                    sand_bitmap_y = absolute_pixel_y - constants.INFO_BAR_HEIGHT

                    if (not self.sand_pile.is_empty_at((sand_bitmap_x, sand_bitmap_y))):
                        return True

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

        # --- Tetromino Updates ---

        if inputs["tapped"] and self.time_since_tapped > constants.TAP_COOLDOWN:
            self._handle_rotations()
            self.time_since_tapped = 0.0

        old_x = self.active_tetromino.x
        old_y = self.active_tetromino.y
        new_x, new_y = self.active_tetromino.get_next_position(dt, inputs["tilt_angle"])

        colliding = self._is_tetromino_collision(new_x, new_y)
        hits_wall = self._tetromino_hits_wall(new_x)


        if colliding:

            self.sand_pile.convert_tetromino_to_sand(self.active_tetromino, self.graphics_manager.sprite_sheet_bitmap)

            if (self.num_tetrominoes_dropped != 0 and self.num_tetrominoes_dropped % constants.TETROMINO_FALLEN_NEXT_LEVEL == 0):
                self.active_tetromino.decrement_fall_rate()

            self.active_tetromino.reset(self.next_shape, self.next_color)

            self.next_shape = self._get_random_shape()

            if random.random() < constants.NEXT_COLOR_CHANCE:
                self.next_color = self._get_random_color()

            self.num_tetrominoes_dropped += 1
            return

        elif hits_wall:
            new_x = old_x

        self.active_tetromino.execute_approved_move(new_x, new_y)

        # --- SandPile Update ---

        self.sand_pile.update()

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

            inputs = self.inputs_manager.get_all_inputs()
            self._update_all_models(dt, inputs)
            self._update_all_views()

            self.time_since_tapped += dt

            frame_time = time.monotonic() - start_frame_time
            sleep_time = constants.TICK_RATE - frame_time

            if sleep_time > 0:
                time.sleep(sleep_time)

            print(sleep_time)
        while True:
            pass
