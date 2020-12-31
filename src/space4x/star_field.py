from typing import Set

import arcade  # type: ignore
import numpy as np  # type: ignore

import space4x.constants
import space4x.resources
from space4x.hex_grid import HexGrid, HexTile
from space4x.star import Star


class StarField(arcade.SpriteList):
    """A star field consisting of multiple stars."""

    def __init__(self, hex_grid: HexGrid) -> None:
        """Creates a star field on a given hex field.

        Args:
            hex_grid (HexGrid): Hex grid of the game
        """
        super().__init__()
        self.hex_grid = hex_grid
        self._create_stars()

    def _create_stars(self) -> None:
        """Initializes stars at random positions (hex tiles)."""
        number_of_hexes = len(self.hex_grid)
        number_of_stars = int(
            space4x.constants.star_to_hex_ratio * number_of_hexes
        )
        hex_ids: Set[int] = set()
        while len(hex_ids) < number_of_stars:
            if (
                hex_id := np.random.randint(
                    low=0, high=number_of_hexes - 1
                )
            ) not in hex_ids:
                hex_ids.add(hex_id)
        for hex_id in hex_ids:
            hex_tile: HexTile = self.hex_grid[hex_id]
            center_x = hex_tile.center_x
            center_y = hex_tile.center_y
            new_star = Star(center_x=center_x, center_y=center_y)
            self.append(new_star)
            hex_tile.set_star(star=new_star)
