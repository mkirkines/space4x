import arcade  # type: ignore

import space4x.constants
import space4x.resources


class Star(arcade.Sprite):
    """A basic star class."""

    def __init__(self, center_x: int, center_y: int) -> None:
        """Creates a star at a given (pixel) position.

        Args:
            center_x (int): pixel position x
            center_y (int): pixel position y
        """
        super().__init__(
            filename=space4x.resources.star_img,
            scale=space4x.constants.star_img_scale,
        )
        self.center_x = center_x
        self.center_y = center_y
