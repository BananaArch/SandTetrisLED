import board
import displayio
import framebufferio
import rgbmatrix
import time
from adafruit_matrixportal.matrix import Matrix

# Release any previously held displays
displayio.release_displays()

# Create Matrix object with correct dimensions
matrix = Matrix(
    width=64,
    height=32,
    bit_depth=6  # 6 is good for color depth on these panels
)


display = matrix.display

# Load the bitmap
bitmap = displayio.OnDiskBitmap("/spritesheet.bmp")

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

print(bitmap.pixel_shader)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Show the group on the display
display.root_group = group

# Loop forever
while True:
    print("Hello!")
    time.sleep(5)
    pass
