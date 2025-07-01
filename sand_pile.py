# sand_pile.py

import displayio

from tetromino import Tetromino
import constants

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

    def contains_sand_at(self, x: int, y: int):

        # Check if out of bounds
        if (x < 0 or x >= constants.GAME_WIDTH) or (y < 0 or y >= constants.PLAYFIELD_HEIGHT):
            return False

        # Return if that pixel position is not a 0, which is our transparent index
        return self.sand_state_bitmap[x, y] != 0

    def convert_tetromino_to_sand(self, tetromino: Tetromino, sprite_sheet_bitmap: displayio.Bitmap):
        """
        Converts the given Tetromino to sand. This method has access to sprite_sheet_bitmap (a view) because it's a
        pragmatic decision based on the fact that our main 2D array is a bitmap (view).

        Args:
            tetromino (Tetromino): The tetromino object to convert to sand.
            sprite_sheet_bitmap
            sprite_sheet_bitmap (displayio.Bitmap): The spritesheet bitmap
            that contains all sprites for minos. This is used to stamp
            the colors and palettes into the sand_bitmap.
        """

        shape_data = tetromino.get_shape_data()

        # Loop through each of the 16 slots in the 4x4 shape data grid.
        # `i` will be the index from 0-15.
        # `tile_col_index` is the value from the bytearray (the sprite's column).
        for index, tile_col_index in enumerate(shape_data):

            # If the value is 0, it's an empty part of the shape, so we skip it.
            if tile_col_index == 0:
                continue

            # --- Step 1: Calculate the destination position ---
            # First, find the logical (x,y) of this mino within the 4x4 piece grid.
            mino_grid_x = index % constants.TETROMINO_SHAPE_DATA_SIZE
            mino_grid_y = index // constants.TETROMINO_SHAPE_DATA_SIZE

            # Now, find the top-left *pixel* coordinate where this mino should be stamped
            # onto the sand bitmap.
            dest_start_x = tetromino.x + mino_grid_x * constants.MINO_SIZE
            dest_start_y = tetromino.y + mino_grid_y * constants.MINO_SIZE

            # --- Step 2: Calculate the source position ---
            # Find the top-left *pixel* coordinate of the source sprite on the sprite sheet.
            source_start_x = tile_col_index * constants.MINO_SIZE
            source_start_y = tetromino.color_type * constants.MINO_SIZE

            # --- Step 3: Copy the 3x3 pixels ---
            # Now we loop 3x3 times to copy the mino's pixels.
            for x_offset in range(constants.MINO_SIZE):
                for y_offset in range(constants.MINO_SIZE):

                    # Calculate the final source pixel to read from
                    source_x = source_start_x + x_offset
                    source_y = source_start_y + y_offset

                    # Calculate the final destination pixel to write to
                    dest_x = dest_start_x + x_offset
                    dest_y = dest_start_y + y_offset - constants.INFO_BAR_HEIGHT
                    # the INFO_BAR_HEIGHT accounts for the fact that the playfield area is 5 px below y=0

                    # Safety check to ensure we don't write out of bounds
                    if (0 <= dest_x < self.sand_state_bitmap.width and
                        0 <= dest_y < self.sand_state_bitmap.height):

                        # Copy the pixel's index value from the sprite sheet
                        # to the sand pile's state bitmap.
                        pixel_value = sprite_sheet_bitmap[source_x, source_y]

                        self.sand_state_bitmap[dest_x, dest_y] = pixel_value

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

