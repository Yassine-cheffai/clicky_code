"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""

import arcade

WINDOW_WIDTH = int(720 / 2)
WINDOW_HEIGHT = int(1280 / 2)
WINDOW_TITLE = "90s space game"
PLAYER_SPEED = 50


class AnimatedSpaceship(arcade.Sprite):

  def __init__(self, scale=1.0):
    super().__init__(scale=scale)

    # 1. Load your sequence of flame animation frames
    self.frames = [
        arcade.load_texture("assets/spaceship/spaceship1.png"),
        arcade.load_texture("assets/spaceship/spaceship2.png"),
    ]

    self.current_frame = 0
    self.time_accumulator = 0.0
    self.animation_speed = 0.05  # Lower = faster flicker (seconds per frame)

    # Set the initial texture
    self.texture = self.frames[0]

  def update_animation(self, delta_time: float = 1 / 60):
    # Accumulate time
    self.time_accumulator += delta_time

    # Switch frame when threshold is reached
    if self.time_accumulator >= self.animation_speed:
      self.time_accumulator = 0.0
      self.current_frame = (self.current_frame + 1) % len(self.frames)
      self.texture = self.frames[self.current_frame]


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_image_path = "assets/background.jpeg"
        self.background_texture = None

        self.player = None
        self.player_list = None

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.setup()

    def setup(self):

        self.background_texture = arcade.load_texture(self.background_image_path)

        self.player_list = arcade.SpriteList()

        # self.player = arcade.Sprite(
        #     "assets/spaceship.png",
        #     scale=0.17,
        #     center_x=WINDOW_WIDTH / 2,
        #     center_y=WINDOW_HEIGHT / 2,
        # )
        self.player = AnimatedSpaceship(scale=0.17)
        self.player.center_x=WINDOW_WIDTH / 2
        self.player.center_y=WINDOW_HEIGHT / 2
        self.player_list.append(self.player)

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        arcade.draw_texture_rect(
            self.background_texture, arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        # Call draw() on all your sprite lists below
        if self.player_list:
            self.player_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Work out direction from held keys
        dx = self.right - self.left
        dy = self.up - self.down

        if self.player:
            self.player.center_x += dx * PLAYER_SPEED * delta_time
            self.player.center_y += dy * PLAYER_SPEED * delta_time

            # Keep the player inside the window
            player_half_width = self.player.width / 2
            player_half_height = self.player.height / 2

            self.player.center_x = max(
                player_half_width,
                min(WINDOW_WIDTH - player_half_width, self.player.center_x),
            )
            self.player.center_y = max(
                player_half_height,
                min(WINDOW_HEIGHT - player_half_height, self.player.center_y),
            )
            self.player.update_animation(delta_time)

    def on_key_press(self, key, key_modifiers):  # type: ignore
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.LEFT:
            self.left = True
        elif key == arcade.key.RIGHT:
            self.right = True
        elif key == arcade.key.UP:
            self.up = True
        elif key == arcade.key.DOWN:
            self.down = True

    def on_key_release(self, key, key_modifiers):  # type: ignore
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT:
            self.left = False
        elif key == arcade.key.RIGHT:
            self.right = False
        elif key == arcade.key.UP:
            self.up = False
        elif key == arcade.key.DOWN:
            self.down = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):  # type: ignore
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):  # type: ignore
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):  # type: ignore
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
