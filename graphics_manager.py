# graphics_manager.py

import displayio
import constants

class GraphicsManager:
    """ The GraphicsManager is a view class that owns all displayio objects (visual components). It also handles the main Matrix. """

    def __init__(self):
        """ Initializes display and creates all displayio objects. """

        pass

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


