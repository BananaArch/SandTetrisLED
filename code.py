import time
import math
import displayio
from adafruit_matrixportal.matrix import Matrix

GAME_HEIGHT = 64
GAME_WIDTH = 32
BG_COLOR = 0x000000 # background fill color
RED = 0xFF0000

DELAY = .1

# Matrix and DisplayIO Setup

matrix = Matrix(
    width=GAME_HEIGHT, # these need to be flipped for the actual board
    height=GAME_WIDTH,
    bit_depth=5, # 2^5 = 32 (5 bits) of potential colors
    rotation=270,
)

display = matrix.display
group = displayio.Group()
display.root_group = group

bg_bitmap = displayio.Bitmap(display.width, display.height, 2)
box_bitmap = displayio.Bitmap(3, 3, 2)

palette = displayio.Palette(2)
palette[0] = BG_COLOR
palette[1] = RED

bg_tilegrid = displayio.TileGrid(bg_bitmap, pixel_shader = palette)
box_tilegrid = displayio.TileGrid(box_bitmap, pixel_shader = palette, x = int(GAME_WIDTH / 2), y = 0)

group.append(bg_tilegrid)
group.append(box_tilegrid)

bg_bitmap.fill(0)
box_bitmap.fill(1)

def update_display():
    display.auto_refresh = False # Stop updating the display while changing things
    if box_tilegrid.y < GAME_HEIGHT - 3:
        box_tilegrid.y = box_tilegrid.y + 1

    display.auto_refresh = True # After changing things, you can update display

while True:
    update_display()
    print(box_tilegrid.y)
    time.sleep(DELAY)
