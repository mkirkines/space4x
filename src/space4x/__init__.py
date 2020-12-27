# Integrated packages
# TODO: Fill

# Installed packages
import arcade

# Own packages
from space4x.app import Application


def main() -> None:
    screen_width, screen_height = [
        int(0.8 * dim) for dim in arcade.get_display_size()
    ]
    app = Application(
        width=screen_width, height=screen_height, title="Space4X"
    )
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()
