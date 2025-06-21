# tetromino.py

class ShapeType():
    """ This represents the 7 shapes that the Tetrominos can be. """
    I = 0
    O = 1
    T = 2
    J = 3
    L = 4
    S = 5
    Z = 6

class Orientation():
    """ This represents the orientation/rotation that the Tetrominos can be in. """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


# -- Constant bytearray representing shapes and their orientation --

I_SHAPE_DATA_UP = bytearray(( # although this is not ideal because it creates tuple, it's fine for small tuples. this might cause memory fragmentation
    0, 0, 0, 0,
    1, 1, 1, 1,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

I_SHAPE_DATA_RIGHT = bytearray((
    0, 0, 1, 0,
    0, 0, 1, 0,
    0, 0, 1, 0,
    0, 0, 1, 0,
))

I_SHAPE_DATA_DOWN = bytearray((
    0, 0, 0, 0,
    0, 0, 0, 0,
    1, 1, 1, 1,
    0, 0, 0, 0,
))

I_SHAPE_DATA_LEFT = bytearray((
    0, 1, 0, 0,
    0, 1, 0, 0,
    0, 1, 0, 0,
    0, 1, 0, 0,
))

O_SHAPE_DATA = bytearray((
    0, 0, 0, 0,
    0, 1, 1, 0,
    0, 1, 1, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_UP = bytearray((
    0, 1, 0, 0,
    1, 1, 1, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_RIGHT = bytearray((
    0, 1, 0, 0,
    0, 1, 1, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_DOWN = bytearray((
    0, 0, 0, 0,
    1, 1, 1, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_LEFT = bytearray((
    0, 1, 0, 0,
    1, 1, 0, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_UP = bytearray((
    1, 0, 0, 0,
    1, 1, 1, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_RIGHT = bytearray((
    0, 1, 1, 0,
    0, 1, 0, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_DOWN = bytearray((
    0, 0, 0, 0,
    1, 1, 1, 0,
    0, 0, 1, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_LEFT = bytearray((
    0, 1, 0, 0,
    0, 1, 0, 0,
    1, 1, 0, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_UP = bytearray((
    0, 0, 1, 0,
    1, 1, 1, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_RIGHT = bytearray((
    0, 1, 0, 0,
    0, 1, 0, 0,
    0, 1, 1, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_DOWN = bytearray((
    0, 0, 0, 0,
    1, 1, 1, 0,
    1, 0, 0, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_LEFT = bytearray((
    1, 1, 0, 0,
    0, 1, 0, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_UP = bytearray((
    0, 1, 1, 0,
    1, 1, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_RIGHT = bytearray((
    0, 1, 0, 0,
    0, 1, 1, 0,
    0, 0, 1, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_DOWN = bytearray((
    0, 0, 0, 0,
    0, 1, 1, 0,
    1, 1, 0, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_LEFT = bytearray((
    1, 0, 0, 0,
    1, 1, 0, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_UP = bytearray((
    1, 1, 0, 0,
    0, 1, 1, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_RIGHT = bytearray((
    0, 0, 1, 0,
    0, 1, 1, 0,
    0, 1, 0, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_DOWN = bytearray((
    0, 0, 0, 0,
    1, 1, 0, 0,
    0, 1, 1, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_LEFT = bytearray((
    0, 1, 0, 0,
    1, 1, 0, 0,
    1, 0, 0, 0,
    0, 0, 0, 0,
))

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
