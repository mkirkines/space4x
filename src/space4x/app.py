# Installed packages
from typing import Tuple, Union

import arcade  # type: ignore

# from arcade.application import View
from arcade.experimental.camera import Camera2D  # type: ignore
from arcade.texture import Texture  # type: ignore

import space4x.constants
import space4x.resources
from space4x.hex_grid import HexGrid, HexTile
from space4x.path_finder import find_path
from space4x.star_field import StarField


class Application(arcade.Window):
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "Application",
        fullscreen: bool = True,
    ) -> None:
        """Application class. Inherits from arcade.Window.

        Manages different views, like menus, games, highscores, etc.

        Args:
            width : Window width. Defaults to 800.
            height : Window height. Defaults to 600.
            title : Title of the app. Defaults to "Application".
            fullscreen : Toggle fullscreen. Defaults to True.
        """
        super().__init__(
            width=width, height=height, title=title, fullscreen=fullscreen
        )
        self.set_vsync(True)
        self.screen_size: Tuple[int, int] = self.get_size()

        self.camera = Camera2D(
            viewport=(0, 0, self.screen_size[0], self.screen_size[1]),
            projection=(0, self.screen_size[0], 0, self.screen_size[1]),
        )
        self.camera.use()
        self.cursor = arcade.Sprite(
            filename=space4x.resources.cursor_img,
            scale=space4x.constants.mouse_img_scale,
        )

        arcade.set_background_color(arcade.color.BLACK)

        self.set_mouse_visible(False)

        self.background: Texture = arcade.load_texture(
            space4x.resources.bg_img
        )

        self.hex_grid: HexGrid = HexGrid()
        self.star_field: StarField = StarField(self.hex_grid)
        self.focussed_hex: Union[None, HexTile] = None  # type: ignore

    def setup(self) -> None:
        """Performs neccessary setup steps."""
        pass

    def on_draw(self) -> None:
        """Gets called everytime something can be drawn to the screen."""
        self.camera.use()
        self.clear()

        arcade.draw_lrwh_rectangle_textured(
            0, 0, *self.screen_size, self.background
        )

        for hex_tile in self.hex_grid:
            x = hex_tile.cube_coordinate.x
            y = hex_tile.cube_coordinate.y
            z = hex_tile.cube_coordinate.z
            x_pos = hex_tile.center_x - 35
            y_pos = hex_tile.center_y - 5
            arcade.draw_text(
                f"({x}, {y}, {z})", x_pos, y_pos, color=arcade.color.WHITE
            )

        self.hex_grid.draw()
        self.star_field.draw()
        self.cursor.draw()

    def on_update(self, delta_time: float) -> None:
        """Gets called every delta_time seconds."""
        collisions = arcade.check_for_collision_with_list(
            self.cursor, self.hex_grid
        )
        if len(collisions) == 0:
            if self.focussed_hex:
                self.focussed_hex.set_texture(0)
                self.focussed_hex = None
            return
        if not (self.focussed_hex in collisions):
            for hex_tile in collisions:
                if self.focussed_hex:
                    self.focussed_hex.set_texture(0)
                hex_tile.set_texture(1)
                self.focussed_hex = hex_tile  # type: ignore

    def on_mouse_motion(
        self, x: float, y: float, dx: float, dy: float
    ) -> None:
        """Gets called when the mouse is moved."""
        self.cursor.set_position(
            *self.camera.mouse_coordinates_to_world(x, y)
        )

    def on_mouse_press(
        self, x: float, y: float, button: int, modifiers: int
    ) -> None:
        if self.focussed_hex:
            pos_x = self.focussed_hex.offset_coordinate.x
            pos_y = self.focussed_hex.offset_coordinate.y
            path = find_path(0, 0, pos_x, pos_y)
            for pos in path:
                hex_tile = self.hex_grid.get_Tile_by_xy(*pos)
                hex_tile.set_texture(1)  # type: ignore

    def on_key_press(self, key: int, _modifiers: int) -> None:
        """Gets called when a key is pressed."""
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.camera.viewport = (
                0,
                0,
                self.get_size()[0],
                self.get_size()[1],
            )

        if key == arcade.key.ESCAPE:
            arcade.close_window()
