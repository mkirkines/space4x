from typing import Iterator

import arcade

import space4x.constants
import space4x.resources


class HexTile(arcade.Sprite):
    def __init__(self, id_x: int, id_y: int) -> None:
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
        self.center_y = self.id_y * (
            space4x.constants.hex_tile_height
            - (
                space4x.constants.hex_grid_margin_y
                + space4x.constants.hex_grid_correction_y
            )
        )


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
