# tetromino.py

import constants

class Tetromino:
    """ This class is a model class that represents the active, falling Tetromino. """

    def __init__(self, shape_type: constants.ShapeType, color_type: constants.ColorType, start_x: int = 0, start_y: int = 0, fall_rate : float = constants.INITIAL_FALL_RATE, orientation: constants.Orientation = constants.Orientation.UP):
        """
        Initializes a new Tetromino

        Args:
            shape_type (constants.ShapeType): The shape of the tetromino.py
            color_type (constants.ColorType): The color of the tetromino.py
            orientation (constants.Orientation): The orientation will almost always be starting UP.
            start_x (int): The starting x coordinate. Default: 0
            start_y (int): The starting y coordinate. Default: 0
        """

        # --- Physics Attributes ---
        self.x = start_x
        self.y = start_y
        self.fall_rate = constants.INITIAL_FALL_RATE
        self.gravity_timer = 0.0

        # --- Characteristic Attribute ---
        self.shape_type = shape_type
        self.color_type = color_type
        self.orientation = orientation

    def get_shape_data(self):
        return constants.SHAPES[self.shape_type][self.orientation]

    def get_coords(self):
        return (self.x, self.y)

    def get_next_position(self, dt: float, tilt_angle : float):
        """
        Calculates where the piece WANTS to go based on its internal physics.
        Does not change its own state. Returns a proposed (x,y).

        Args:
            dt (float): the time since last move.
            tilt_angle (float): the angle at which the matrix is tilted.
        """

        proposed_dx = 0
        proposed_dy = 0

        self.gravity_timer += dt

        if self.gravity_timer >= self.fall_rate:  # If enough time has passed, a gravity step will occur
            proposed_dy = 1

        if tilt_angle > constants.TILT_THRESHOLD_LARGE_RIGHT:
            proposed_dx = 2
        elif tilt_angle > constants.TILT_THRESHOLD_SMALL_RIGHT:
            proposed_dx = 1
        elif tilt_angle < constants.TILT_THRESHOLD_LARGE_LEFT:
            proposed_dx = -2
        elif tilt_angle < constants.TILT_THRESHOLD_SMALL_LEFT:
            proposed_dx = -1

        return (self.x + proposed_dx, self.y + proposed_dy)

    def execute_approved_move(self, new_x : int, new_y : int):
        """
        After receiving approval from the Game class that the Tetromino can fall,
        it updates its internal data to fall. Does not render it -- that is handled by GraphicsManager.
        """

        if new_y > self.y:
            self.gravity_timer -= self.fall_rate # reset the gravity timer

        self.x = new_x
        self.y = new_y

    def decrement_fall_rate(self):

        new_fall_rate = self.fall_rate - constants.FALL_RATE_DECREMENTATION_RATE
        if new_fall_rate < constants.TICK_RATE:  # The tetromino can't fall faster than TPS
            self.fall_rate = constants.TICK_RATE
        else:
            self.fall_rate = new_fall_rate

    def rotate(self):
        """ Handles logic to rotate the piece. """

        self.orientation = (self.orientation + 1) % constants.NUM_ORIENTATIONS


    def reset(self, shape_type : constants.ShapeType, color_type : constants.ColorType):
        """
        Resets the Active Tetromino into a new Tetromino with shape_type and color_type.
        All new Tetrominos start with the UP orientation.
        """
        self.orientation = constants.Orientation.UP

        pass
