# constants.py
# This file holds all the static configuration values for the Sand Tetris game.

# -- Display and Grid Dimensions --
GAME_WIDTH = 32
GAME_HEIGHT = 64

# -- Timing --
GAME_LOOP_DELAY = 0.1  # A small delay in the main loop
INITIAL_FALL_RATE = 1.0   # Time in seconds for a piece to fall one step

# -- Tetromino Dimensions --

# The width (in minos) of the logical grid used to store the shape data for
# every tetromino piece. Since all standard tetrominos fit within a 4x4 area,
# this value is 4. It's used to translate 2D coordinates into a 1D index
# and vice versa for the SHAPE_DATA (bytearray) in the tetromino.py file.
TETROMINO_SHAPE_DATA_WIDTH = 4

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

