from typing import Iterator, List, Union

import arcade  # type: ignore

import space4x.constants
import space4x.resources


class OffsetCoordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class CubeCoordinate:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


class HexTile(arcade.Sprite):
    """A HexTile is the basic unit the game field consists of."""

    def __init__(self, x: int, y: int) -> None:
        """Creates a HexTile for a given integer coordinate.

        The texture is loade and the position on the screen is calculated.

        Args:
            x (int): x-Position
            y (int): y-Position
        """
        super().__init__(
            filename=space4x.resources.hex_img,
            scale=space4x.constants.hex_tile_scale,
        )
        self.append_texture(
            arcade.load_texture(space4x.resources.hex_highlighted_img)
        )

        self.has_star = False

        self.offset_coordinate = OffsetCoordinate(x, y)
        self.cube_coordinate = self._get_cube_coordinate()

        if self.offset_coordinate.y & 1 == 0:
            self.center_x = (
                self.offset_coordinate.x
                * (
                    space4x.constants.hex_tile_width
                    + space4x.constants.hex_grid_margin_x
                )
                + space4x.constants.hex_tile_width // 2
                + space4x.constants.hex_grid_correction_x
            )
        else:
            self.center_x = self.offset_coordinate.x * (
                space4x.constants.hex_tile_width
                + space4x.constants.hex_grid_margin_x
            )
        self.center_y = (
            space4x.constants.hex_grid_origin_offset
            - self.offset_coordinate.y
            * (
                space4x.constants.hex_tile_height
                - (
                    space4x.constants.hex_grid_margin_y
                    + space4x.constants.hex_grid_correction_y
                )
            )
        )

    def _get_cube_coordinate(self):
        x = (
            self.offset_coordinate.x
            - (self.offset_coordinate.y + (self.offset_coordinate.y & 1))
            // 2
        )
        z = self.offset_coordinate.y
        y = -x - z
        return CubeCoordinate(x, y, z)


class HexGrid(arcade.SpriteList):
    """A HexGrid is a collection of HexTiles that make up the game's field.

    Uses the 'even-r' horizontal layout.
    """

    def __init__(self) -> None:
        """A Hex grid is iniatilized by creating [dim_x]x[dim_y] HexTiles.

        For values see constants.
        """
        super().__init__()
        self.dim_x = space4x.constants.hex_grid_dim_x
        self.dim_y = space4x.constants.hex_grid_dim_y
        self.tiles_offset: List[List[Union[None, HexTile]]] = [
            [None for x in range(self.dim_x)] for y in range(self.dim_y)
        ]
        self._setup_grid()

    def _setup_grid(self) -> None:
        """Creates the HexTiles and appends them to the HexGrid."""
        for x in range(0, self.dim_x):
            for y in range(0, self.dim_y):
                new_tile = HexTile(x=x, y=y)
                self.append(new_tile)
                self.tiles_offset[x][y] = new_tile

    def get_Tile_by_xy(self, x: int, y: int) -> Union[None, HexTile]:
        """Returns the HexTile for a given integer id.

        Args:
            idx (int): x-Position
            idy (int): y-Position

        Returns:
            Union[None, HexTile]: Returns the HexFile at the position or
                                  None, if it does not exist.
        """
        try:
            return self.tiles_offset[x][y]
        except IndexError:
            return None

    def __iter__(self) -> Iterator[HexTile]:
        """Return an iterable object of sprites."""
        return iter(self.sprite_list)
