from typing import Iterator

import arcade

import space4x.constants
from space4x.hex_tile import HexTile


class HexGrid(arcade.SpriteList):
    def __init__(self) -> None:
        super().__init__()
        self.dim_x = space4x.constants.hex_grid_dim_x
        self.dim_y = space4x.constants.hex_grid_dim_y
        self._setup_grid()

    def _setup_grid(self) -> None:
        for id_x in range(0, self.dim_x):
            for id_y in range(0, self.dim_y):
                new_tile = HexTile(id_x=id_x, id_y=id_y)
                self.append(new_tile)

    def __iter__(self) -> Iterator[HexTile]:
        """Return an iterable object of sprites."""
        return iter(self.sprite_list)
