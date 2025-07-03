# constants.py
# This file holds all the static configuration values for the Sand Tetris game.

# --- File location for Sprite Sheet ---
SPRITE_FILE_LOCATION = "/spritesheet.bmp"

# --- Display and Grid Dimensions ---
GAME_WIDTH = 32
GAME_HEIGHT = 64
INFO_BAR_HEIGHT = 5
PLAYFIELD_HEIGHT = GAME_HEIGHT - INFO_BAR_HEIGHT

# --- Timing ---
TPS = 20  # The amount of ticks that run in a single second
# If the TPS is too fast, the controller will not respect it and run as
# fast as it can.
TICK_RATE = 1.0 / TPS

# --- Input ---
MATRIX_PORTAL_LIS3DH_ADDRESS = 0x19
TAP_THRESHOLD = 100
SHAKE_THRESHOLD = 25
TAP_COOLDOWN = 0.1  # the time in seconds before another tap (rotate) can occur

# --- Sand Physics ---

# Only merge if the new area of dirty rectangle is less than 2x the old areas.
MERGE_HEURISTIC_FACTOR = 1.5


# --- Tetromino Physics ---
INITIAL_FALL_RATE = 0.05  # the seconds it takes for the tetromino to fall 1 px. Default: 0.15
FALL_RATE_DECREMENTATION_RATE = 0.025  # removes this value from the fall_rate when Tetromino calls decrement_fall_rate()
TETROMINO_FALLEN_NEXT_LEVEL = 10  # requires 10 tetrominos to fall to speed up

TILT_THRESHOLD_SMALL_RIGHT = 15.0  # the tilt (in degrees) it takes to move the tetromino rightslowly
TILT_THRESHOLD_SMALL_LEFT = -15.0  # the tilt (in degrees) it takes to move the tetromino left

# --- Tetromino Dimensions ---

# The size (in minos) of the logical grid used to store the shape data for
# every tetromino piece. Since all standard tetrominos fit within a 4x4 area,
# this value is 4. It's used to translate 2D coordinates into a 1D index
# and vice versa for the SHAPE_DATA (bytes) shown below.
TETROMINO_SHAPE_DATA_SIZE = 4

# This is the scale-up for the Mino.
# This means for each mino, it is going to be 3 px by 3 px
MINO_SIZE = 3

# --- Tetromino Starting Location ---
TETROMINO_START_X = 13  # where the tetromino starts

# --- Tetromino Rotation Logic ---
MAX_SHIFTS = 6
# the maximum shifts/wall kick positions it will move until it
# it gives up trying to find a valid position

# --- Colors ---
NUM_SPRITES_PER_COLOR = 15


# --- Color enum class by Row Number ---
# (e.g., Blue is Row 1, Red is Row 2, ...)
# Used for rendering tetromino

class ColorType:
    BLUE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    WHITE = 4

# --- Shape Enums ---

class ShapeType:
    """Namespace for the 7 unique tetromino shapes, using strings as keys."""
    I = 0
    O = 1
    T = 2
    L = 3
    J = 4
    S = 5
    Z = 6

class Orientation:
    """Namespace for the 4 possible orientations. The values are the direct indices."""
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

NUM_ORIENTATIONS = 4

# --- Lists for Random Selection ---

# A list of all possible shape types to be used with random.choice()
SHAPE_TYPE_POPULATION = [
    ShapeType.I, ShapeType.O, ShapeType.T, ShapeType.L,
    ShapeType.J, ShapeType.S, ShapeType.Z
]

# A list of all possible color types for weighted selection
COLOR_TYPE_POPULATION_WEIGHTED = [
    ColorType.BLUE, ColorType.BLUE, ColorType.BLUE, ColorType.BLUE,
    ColorType.RED, ColorType.RED, ColorType.RED, ColorType.RED,
    ColorType.GREEN, ColorType.GREEN, ColorType.GREEN, ColorType.GREEN,
    ColorType.YELLOW, ColorType.YELLOW, ColorType.YELLOW, ColorType.YELLOW,
    ColorType.WHITE
]

NEXT_COLOR_CHANCE = 0.65

# The corresponding weights for the color
COLOR_WEIGHTS = [
    22.5,  # Blue
    22.5,  # Red
    22.5,  # Green
    22.5,  # Yellow
    10.0,  # White (wildcard, rare)
]


# --- Constant bytes representing shapes and their orientation ---

# The number represents the column number in the spritesheet.

I_SHAPE_DATA_UP = bytes((
# although this is not ideal because it creates tuple, it's fine for small tuples. this might cause memory fragmentation
    0, 0, 0, 0,
    4, 5, 5, 6,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

I_SHAPE_DATA_RIGHT = bytes((
    0, 0, 1, 0,
    0, 0, 2, 0,
    0, 0, 2, 0,
    0, 0, 3, 0,
))

I_SHAPE_DATA_DOWN = bytes((
    0, 0, 0, 0,
    0, 0, 0, 0,
    4, 5, 5, 6,
    0, 0, 0, 0,
))

I_SHAPE_DATA_LEFT = bytes((
    0, 1, 0, 0,
    0, 2, 0, 0,
    0, 2, 0, 0,
    0, 3, 0, 0,
))

O_SHAPE_DATA = bytes((
    0, 0, 0, 0,
    0, 7, 8, 0,
    0, 9, 10, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_UP = bytes((
    0, 1, 0, 0,
    4, 11, 6, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_RIGHT = bytes((
    0, 1, 0, 0,
    0, 12, 6, 0,
    0, 3, 0, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_DOWN = bytes((
    0, 0, 0, 0,
    4, 13, 6, 0,
    0, 3, 0, 0,
    0, 0, 0, 0,
))

T_SHAPE_DATA_LEFT = bytes((
    0, 1, 0, 0,
    4, 14, 0, 0,
    0, 3, 0, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_UP = bytes((
    1, 0, 0, 0,
    9, 5, 6, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_RIGHT = bytes((
    0, 7, 6, 0,
    0, 2, 0, 0,
    0, 3, 0, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_DOWN = bytes((
    0, 0, 0, 0,
    4, 5, 8, 0,
    0, 0, 3, 0,
    0, 0, 0, 0,
))

J_SHAPE_DATA_LEFT = bytes((
    0, 1, 0, 0,
    0, 2, 0, 0,
    4, 10, 0, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_UP = bytes((
    0, 0, 1, 0,
    4, 5, 10, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_RIGHT = bytes((
    0, 1, 0, 0,
    0, 2, 0, 0,
    0, 9, 6, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_DOWN = bytes((
    0, 0, 0, 0,
    7, 5, 6, 0,
    3, 0, 0, 0,
    0, 0, 0, 0,
))

L_SHAPE_DATA_LEFT = bytes((
    4, 8, 0, 0,
    0, 2, 0, 0,
    0, 3, 0, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_UP = bytes((
    0, 7, 6, 0,
    4, 10, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_RIGHT = bytes((
    0, 1, 0, 0,
    0, 9, 8, 0,
    0, 0, 3, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_DOWN = bytes((
    0, 0, 0, 0,
    0, 7, 6, 0,
    4, 10, 0, 0,
    0, 0, 0, 0,
))

S_SHAPE_DATA_LEFT = bytes((
    1, 0, 0, 0,
    9, 8, 0, 0,
    0, 3, 0, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_UP = bytes((
    4, 8, 0, 0,
    0, 9, 6, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_RIGHT = bytes((
    0, 0, 1, 0,
    0, 7, 10, 0,
    0, 3, 0, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_DOWN = bytes((
    0, 0, 0, 0,
    4, 8, 0, 0,
    0, 9, 6, 0,
    0, 0, 0, 0,
))

Z_SHAPE_DATA_LEFT = bytes((
    0, 1, 0, 0,
    7, 10, 0, 0,
    3, 0, 0, 0,
    0, 0, 0, 0,
))

# --- The Main SHAPES Dictionary ---
# This dictionary uses the string values from the ShapeType class as keys.
SHAPES = {
    ShapeType.I: [I_SHAPE_DATA_UP, I_SHAPE_DATA_RIGHT, I_SHAPE_DATA_DOWN, I_SHAPE_DATA_LEFT],
    ShapeType.O: [O_SHAPE_DATA, O_SHAPE_DATA, O_SHAPE_DATA, O_SHAPE_DATA],
        # Memory: It's okay having four of the same bytes arrays in the list above because
        # python only creates one 'real' bytes array and the rest are pointers. Also,
        # we don't care about flash memory as much as RAM. The bytes are typically stored
        # in flash memory.
    ShapeType.T: [T_SHAPE_DATA_UP, T_SHAPE_DATA_RIGHT, T_SHAPE_DATA_DOWN, T_SHAPE_DATA_LEFT],
    ShapeType.L: [L_SHAPE_DATA_UP, L_SHAPE_DATA_RIGHT, L_SHAPE_DATA_DOWN, L_SHAPE_DATA_LEFT],
    ShapeType.J: [J_SHAPE_DATA_UP, J_SHAPE_DATA_RIGHT, J_SHAPE_DATA_DOWN, J_SHAPE_DATA_LEFT],
    ShapeType.S: [S_SHAPE_DATA_UP, S_SHAPE_DATA_RIGHT, S_SHAPE_DATA_DOWN, S_SHAPE_DATA_LEFT],
    ShapeType.Z: [Z_SHAPE_DATA_UP, Z_SHAPE_DATA_RIGHT, Z_SHAPE_DATA_DOWN, Z_SHAPE_DATA_LEFT],
}

