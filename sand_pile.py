# sand_pile.py

import displayio
import random

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
        self.dirty_rects = []
        # Each rectangle will be a tuple with (x, y, width, height).
        # The x and y represents the coordinate of the top-left of the rectangle.

    def _coord_within_bounds(self, coord: Tuple[int, int]):
        x, y = coord

        x_in_bounds = (0 <= x < constants.GAME_WIDTH)
        y_in_bounds = (0 <= y < constants.PLAYFIELD_HEIGHT)

        return x_in_bounds and y_in_bounds

    def is_empty_at(self, coord: Tuple[int, int]):
        """
        Returns whether (x, y) is empty

        If it's out-of-bounds, we return True
        """

        if (not self._coord_within_bounds(coord)):  # if out of bounds, we say it is empty
            return True

        x, y = coord

        # Returns if pixel position is 0, which is our transparent index
        return self.sand_state_bitmap[x, y] == 0

    def _rects_overlap(self, rect1 : Tuple[int, int, int, int], rect2 : Tuple[int, int, int, int]):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2

        # Check if rect2 is to the right or left of rect1
        if (x1 + w1 < x2 or x2 + w2 < x1):
            return False

        # Check if rect2 is above or below rect1
        if (y1 + h1 < y2 or y2 + h2 < y1):
            return False

        # Otherwise, they do overlap
        return True

    def _get_rects_union(self, rect1 : Tuple[int, int, int, int], rect2 : Tuple[int, int, int, int]):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2

        # Get the top-left coordinates for the union rectangle
        union_x = min(x1, x2)
        union_y = min(y1, y2)

        # Get the bottom-right coordinates for the union rectangle
        union_right_x = max(x1 + w1, x2 + w2)
        union_bot_y = max(y1 + h1, y2 + h2)

        union_width = union_right_x - union_x
        union_height = union_bot_y - union_y

        return (union_x, union_y, union_width, union_height)

    def _merge_overlapping_rects(self):

        if (len(self.dirty_rects) == 0):
            return

        merged_rects = self.dirty_rects.copy()

        while True:
            merge_happened = False

            i = 0
            while i < len(merged_rects):

                j = i + 1
                while j < len(merged_rects):

                    rect1 = merged_rects[i]
                    rect2 = merged_rects[j]

                    if not self._rects_overlap(rect1, rect2):
                        j += 1  # We increment j to check for the next rect if they don't overlap.
                        continue  # We don't have to worry about merging.

                    union_rect = self._get_rects_union(rect1, rect2)
                    merged_rects[i] = union_rect
                    del merged_rects[j]

                    merge_happened = True
                    break

                if merge_happened:
                    break

                i += 1

            if not merge_happened:
                break

        self.dirty_rects = merged_rects
        print(merged_rects)

    def dirty_the_area(self, x: int, y: int, width: int, height: int):
        self.dirty_rects.append((x, y, width, height))

    def _swap(self, coord1: Tuple[int, int], coord2: Tuple[int, int]):
        first_x, first_y = coord1
        second_x, second_y = coord2

        if (not self._coord_within_bounds(coord1) or not self._coord_within_bounds(coord2)):
            raise IndexError

        temp = self.sand_state_bitmap[first_x, first_y]
        self.sand_state_bitmap[first_x, first_y] = self.sand_state_bitmap[second_x, second_y]
        self.sand_state_bitmap[second_x, second_y] = temp

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
        This version is optimized for performance and more natural-looking physics.
        This method currently takes the majority (80%) of the runtime of each tick, and
        it's really slow. We will have to optimize this later.
        """

        if (len(self.dirty_rects) == 0):
            return

        next_dirty_rects = []

        self._merge_overlapping_rects()
        cur_dirty_rects = self.dirty_rects

        grid = self.sand_state_bitmap
        grid_width = constants.GAME_WIDTH
        grid_height = constants.PLAYFIELD_HEIGHT

        for rect in cur_dirty_rects:

            rect_x, rect_y, width, height = rect

            # Loop from the bottom-up
            for y in range(rect_y + height - 1, rect_y - 1, -1):

                # Alternate x scanning direction for more random patterns
                x_range = range(rect_x, rect_x + width)
                if (random.getrandbits(1)):
                    x_range = reversed(x_range)

                for x in x_range:

                    # Check if within boundaries
                    if (not (0 <= x < grid_width and 0 <= y < grid_height)):
                        continue

                    # If the current pixel is empty, we do not need to do sand physics
                    if grid[x, y] == 0:
                        continue

                    # print("Checks sand logic")

                    # --- Sand Physics Logic ---

                    # 1) Check if the pixel directly below is empty.
                    # If so, we move it down.
                    # We also dirty the surrounding area.
                    if y + 1 < grid_height and grid[x, y + 1] == 0:
                        grid[x, y + 1] = grid[x, y]
                        grid[x, y] = 0
                        next_dirty_rects.append((x, y - 1, 1, 3))
                        continue

                    # 2) If straight down is blocked, check the two diagonals
                    # Randomly choose a direction: 1 for right, -1 for left
                    # This makes it more natural and randomized

                    direction = 1 if random.getrandbits(1) else -1

                    # Check the boundaries of the first diagonal in the chosen direction
                    if 0 <= (x + direction) < grid_width and y + 1 < grid_height and grid[x + direction, y + 1] == 0:
                        grid[x + direction, y + 1] = grid[x, y]
                        grid[x, y] = 0
                        next_dirty_rects.append((x - 1, y - 1, 3, 3))

                    # If the first direction failed, check the other diagonal
                    elif 0 <= (x - direction) < grid_width and y + 1 < grid_height and grid[x - direction, y + 1] == 0:
                        grid[x - direction, y + 1] = grid[x, y]
                        grid[x, y] = 0
                        next_dirty_rects.append((x - 1, y - 1, 3, 3))

        self.dirty_rects = next_dirty_rects

    def find_and_clear_lines(self):
        """
        Finds any continuous paths of same-colored sand from left to right.
        If found, clears them and returns the number of points scored.
        Returns the number of cleared sand pixels.
        """
        pass

    def update(self):
        self.apply_sand_physics()


