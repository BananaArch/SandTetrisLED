# sand_pile.py

import displayio
import random
import time

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
        # A list of sets. Each index in the list corresponds to a Y-row.
        # The set at that index contains all active X-coordinates for that row.
        self.active_rows = [set() for _ in range(constants.PLAYFIELD_HEIGHT)]
        self.odd_rows = False

    def _activate_pixel(self, coord: Tuple[int, int]):
        """A helper method to add a pixel to the active list, with boundary checks."""
        x, y = coord
        if 0 <= y < constants.PLAYFIELD_HEIGHT and 0 <= x < constants.GAME_WIDTH:
            self.active_rows[y].add(x)

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

    def _swap(self, coord1: Tuple[int, int], coord2: Tuple[int, int]):
        first_x, first_y = coord1
        second_x, second_y = coord2

        if (not self._coord_within_bounds(coord1) or not self._coord_within_bounds(coord2)):
            raise IndexError

        temp = self.sand_state_bitmap[first_x, first_y]
        self.sand_state_bitmap[first_x, first_y] = self.sand_state_bitmap[second_x, second_y]
        self.sand_state_bitmap[second_x, second_y] = temp

    def transform_and_activate_tetromino_to_sand(self, tetromino: Tetromino, sprite_sheet_bitmap: displayio.Bitmap):
        """
        Converts the given Tetromino to sand. This method has access to sprite_sheet_bitmap (a view) because it's a
        pragmatic decision based on the fact that our main 2D array is a bitmap (view).
        It also "activates" each of the pixel (adds it to the active_pixels list).

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
                    if (self._coord_within_bounds((dest_x, dest_y))):

                        # Copy the pixel's index value from the sprite sheet
                        # to the sand pile's state bitmap.
                        pixel_value = sprite_sheet_bitmap[source_x, source_y]

                        self.sand_state_bitmap[dest_x, dest_y] = pixel_value
                        self._activate_pixel((dest_x, dest_y))

    def apply_sand_physics(self):
        """
        Iterates through the SandPile and makes any unsupported sand pixels fall down.
        This version is optimized for performance and more natural-looking physics.
        It is not perfect and there may be a peeling issue with a "race condition"
        due to the nature of the cellular automata simulation.
        """

        #start_time = time.monotonic()

        has_any_active_pixels = any(self.active_rows)
        if not has_any_active_pixels:
            return


        # To create a more natural, random, less frantic-looking sand cascade, we only
        # process half of the rows each frame. This slows down the overall simulation
        # in a visually pleasing way without causing stutter.

        # Flip the boolean to alternate between processing even and odd rows each frame,
        # creating a "zebra stripe" pattern of updates over time.
        self.odd_rows = not self.odd_rows

        grid = self.sand_state_bitmap
        grid_width = constants.GAME_WIDTH
        grid_height = constants.PLAYFIELD_HEIGHT

        # This loop iterates from the bottom-up, but with a step of -2, processing
        # only every other row. The 'odd_rows' boolean determines whether we start
        # on an even or odd row, creating the interlaced "zebra" effect. This is an
        # intentional visual choice to make large cascades look less uniform and more
        # granular, as it creates temporary "holes" that fill in on the next frame.
        for y in range(grid_height - 1 - self.odd_rows, -1, -2):

            # If the row has no active pixels, we skip that row
            if not self.active_rows[y]:
                continue

            # Iterate through all x values in the row
            while self.active_rows[y]:

                x = self.active_rows[y].pop()

                # Check for bounds. We do not use self._coord_within_bounds() for performance.
                # We also make sure it excludes the bottom row. We need to do this, because
                # the code checks and manipulates the row below the current y value.

                if (not (0 <= x < grid_width and 0 <= y < grid_height)):
                    continue

                # Check if there is no sand at that pixel, if so, we skip this pixel.
                if (grid[x, y] == 0):
                    continue

                # --- PHYSICS LOGIC ---

                new_pos = None  # The new position that the pixel moves to (if it moves)

                # STEP 1) CHECK IF THE PIXEL CAN GO DOWN

                if (y + 1 < grid_height and grid[x, y + 1] == 0):
                    new_pos = (x, y + 1)

                # STEP 2) CHECK IF THE PIXEL CAN GO DIAGONALLY
                #         DOWN TO ENSURE RANDOMNESS, IT WILL RANDOMLY CHOOSE
                #         DIRECTION (LEFT OR RIGHT) IT WILL TRY TO GO DOWN FIRST.
                #         IF THE PIXEL BELOW IT HAS NOT BEEN UPDATED, IT WILL NOT
                #         GO DIAGONALLY, SINCE THAT WOULD MEAN IT WOULD USE A
                #         "FLOATING PIXEL" AS A PIVOT.

                else:
                    if (y + 2 < grid_height and grid[x, y+2] == 0):
                        # This means it's trying to use a "floating" pixel as a pivot
                        # if that is the case, we don't do anything with this pixel.
                        continue

                    direction = 1 if random.getrandbits(1) else -1

                    # CHECK THE BOUNDARIES OF THE DIAGONAL IN THE RANDOM DIRECTION. ALSO CHECK IF DIAGONAL IS EMPTY.
                    if (0 <= (x + direction) < grid_width and 0 <= y + 1 < grid_height) and (grid[x + direction, y + 1] == 0):
                        # IF IT IS, THEY SWAP
                        new_pos = (x + direction, y + 1)
                    # IF THE FIRST DIAGONAL FAILS, CHECK THE OTHER DIAGONAL.
                    elif (0 <= (x - direction) < grid_width and 0 <= y + 1 < grid_height) and (grid[x - direction, y + 1] == 0):
                        new_pos = (x - direction, y + 1)


                # UPDATE THE GRID AND WAKE UP NEIGHBORS
                if new_pos is not None:

                    # Actually move the pixel
                    grid[new_pos[0], new_pos[1]] = grid[x, y]
                    grid[x, y] = 0

                    # The pixel moved, leaving a hole. The pixels above it might now be unstable.
                    # We must add them to the active set for the next frame so they get checked.

                    if y - 1 >= 0:
                        self.active_rows[y-1].add(x)  # Above
                        if x - 1 >= 0: self.active_rows[y-1].add(x-1)  # Above-Left
                        if x + 1 < grid_width: self.active_rows[y-1].add(x+1)  # Above-Right

                    # We also need to add the new_pos, as it might fall again.
                    self.active_rows[new_pos[1]].add(new_pos[0])

        #end_time = time.monotonic()

        #print("Sand Physics Time", end_time - start_time)
        #if end_time - start_time >= constants.TICK_RATE:
        #    print(" --------------------------- Too slow --------------------")

    def find_and_clear_lines(self):
        """
        Finds any continuous paths of same-colored sand from left to right.
        If found, clears them and returns the number of points scored.
        Returns the number of cleared sand pixels.
        """
        pass

