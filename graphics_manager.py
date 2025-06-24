# graphics_manager.py

import constants

import displayio
import adafruit_imageload
from adafruit_matrixportal.matrix import Matrix


class GraphicsManager:
    """ The GraphicsManager is a view class that owns all displayio objects (visual components). It also handles the main Matrix. """

    def __init__(self):
        """ Initializes display and creates all displayio objects. """

        displayio.release_displays()  # ensures no previous displays displaying

        self.matrix = Matrix(
            width=constants.GAME_HEIGHT, # these need to be flipped for the actual board
            height=constants.GAME_WIDTH,
            bit_depth=5, # 2^5 = 32 (5 bits) of potential colors
            rotation=270,
        )
        self.display = self.matrix.display

        self.root_group = displayio.Group()
        self.display.root_group = self.root_group

        self.sprite_sheet_bitmap, self.sprite_sheet_palette = adafruit_imageload.load(
            "/spritesheet.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )

        self.active_tetromino_group = displayio.Group()

        self.root_group.append(self.active_tetromino_group)

    def update_display(self, active_tetromino: Tetromino):
        """ Main Update Display method that will be called by the Game to update EVERYTHING related to the display. """

        self.display.auto_refresh = False # Stop updating the display while changing things

        self.update_tetromino_position(active_tetromino)

        self.display.auto_refresh = True # After changing things, you can update display

    def create_tetromino_tile_grid_and_group(self, active_tetromino: Tetromino):
        """ Creates the Tile Grid rendering for the Tetromino piece, accounting for orientation, position, and color. """
        self.active_tetromino_tile_grid = displayio.TileGrid(
            self.sprite_sheet_bitmap,
            pixel_shader = self.sprite_sheet_palette,
            width = constants.TETROMINO_SHAPE_DATA_SIZE,
            height = constants.TETROMINO_SHAPE_DATA_SIZE,
            tile_width = constants.MINO_SIZE,
            tile_height = constants.MINO_SIZE,
        )

        for i in range(0, constants.TETROMINO_SHAPE_DATA_SIZE ** 2):
            self.active_tetromino_tile_grid[i] = active_tetromino.shape_data[i] + active_tetromino.color_type * constants.NUM_SPRITES_PER_COLOR
            # Creates the tetromino tile grid by parsing and patching the bitmap.
            # It takes the tile from the bitmap that aligns with color_type (row) and shape_data (col),
            # and then attaches it to the tilegrid at position i.
            # This logic: active_tetromino.shape_data[i] + active_tetromino.color_type * constants.NUM_SPRITES_PER_COLOR
            # is for converting 2D (row: color_type, col: shape_data) into 1D
            # Shape_data stores information about column on sprite sheet.

        self.active_tetromino_group.x = active_tetromino.x
        self.active_tetromino_group.y = active_tetromino.y

        self.active_tetromino_group.append(self.active_tetromino_tile_grid)

    def update_tetromino_position(self, active_tetromino: Tetromino):
        self.active_tetromino_group.x = active_tetromino.x
        self.active_tetromino_group.y = active_tetromino.y

    def create_infobar_group(self):
        """ helper class for constructor to create infobar layout. """
        pass

    def update_score_display(self, score: int):
        """ updates the score on the infobar. """
        pass

    def update_next_tetromino(self, active_tetromino: Tetromino):
        """ updates what the next tetromino is going to be on the infobar. """
        pass

    def draw_active_tetromino(self, active_tetromino: Tetromino):
        """ draws the current tetromino. """
        pass



