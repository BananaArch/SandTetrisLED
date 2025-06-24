# sand_pile_view.py

import constants

import displayio

class SandPileView:
    """
    The SandPileView is a view class that owns the SandPile displayio objects
        (visual components). This includes the SandPile Bitmap and the SandPile Group.
        We will mainly be working on the BitMap. The TileGrid is kind-of useless; it's
        it's just a wrapper class for BitMap so that we can convert it into a group.

    Its sole responsibility is to visually represent the state of a single Tetromino
        data model on the screen.
    """

    def __init__(
        self,
        sprite_sheet_palette: displayio.Palette,
        root_group: displayio.Group,
    ):

        """
        Initializes the view class for the SandPile.

        Args:
            sprite_sheet_palette (displayio.Palette): The master palette of
                potential colors that can come up in the SandPile.
            root_group (displayio.Group): The root_group connected to the display.
        """

        self.sand_palette = sprite_sheet_palette

        self.sand_state_bitmap = displayio.Bitmap(
            constants.GAME_WIDTH,  # width
            constants.PLAYFIELD_HEIGHT,  # height
            len(self.sand_palette),  # value_count
        )

        self._sand_tile_grid = displayio.TileGrid(
            bitmap=self.sand_state_bitmap,
            pixel_shader=self.sand_palette,
            width=1, # The grid is only 1 tile wide
            height=1, # The grid is only 1 tile high
            tile_width=constants.GAME_WIDTH,
            tile_height=constants.PLAYFIELD_HEIGHT,
        )

        root_group.append(self._sand_tile_grid)
        # No dedicated sand_group needed, as the sand_tilegrid is a single visual object that never moves.

    def update(self):

        """
        The main public method. Updates the view to match the model.

        Args:

        """

        pass
