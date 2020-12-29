from __future__ import annotations

from typing import Iterator, Union

import arcade  # type: ignore

import space4x.constants
import space4x.resources


class OffsetCoordinate:
    """Simple Wrapper class for 2D Coordinates."""

    def __init__(self, x: int, y: int) -> None:
        """Initializes a 2D Coordinate.

        Args:
            x (int): x-Position
            y (int): y-Position
        """
        self.x = x
        self.y = y


class OffsetHash(dict):
    """A HashTable inheriting from dict for offset coordinates."""

    def get_identifier(self, x: int, y: int) -> str:
        """Returns a unique identifier for offset coordinates.

        Args:
            x (int): x-Position
            y (int): y-Position

        Returns:
            str: Identifier
        """
        return f"x:{x},y:{y}"


class CubeCoordinate:
    """Simple Wrapper class for 3D Coordinates."""

    def __init__(self, x: int, y: int, z: int) -> None:
        """Initializes a 3D Coordinate.

        Args:
            x (int): x-Position
            y (int): y-Position
            z (int): z-Position
        """
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_offset_coordinate(
        cls, offset_coordinate: OffsetCoordinate
    ) -> CubeCoordinate:
        """Creates a cube coordinate by converting an offset coordinate.

        Args:
            offset_coordinate (OffsetCoordinate): x, y coordinates (2D)

        Returns:
            CubeCoordinate: x, y, z (3D)
        """
        x = (
            offset_coordinate.x
            - (offset_coordinate.y + (offset_coordinate.y & 1)) // 2
        )
        z = offset_coordinate.y
        y = -x - z
        return cls(x, y, z)


class CubeHash(dict):
    """A HashTable inheriting from dict for cube coordinates."""

    def get_identifier(self, x: int, y: int, z: int) -> str:
        """Returns a unique identifier for cube coordinates.

        Args:
            x (int): x-Position
            y (int): y-Position
            z (int): z-Position

        Returns:
            str: Identifier
        """
        return f"x:{x},y:{y},z:{z}"


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
        self.cube_coordinate = CubeCoordinate.from_offset_coordinate(
            offset_coordinate=self.offset_coordinate
        )

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
        self.offset_hash = OffsetHash()
        self.cube_hash = CubeHash()
        self._setup_grid()

    def _setup_grid(self) -> None:
        """Creates the HexTiles and appends them to the HexGrid."""
        for x in range(0, self.dim_x):
            for y in range(0, self.dim_y):
                new_tile = HexTile(x=x, y=y)
                self.append(new_tile)
                self.offset_hash[
                    self.offset_hash.get_identifier(
                        x=new_tile.offset_coordinate.x,
                        y=new_tile.offset_coordinate.y,
                    )
                ] = new_tile
                self.cube_hash[
                    self.cube_hash.get_identifier(
                        x=new_tile.cube_coordinate.x,
                        y=new_tile.cube_coordinate.y,
                        z=new_tile.cube_coordinate.z,
                    )
                ] = new_tile

    def get_Tile_by_xy(self, x: int, y: int) -> Union[None, HexTile]:
        """Returns the HexTile for a given offset coordinate.

        Args:
            x (int): x-Position
            y (int): y-Position

        Returns:
            Union[None, HexTile]: Returns the HexFile at the position or
                                  None, if it does not exist.
        """
        try:
            return self.offset_hash[
                self.offset_hash.get_identifier(x=x, y=y)
            ]
        except KeyError:
            return None

    def get_Tile_by_xyz(
        self, x: int, y: int, z: int
    ) -> Union[None, HexTile]:
        """Returns the HexTile for a given cube coordinate.

        Args:
            x (int): x-Position
            y (int): y-Position
            z (int): z-Position

        Returns:
            Union[None, HexTile]: Returns the HexFile at the position or
                                  None, if it does not exist.
        """
        try:
            return self.cube_hash[
                self.cube_hash.get_identifier(x=x, y=y, z=z)
            ]
        except KeyError:
            return None

    def __iter__(self) -> Iterator[HexTile]:
        """Return an iterable object of sprites."""
        return iter(self.sprite_list)
