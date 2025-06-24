# graphics_manager.py

import constants

import displayio
import adafruit_imageload
from adafruit_matrixportal.matrix import Matrix


class GraphicsManager:
    """
    The GraphicsManager is a view class that owns and manages the main displayio objects (visual components).
    This includes the matrix, the display, the root_group, and the sprite sheets.
    Think about it like the Asset Manager for our program.
    """

    def __init__(self):
        """ Initializes display and creates all displayio objects. """

        displayio.release_displays()  # ensures no previous displays displaying

        self._matrix = Matrix(
            width=constants.GAME_HEIGHT, # these need to be flipped for the actual board
            height=constants.GAME_WIDTH,
            bit_depth=5, # 2^5 = 32 (5 bits) of potential colors
            rotation=270,
        )
        self._display = self._matrix.display

        self.root_group = displayio.Group()
        self._display.root_group = self.root_group

        self.sprite_sheet_bitmap, self.sprite_sheet_palette = adafruit_imageload.load(
            "/spritesheet.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )

        self.sprite_sheet_palette.make_transparent(0)


    def begin_frame(self):
        """
        Disable the display's automatic refresh.

        This method prepares the display for a batch of drawing operations
        by turning off automatic screen updates. This can improve performance
        and prevent flickering during multiple graphical changes.
        """
        self._display.auto_refresh = False

    def end_frame(self):
        """
        Re-enable the display's automatic refresh.

        This method signals the end of the batch drawing operations by turning
        automatic screen updates back on, allowing the display to refresh and
        show all the accumulated changes at once.
        """
        self._display.auto_refresh = True

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



