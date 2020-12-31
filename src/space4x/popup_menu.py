import arcade  # type: ignore
from arcade.experimental.camera import Camera2D  # type: ignore

import space4x.constants
import space4x.resources


class PopupMenu(arcade.SpriteList):
    def __init__(self, cursor: arcade.Sprite, camera: Camera2D) -> None:
        super().__init__()
        # get cursor
        self.cursor = cursor
        # load camera
        self.camera = camera
        # load textures
        self.bg = arcade.Sprite(
            filename=space4x.resources.popup_menu_bg,
            scale=space4x.constants.popup_menu_bg_scale,
        )
        self.exit_button = arcade.Sprite(
            filename=space4x.resources.popup_menu_exit_button,
            scale=space4x.constants.popup_menu_exit_button_scale,
        )
        # set positions
        self._update_positions()
        # append to sprite list (order imported for drawing)
        self.append(self.bg)
        self.append(self.exit_button)

    def update(self):
        super().update()
        self._update_positions()
        if arcade.check_for_collision(self.cursor, self.exit_button):
            for sprite in self:
                self.remove(sprite)
                sprite.kill()
                del sprite
            del self

    def _update_positions(self) -> None:
        self.bg.set_position(
            center_x=self.camera.scroll_x
            + space4x.constants.popup_menu_default_x,
            center_y=self.camera.scroll_y
            + space4x.constants.popup_menu_default_y,
        )
        self.exit_button.set_position(
            center_x=self.bg.center_x
            + self.bg.width // 2
            - self.exit_button.width // 2
            - space4x.constants.popup_menu_exit_button_offset,
            center_y=self.bg.center_y
            + self.bg.height // 2
            - self.exit_button.height // 2
            - space4x.constants.popup_menu_exit_button_offset,
        )
