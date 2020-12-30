import math
from typing import List

import arcade

import space4x.constants
import space4x.resources
from space4x.hex_grid import HexGrid, HexTile


class Spaceship(arcade.Sprite):
    def __init__(self, hex_grid: HexGrid, x: int, y: int) -> None:
        super().__init__(
            filename=space4x.resources.space_ship_img,
            scale=space4x.constants.space_ship_img_scale,
        )
        self.hex_grid = hex_grid
        hex_tile: HexTile = self.hex_grid.get_Tile_by_xy(x=x, y=y)  # type: ignore
        self.offset_coordinate = hex_tile.offset_coordinate
        self.cube_coordinate = hex_tile.cube_coordinate
        self.center_x = hex_tile.center_x
        self.center_y = hex_tile.center_y
        self.path: List[HexTile] = []
        self.timer: float = 0

    def update(self, delta_time: float = 1 / 60) -> None:
        super().update()

        self.timer += delta_time
        if not self.timer > 1 / space4x.constants.space_ship_speed:
            return

        self.timer = 0

        if not len(self.path) == 0:
            current_target: HexTile = self.path[0]
            if (current_target.center_x == self.center_x) and (
                current_target.center_y == self.center_y
            ):
                self.path.pop(0)
                return
            current_target.set_texture(0)
            self.angle = (
                math.atan2(
                    self.center_y - current_target.center_y,
                    self.center_x - current_target.center_x,
                )
                * 180
                / math.pi
                + 90
            )
            self.offset_coordinate = current_target.offset_coordinate
            self.cube_coordinate = current_target.cube_coordinate
            self.center_x = current_target.center_x
            self.center_y = current_target.center_y

    def set_path(self, path: List[HexTile]) -> None:
        self.path = path
