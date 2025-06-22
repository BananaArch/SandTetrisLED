# constants.py
# This file holds all the static configuration values for the Sand Tetris game.

# -- Display and Grid Dimensions --
GAME_WIDTH = 32
GAME_HEIGHT = 64
INFO_BAR_HEIGHT = 5
PLAYFIELD_HEIGHT = GAME_HEIGHT - INFO_BAR_HEIGHT

# -- Timing --
GAME_LOOP_DELAY = 0.1  # A small delay in the main loop
INITIAL_FALL_RATE = 1.0   # Time in seconds for a piece to fall one step

# -- Timing --
GAME_LOOP_DELAY = 0.01
INITIAL_FALL_RATE = 0.5

# -- Tetromino Dimensions --

# The width (in minos) of the logical grid used to store the shape data for
# every tetromino piece. Since all standard tetrominos fit within a 4x4 area,
# this value is 4. It's used to translate 2D coordinates into a 1D index
# and vice versa for the SHAPE_DATA (bytearray) shown below.
TETROMINO_SHAPE_DATA_WIDTH = 4

# This is the scale-up for the Mino.
# This means for each mino, it is going to be 3 px by 3 px
MINO_SIZE = 3

# -- Colors --
BG_COLOR = 0x000000  # black
RED = 0xFF0000
GREEN = 0x00FF00
BLUE = 0x0000FF
YELLOW = 0xFFFF00

RED_SAND_COLORS = [
    0xFFA07A,  # Light Red
    0xFF0000,  # Pure Red
    0x8B0000,  # Dark Red
    0xDC143C,  # Crimson
]

# -- Shape Enums --

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

# -- Constant bytearray representing shapes and their orientation --

I_SHAPE_DATA_UP = bytearray((
# although this is not ideal because it creates tuple, it's fine for small tuples. this might cause memory fragmentation
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

# --- The Main SHAPES Dictionary ---
# This dictionary uses the string values from the ShapeType class as keys.
SHAPES = {
    ShapeType.I: [I_SHAPE_DATA_UP, I_SHAPE_DATA_RIGHT, I_SHAPE_DATA_DOWN, I_SHAPE_DATA_LEFT],
    ShapeType.O: [O_SHAPE_DATA, O_SHAPE_DATA, O_SHAPE_DATA, O_SHAPE_DATA],
        # Memory: It's okay having four of the same bitearrays in the list above because
        # python only creates one 'real' bytearray and the rest are pointers.
    ShapeType.T: [T_SHAPE_DATA_UP, T_SHAPE_DATA_RIGHT, T_SHAPE_DATA_DOWN, T_SHAPE_DATA_LEFT],
    ShapeType.L: [L_SHAPE_DATA_UP, L_SHAPE_DATA_RIGHT, L_SHAPE_DATA_DOWN, L_SHAPE_DATA_LEFT],
    ShapeType.J: [J_SHAPE_DATA_UP, J_SHAPE_DATA_RIGHT, J_SHAPE_DATA_DOWN, J_SHAPE_DATA_LEFT],
    ShapeType.S: [S_SHAPE_DATA_UP, S_SHAPE_DATA_RIGHT, S_SHAPE_DATA_DOWN, S_SHAPE_DATA_LEFT],
    ShapeType.Z: [Z_SHAPE_DATA_UP, Z_SHAPE_DATA_RIGHT, Z_SHAPE_DATA_DOWN, Z_SHAPE_DATA_LEFT],
}

