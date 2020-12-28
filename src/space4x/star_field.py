from typing import Set

import arcade  # type: ignore
import numpy as np  # type: ignore

import space4x.constants
import space4x.resources
from space4x.hex_grid import HexGrid, HexTile


class Star(arcade.Sprite):
    def __init__(self, center_x: int, center_y: int) -> None:
        super().__init__(
            filename=space4x.resources.star_img,
            scale=space4x.constants.star_img_scale,
        )
        self.center_x = center_x
        self.center_y = center_y


class StarField(arcade.SpriteList):
    def __init__(self, hex_grid: HexGrid) -> None:
        super().__init__()
        self.hex_grid = hex_grid
        self._create_stars()

    def _create_stars(self) -> None:
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
            hex_tile.has_star = True
            center_x = hex_tile.center_x
            center_y = hex_tile.center_y
            self.append(Star(center_x=center_x, center_y=center_y))
