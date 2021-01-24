import arcade  # type: ignore
from arcade.experimental.camera import Camera2D  # type: ignore

import space4x.constants
import space4x.resources
from space4x.star import Star


class PopupMenu(arcade.SpriteList):
    """A popup menu displaying information about and options on star
    systems."""

    def __init__(
        self, cursor: arcade.Sprite, camera: Camera2D, star: Star
    ) -> None:
        """Initializes a popup menu for a star.

        Args:
            cursor (arcade.Sprite): Contains the position of the mouse.
                                    Necessary for handling user input.
            camera (Camera2D): Contains the current world scroll.
                               Necessary for positioning.
            star (Star): The star, of which the information will be displayed.
        """
        super().__init__()
        # get cursor
        self.cursor = cursor
        # load camera
        self.camera = camera
        # load star
        self.star = star
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
        self.pos_x = space4x.constants.popup_menu_default_x
        self.pos_y = space4x.constants.popup_menu_default_y
        self._update_positions()
        # append to sprite list (order imported for drawing)
        self.append(self.bg)
        self.append(self.exit_button)

    def draw(self) -> None:  # type: ignore
        """Draws the popup menu."""
        super().draw()
        self.draw_star_status()

    def update(self) -> None:
        """Updates the popup menu."""
        super().update()
        self._update_positions()

    def _update_positions(self) -> None:
        """Updates the positions of the menu elements."""
        # TODO: find better way for positioning
        self.bg.set_position(
            center_x=self.camera.scroll_x + self.pos_x,
            center_y=self.camera.scroll_y + self.pos_y,
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

    def process_mouse_click(self) -> bool:
        """Processes the mouseclicks targeting the popup menu."""
        if arcade.check_for_collision(self.cursor, self.bg):
            if arcade.check_for_collision(self.cursor, self.exit_button):
                while len(self.sprite_list) > 0:
                    self.sprite_list.pop()
                del self
            return True
        else:
            return False

    def draw_star_status(self) -> None:
        """Draws the status of the star to the popup."""
        # Draw star name
        arcade.draw_text(
            text="Name: " + self.star.name,
            start_x=self.bg.center_x - self.bg.width // 2 + 20,
            start_y=self.bg.center_y + self.bg.height // 2 - 50,
            color=(54, 94, 54),
            font_size=30,
        )
        # Draw amount of iron ore
        arcade.draw_text(
            text="Iron ore: " + str(self.star.amount_iron_ore) + " MT",
            start_x=self.bg.center_x - self.bg.width // 2 + 20,
            start_y=self.bg.center_y + self.bg.height // 2 - 100,
            color=(54, 94, 54),
            font_size=30,
        )
        # Draw amount of biomass
        arcade.draw_text(
            text="Biomass: " + str(self.star.amount_bio_mass) + " MT",
            start_x=self.bg.center_x - self.bg.width // 2 + 20,
            start_y=self.bg.center_y + self.bg.height // 2 - 150,
            color=(54, 94, 54),
            font_size=30,
        )
