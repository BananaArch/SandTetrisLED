# tetromino.py

import constants

class Tetromino:
    """ This class is a model class that represents the active, falling Tetromino. """

    def __init__(self, shape_type: constants.ShapeType, color_type: constants.ColorType, start_x: int = 0, start_y: int = 0, orientation: constants.Orientation = constants.Orientation.UP):
        """
        Initializes a new Tetromino

        Args:
            shape_type (constants.ShapeType): The shape of the tetromino.py
            color_type (constants.ColorType): The color of the tetromino.py
            orientation (constants.Orientation): The orientation will almost always be starting UP.
            start_x (int): The starting x coordinate. Default: 0
            start_y (int): The starting y coordinate. Default: 0
        """

        self.x = start_x
        self.y = start_y
        self.shape_type = shape_type
        self.shape_data = constants.SHAPES[shape_type][orientation]
        self.color_type = color_type
        self.orientation = orientation

    # -- Logic Methods --

    def get_next_position(self):
        """
        Calculates where the piece WANTS to go based on its internal physics.
        Does not change its own state. Returns a proposed (x,y).
        """
        pass

    def execute_approved_move(self):
        """
        After receiving approval from the Game class that the Tetromino can fall,
        it updates its internal data to fall. Does not render it -- that is handled by GraphicsManager.
        """
        pass

    def rotate(self):
        """ Handles logic to rotate the piece. """
        pass
