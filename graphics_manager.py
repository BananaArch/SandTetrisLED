# graphics_manager.py

import constants

import displayio
from adafruit_matrixportal.matrix import Matrix

class GraphicsManager:
    """ The GraphicsManager is a view class that owns all displayio objects (visual components). It also handles the main Matrix. """

    def __init__(self):
        """ Initializes display and creates all displayio objects. """
        self.matrix = Matrix(
            width=constants.GAME_HEIGHT, # these need to be flipped for the actual board
            height=constants.GAME_WIDTH,
            bit_depth=5, # 2^5 = 32 (5 bits) of potential colors
            rotation=270,
        )
        self.display = self.matrix.display
        self.root_group = displayio.Group()
        self.display.root_group = self.root_group

        self.palette = displayio.Palette(2)
        self.palette[0] = constants.BG_COLOR
        self.palette[1] = constants.RED

        self.bg_bitmap = displayio.Bitmap(constants.GAME_WIDTH, constants.GAME_HEIGHT, 2)

        self.bg_tilegrid = displayio.TileGrid(self.bg_bitmap, pixel_shader = self.palette)
        self.bg_bitmap.fill(0)

        self.root_group.append(self.bg_tilegrid)

        self.create_box()

    def update_display(self):
        """ Main Update Display method that will be called by the Game to update EVERYTHING related to the display. """

        self.display.auto_refresh = False # Stop updating the display while changing things

        self.update_box_display()

        self.display.auto_refresh = True # After changing things, you can update display

    def create_box(self):
        self.box_bitmap = displayio.Bitmap(3, 3, 2)
        self.box_tilegrid = displayio.TileGrid(self.box_bitmap, pixel_shader = self.palette, x = int(constants.GAME_WIDTH / 2), y = 0)
        self.box_bitmap.fill(1)
        self.root_group.append(self.box_tilegrid)

    def update_box_display(self):
        if self.box_tilegrid.y < constants.GAME_HEIGHT - 3:
            self.box_tilegrid.y = self.box_tilegrid.y + 1
        else:
            self.box_tilegrid.y=0

        print(self.box_tilegrid.y)

    def create_infobar_group(self):
        """ helper class for constructor to create infobar layout. """
        pass

    def update_score_display(self, score):
        """ updates the score on the infobar. """
        pass

    def update_next_tetromino(self, tetromino):
        """ updates what the next tetromino is going to be on the infobar. """
        pass

    def draw_active_tetromino(self, active_tetromino):
        """ draws the current tetromino. """
        pass



