import arcade  # type: ignore
import numpy as np  # type: ignore

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

        self.name: str = "".join(
            [chr(i) for i in np.random.randint(65, 91, 5)]
        )
        self.amount_iron_ore: int = np.random.randint(0, 1e4)
        self.amount_bio_mass: int = np.random.randint(0, 1e4)

        self.timer: float = 0

    def update(self, delta_time: float = 1 / 60) -> None:
        if not self.timer >= 1:
            self.timer += delta_time
            return
        if self.amount_iron_ore > 0:
            self.amount_iron_ore -= 1
        if self.amount_bio_mass > 0:
            self.amount_bio_mass -= 1
        self.timer = 0
