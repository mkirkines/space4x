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
