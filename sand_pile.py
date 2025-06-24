# sand_pile.py

import displayio
from tetromino import Tetromino

class SandPile:
    """
    This is a model class that manages the logic of the playfield (sandpile).
    It's responsible for managing the state of the settled sand, implementing gravity logic, and the collision methods.
    Unfortunately, this class does not reflect the pure MVC structure because the model has access to a bitmap from the view.
    This is because of pragmatic reasons. We only have 192KB of RAM, and if we were to create another 2D array to represent the field,
        it will cost us 59 (Game Area Height) * 32 (Game Area Width) * 4 (bytes per int) = 7552 bytes which is around 4% of our
        available RAM.
    Instead, we are going to use the bitmap as the single source of truth.
    """

    def __init__(self, sand_bitmap: displayio.Bitmap):
        """
        Initializes SandPile class.

        Args:
            bitmap_to_manage (displayio.Bitmap): The bitmap object that the class receives from the GraphicsManager is the
            single data source for all of its logic. Otherwise, we would have had to create another 2D array with
            MATRIX WIDTH * MATRIX HEIGHT values which is extremely expensive. It is a pragmatic decision to let the SandPile
            model have access to the view.

        """

        self.sand_state_bitmap = sand_bitmap
        pass

    def is_collision(self, tetromino: Tetromino, dx=0, dy=0):
        """
        Checks if a given Tetromino at a proposed new position would collide
        with the grid boundaries or existing sand.

        Args:
            tetromino (Tetromino): The tetromino object to check.
            dx (int, optional): The proposed change in x. Default: 0
            dy (int, optional): The proposed change in y. Default: 0
        """

        pass

    def convert_tetromino_to_sand(self, tetromino: Tetromino):
        """
        Converts the given Tetromino to sand.

        Args:
            tetromino (Tetromino): The tetromino object to convert to snd.
        """

        pass

    def apply_sand_physics(self):
        """
        Iterates through the SandPile and makes any unsupported sand pixels fall down.
        """

        pass

    def find_and_clear_lines(self):
        """
        Finds any continuous paths of same-colored sand from left to right.
        If found, clears them and returns the number of points scored.
        Returns the number of cleared sand pixels.
        """
        pass

