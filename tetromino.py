# tetromino.py

class Tetromino:
    """ This class is a model class that represents the active, falling Tetromino. """

    def __init__(self, shape_type, orientation=Orientation.UP, start_x = 0, start_y = 0, rotation=0):
        """
        Initializes a new Tetromino

        Args:
            shape_type (ShapeType): The shape of the tetromino.py
            orientation (Orientation): The orientation will almost always be starting UP.
            start_x (int): The starting x coordinate. Default: 0
            start_y (int): The starting y coordinate. Default: 0
            rotation (int): Its rotation value. Default: 0
        """

        self.x = start_x
        self.y = start_y
        self.shape = shape
        self.rotation = rotation


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
