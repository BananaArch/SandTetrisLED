# constants.py
# This file holds all the static configuration values for the Sand Tetris game.

# -- Display and Grid Dimensions --
GAME_WIDTH = 32
GAME_HEIGHT = 64

# -- Timing --
GAME_LOOP_DELAY = 0.01  # A small delay in the main loop
INITIAL_FALL_RATE = 1.0   # Time in seconds for a piece to fall one step

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
