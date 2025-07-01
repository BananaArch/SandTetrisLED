# tetromino_view.py

import constants

import displayio

class TetrominoView:
    """
    The TetrominoView is a view class that owns the Tetromino displayio objects
        (visual components). This includes the Tetromino Group and Tetromino TileGrid.

    Its sole responsibility is to visually represent the state of a single Tetromino
        data model on the screen.
    """

    def __init__(
        self,
        sprite_sheet_bitmap: displayio.Bitmap,
        sprite_sheet_palette: displayio.Palette,
        root_group: displayio.Group,
    ):

        """
        Initializes the view for the active tetromino.

        Args:
            sprite_sheet_bitmap (displayio.Bitmap): The master sprite sheet.
            sprite_sheet_palette (displayio.Palette): The master palette.
            root_group (displayio.Group): The root_group connected to the display.
        """

        self.tetromino_tile_grid = displayio.TileGrid(
            bitmap=sprite_sheet_bitmap,
            pixel_shader=sprite_sheet_palette,
            width=constants.TETROMINO_SHAPE_DATA_SIZE,
            height=constants.TETROMINO_SHAPE_DATA_SIZE,
            tile_width=constants.MINO_SIZE,
            tile_height=constants.MINO_SIZE,
        )

        self.tetromino_group = displayio.Group()
        self.tetromino_group.append(self.tetromino_tile_grid)

        root_group.append(self.tetromino_group)

        # --- State Tracking Attributes ---

        # Used to remember the last state we drew to avoid unnecessary redraws
        #    for shape, color, and orientation.
        self._last_shape_data = None
        self._last_color_type = None

    def _redraw_shape_and_color(
        self,
        active_tetromino_shape_data : bytes,
        active_tetromino_color_type : constants.ColorType
    ):

        """
        (Internal) The "expensive" method that redraws the shape, color,
            and orientation for the Tetromino.

        Instead of passing the Tetromino object directly, we pass the attributes of the
            Tetromino object to keep the Model and View classes separated.
        """

        for i in range(len(active_tetromino_shape_data)):
            col_index = active_tetromino_shape_data[i]
            row_index = active_tetromino_color_type
            sprite_index = col_index + row_index * constants.NUM_SPRITES_PER_COLOR
            self.tetromino_tile_grid[i] = sprite_index

            # Creates the tetromino tile grid by parsing and patching the bitmap.
            # It takes the tile from the bitmap that aligns
            #       with color_type (row) and shape_data (col),
            # and then attaches it to the tilegrid at position i.
            # This logic: active_tetromino.shape_data[i] +
            #       active_tetromino.color_type * constants.NUM_SPRITES_PER_COLOR
            # is for converting 2D (row: color_type, col: shape_data) into 1D
            # Shape_data stores information about column on sprite sheet.

        # Update the state tracking variables

        self._last_shape_data = active_tetromino_shape_data
        self._last_color_type = active_tetromino_color_type

    def _update_position(self, active_tetromino_x : int, active_tetromino_y : int):
        """
        (Internal) The "cheap" method that only updates screen position.
        Instead of passing the Tetromino object directly, we pass the attributes
            of the Tetromino object to keep the Model and View classes separated.
        """

        self.tetromino_group.x = active_tetromino_x
        self.tetromino_group.y = active_tetromino_y

    def update(
        self,
        active_tetromino_shape_data : bytes,
        active_tetromino_color_type : constants.ColorType,
        active_tetromino_x : int,
        active_tetromino_y : int
    ):

        """
        The main public method. Updates the view to match the model,
            efficiently redrawing the shape only when necessary.

        Args:
            active_tetromino_shape_data (bytes): The 1D bytes
                representing the current 4x4 shape of the piece
            active_tetromino_color_type (constants.ColorType): The color
                type value of the active tetromino
            active_tetromino_x (int): The current x-coordinate (in pixels) of the piece
            active_tetromino_y (int): The current y-coordinate (in pixels) of the piece
        """
        # Check if the piece's appearance has changed
        if (active_tetromino_shape_data != self._last_shape_data or
            active_tetromino_color_type != self._last_color_type):

            # If it changed, perform the expensive redraw
            self._redraw_shape_and_color(active_tetromino_shape_data, active_tetromino_color_type)

        # Always update the position, which is cheap
        self._update_position(active_tetromino_x, active_tetromino_y)

