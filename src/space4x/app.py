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

        self.example_image: Texture = arcade.load_texture(
            ":resources:images/tiles/boxCrate_double.png"
        )

    def setup(self) -> None:
        """Performs neccessary setup steps."""
        pass

    def on_draw(self):
        """Gets called everytime something can be drawn to the screen."""
        self.camera.use()
        self.clear()

        for x in range(64, 1568, 128):
            y = 64
            width = 128
            height = 128
            arcade.draw_texture_rectangle(
                center_x=x,
                center_y=y,
                width=width,
                height=height,
                texture=self.example_image,
            )
            arcade.draw_text(f"{x},{y}", x, y, color=arcade.color.WHITE)
        arcade.draw_line(
            start_x=0,
            start_y=0,
            end_x=self.screen_size[0],
            end_y=self.screen_size[1],
            color=arcade.color.WHITE,
        )

        world_pos = self.camera.mouse_coordinates_to_world(*self.mouse_pos)
        arcade.draw_circle_filled(
            *world_pos, radius=10, color=arcade.color.WHITE
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
