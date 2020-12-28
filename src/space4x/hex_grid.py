from typing import Iterator, List, Union

import arcade

import space4x.constants
import space4x.resources


class HexTile(arcade.Sprite):
    """A HexTile is the basic unit the game field consists of.

    Uses the 'even-r' horizontal layout.
    """

    def __init__(self, id_x: int, id_y: int) -> None:
        """Creates a HexTile for a given integer coordinate.

        The texture is loade and the position on the screen is calculated.

        Args:
            id_x (int): x-Position
            id_y (int): y-Position
        """
        super().__init__(
            filename=space4x.resources.hex_img,
            scale=space4x.constants.hex_tile_scale,
        )
        self.append_texture(
            arcade.load_texture(space4x.resources.hex_highlighted_img)
        )

        self.has_star = False

        self.id_x = id_x
        self.id_y = id_y

        if self.id_y % 2 == 0:
            self.center_x = (
                self.id_x
                * (
                    space4x.constants.hex_tile_width
                    + space4x.constants.hex_grid_margin_x
                )
                + space4x.constants.hex_tile_width // 2
                + space4x.constants.hex_grid_correction_x
            )
        else:
            self.center_x = self.id_x * (
                space4x.constants.hex_tile_width
                + space4x.constants.hex_grid_margin_x
            )
        self.center_y = (
            space4x.constants.hex_grid_origin_offset
            - self.id_y
            * (
                space4x.constants.hex_tile_height
                - (
                    space4x.constants.hex_grid_margin_y
                    + space4x.constants.hex_grid_correction_y
                )
            )
        )


class HexGrid(arcade.SpriteList):
    """A HexGrid is a collection of HexTiles that make up the game's
    field."""

    def __init__(self) -> None:
        """A Hex grid is iniatilized by creating [dim_x]x[dim_y] HexTiles.

        For values see constants.
        """
        super().__init__()
        self.dim_x = space4x.constants.hex_grid_dim_x
        self.dim_y = space4x.constants.hex_grid_dim_y
        self.tiles: List[List[Union[None, HexTile]]] = [
            [None for x in range(self.dim_x)] for y in range(self.dim_y)
        ]
        self._setup_grid()

    def _setup_grid(self) -> None:
        """Creates the HexTiles and appends them to the HexGrid."""
        for id_x in range(0, self.dim_x):
            for id_y in range(0, self.dim_y):
                new_tile = HexTile(id_x=id_x, id_y=id_y)
                self.append(new_tile)
                self.tiles[id_x][id_y] = new_tile

    def get_Tile_by_ID(self, idx: int, idy: int) -> Union[None, HexTile]:
        """Returns the HexTile for a given integer id.

        Args:
            idx (int): x-Position
            idy (int): y-Position

        Returns:
            Union[None, HexTile]: Returns the HexFile at the position or
                                  None, if it does not exist.
        """
        try:
            return self.tiles[idx][idy]
        except IndexError:
            return None

    def __iter__(self) -> Iterator[HexTile]:
        """Return an iterable object of sprites."""
        return iter(self.sprite_list)
