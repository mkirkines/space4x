# Installed packages
from typing import List, Tuple, Union

import arcade  # type: ignore

# from arcade.application import View
from arcade.experimental.camera import Camera2D  # type: ignore
from arcade.texture import Texture  # type: ignore

import space4x.constants
import space4x.resources
from space4x.hex_grid import HexGrid, HexTile
from space4x.path_finder import PathFinder
from space4x.popup_menu import PopupMenu
from space4x.spaceship import Spaceship
from space4x.star_field import StarField


# TODO: Make game class, and make Application class "light-weight"
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
        self.scroll_direction = (0, 0)

        arcade.set_background_color(arcade.color.BLACK)

        self.set_mouse_visible(False)

        self.background: Texture = arcade.load_texture(
            space4x.resources.bg_img
        )

        self.hex_grid: HexGrid = HexGrid()
        self.star_field: StarField = StarField(self.hex_grid)
        self.path_finder: PathFinder = PathFinder(self.hex_grid)
        self.last_path: List[HexTile] = []

        self.space_ship: Spaceship = Spaceship(
            hex_grid=self.hex_grid,
            x=7,
            y=5,
        )

        self.popup_menu: Union[None, PopupMenu] = None

    def setup(self) -> None:
        """Performs neccessary setup steps."""
        pass

    def on_draw(self) -> None:
        """Gets called everytime something can be drawn to the screen."""
        self.camera.use()
        self.clear()

        arcade.draw_lrwh_rectangle_textured(
            *self.camera.scroll, *self.screen_size, self.background
        )

        # for hex_tile in self.hex_grid:
        #     x = hex_tile.cube_coordinate.x
        #     y = hex_tile.cube_coordinate.y
        #     z = hex_tile.cube_coordinate.z
        #     x_pos = hex_tile.center_x - 35
        #     y_pos = hex_tile.center_y - 5
        #     arcade.draw_text(
        #         f"({x}, {y}, {z})", x_pos, y_pos, color=arcade.color.WHITE
        #     )

        self.hex_grid.draw()
        self.star_field.draw()
        self.space_ship.draw()
        if self.popup_menu:
            self.popup_menu.draw()
        self.cursor.draw()

    def on_update(self, delta_time: float) -> None:
        """Gets called every delta_time seconds."""

        self.camera._scroll_x += self.scroll_direction[0]
        self.camera._scroll_y += self.scroll_direction[1]
        if self.popup_menu:
            self.popup_menu.update()

        if self.space_ship.path == []:
            if (
                len(
                    collisions := arcade.check_for_collision_with_list(
                        self.cursor, self.hex_grid
                    )
                )
                == 0
            ):
                return
            if collisions[0].has_star():  # type: ignore
                return

            # TODO: seperate path validation into its own function or class
            # Also for for considering range

            # Unmark old path
            for hex_tile in self.last_path:
                hex_tile.set_texture(0)
            # Get new path
            start_hex = self.hex_grid.get_Tile_by_xy(
                x=self.space_ship.offset_coordinate.x,
                y=self.space_ship.offset_coordinate.y,
            )
            path = self.path_finder.a_star(
                start_hex=start_hex,  # type: ignore
                end_hex=collisions[0],  # type: ignore
            )
            # Mark new path
            for hex_tile in path:
                hex_tile.set_texture(1)  # type: ignore
            self.last_path = path

        self.space_ship.update(delta_time=delta_time)
        self.star_field.update(delta_time=delta_time)

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
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.popup_menu:
                if self.popup_menu.process_mouse_click():
                    return
            self.hex_grid.get_Tile_by_xy(  # type: ignore
                self.space_ship.offset_coordinate.x,
                self.space_ship.offset_coordinate.y,
            ).set_texture(0)
            self.space_ship.set_path(self.last_path)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if (
                len(
                    collisions := arcade.check_for_collision_with_list(
                        self.cursor, self.hex_grid
                    )
                )
                == 1
            ):
                if collisions[0].has_star():  # type: ignore
                    star = collisions[0].get_star()  # type: ignore
                    self.popup_menu = PopupMenu(
                        cursor=self.cursor, camera=self.camera, star=star
                    )

    def on_mouse_drag(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        buttons: int,
        modifiers: int,
    ) -> None:
        """Processed mouse drags.

        Args:
            x (float): mouse pos x
            y (float): mouse pos y
            dx (float): delta x
            dy (float): dy
            buttons (int): button id
            modifiers (int): modifier button
        """
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            if self.popup_menu:
                if self.popup_menu.dragged:
                    self.popup_menu.pos_x += int(dx)
                    self.popup_menu.pos_y += int(dy)
        self.cursor.set_position(
            *self.camera.mouse_coordinates_to_world(x, y)
        )

    def on_mouse_release(
        self, x: float, y: float, button: int, modifiers: int
    ):
        """Actions to perform on mouse release

        Args:
            x (float): mouse pos x
            y (float): mouse pos y
            button (int): button clicked
            modifiers (int): modifier button
        """
        if self.popup_menu:
            self.popup_menu.dragged = False

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

        if key == arcade.key.W:
            self.scroll_direction = (
                self.scroll_direction[0],
                self.scroll_direction[1] + space4x.constants.scroll_speed,
            )

        if key == arcade.key.S:
            self.scroll_direction = (
                self.scroll_direction[0],
                self.scroll_direction[1] - space4x.constants.scroll_speed,
            )

        if key == arcade.key.A:
            self.scroll_direction = (
                self.scroll_direction[0] - space4x.constants.scroll_speed,
                self.scroll_direction[1],
            )

        if key == arcade.key.D:
            self.scroll_direction = (
                self.scroll_direction[0] + space4x.constants.scroll_speed,
                self.scroll_direction[1],
            )

        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key: int, _modifiers: int) -> None:
        if key == arcade.key.W:
            self.scroll_direction = (
                self.scroll_direction[0],
                self.scroll_direction[1] - space4x.constants.scroll_speed,
            )

        if key == arcade.key.S:
            self.scroll_direction = (
                self.scroll_direction[0],
                self.scroll_direction[1] + space4x.constants.scroll_speed,
            )

        if key == arcade.key.A:
            self.scroll_direction = (
                self.scroll_direction[0] + space4x.constants.scroll_speed,
                self.scroll_direction[1],
            )

        if key == arcade.key.D:
            self.scroll_direction = (
                self.scroll_direction[0] - space4x.constants.scroll_speed,
                self.scroll_direction[1],
            )
