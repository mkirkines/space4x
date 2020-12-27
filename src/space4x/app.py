# Installed packages
from typing import Tuple

import arcade

# from arcade.application import View
from arcade.experimental.camera import Camera2D
from arcade.texture import Texture


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
        self.mouse_pos = 0, 0

        arcade.set_background_color(arcade.color.BLACK)

        self.set_mouse_visible(False)

        self.hex: Texture = arcade.load_texture("resources/hex.png")
        self.background: Texture = arcade.load_texture(
            "resources/space_bg.png"
        )

    def setup(self) -> None:
        """Performs neccessary setup steps."""
        pass

    def on_draw(self):
        """Gets called everytime something can be drawn to the screen."""
        self.camera.use()
        self.clear()

        arcade.draw_lrwh_rectangle_textured(
            0, 0, *self.screen_size, self.background
        )

        hex_width = 100
        hex_height = 116
        margin_x = 4
        margin_y = 4
        correction_x = 2
        correction_y = 21
        for x in range(0, 16):
            for y in range(0, 16):
                y_pos = y * (hex_height - (margin_y + correction_y))
                if y % 2 == 0:
                    x_pos = (
                        x * (hex_width + margin_x)
                        + hex_width // 2
                        + correction_x
                    )
                    arcade.draw_scaled_texture_rectangle(
                        center_x=x_pos,
                        center_y=y_pos,
                        texture=self.hex,
                        scale=0.25,
                    )
                else:
                    x_pos = x * (hex_width + margin_x)
                    arcade.draw_scaled_texture_rectangle(
                        center_x=x_pos,
                        center_y=y_pos,
                        texture=self.hex,
                        scale=0.25,
                    )
                arcade.draw_text(
                    f"({x}, {y})", x_pos, y_pos, color=arcade.color.WHITE
                )

        world_pos = self.camera.mouse_coordinates_to_world(*self.mouse_pos)
        arcade.draw_circle_filled(
            *world_pos, radius=5, color=arcade.color.WHITE
        )

    def on_update(self, delta_time: float):
        """Gets called every delta_time seconds."""
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """Gets called when the mouse is moved."""
        self.mouse_pos = x, y

    def on_key_press(self, key, _modifiers):
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
