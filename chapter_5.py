from platform import system
import arcade
import settings
import typing
import pyglet
import random
import os

x = 100
y = 100
SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "omae wa mou shinderu nani"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 250

RIGHT_MARGIN = 150

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.5

class Chapter5View(arcade.View):
    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.

        # Sprite lists
        self.wall_list = None
        self.enemy_list = None
        self.player_list = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False
    def on_show(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Draw the walls on the bottom
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("images/temp.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        for x in range(SPRITE_SIZE * 16, SPRITE_SIZE * 31, SPRITE_SIZE):
            wall = arcade.Sprite("images/temp.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        for x in range(SPRITE_SIZE * 34, SPRITE_SIZE * 41, SPRITE_SIZE):
            wall = arcade.Sprite("images/temp.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        # Draw the platform
        for x in range(SPRITE_SIZE * 3, SPRITE_SIZE * 8, SPRITE_SIZE):
            wall = arcade.Sprite("images/temp.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE * 3
            wall.left = x
            self.wall_list.append(wall)


        # Draw the crates
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE * 5):
            wall = arcade.Sprite("images/temp.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE
            wall.left = x
            self.wall_list.append(wall)

        wall = arcade.Sprite("images/temp.png", SPRITE_SCALING)

        wall.bottom = SPRITE_SIZE
        wall.left = SPRITE_SIZE*16
        self.wall_list.append(wall)


        # -- Draw an enemy on the ground
        enemy = arcade.Sprite("images/temp.png", SPRITE_SCALING)

        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 17

        # Set enemy initial speed
        enemy.change_x = 10
        enemy.boundary_right = SPRITE_SIZE * 31
        enemy.boundary_left = SPRITE_SIZE * 16
        self.enemy_list.append(enemy)

        enemy = arcade.Sprite("images/temp.png", SPRITE_SCALING)

        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 2

        # Set enemy initial speed
        enemy.change_x = 2
        self.enemy_list.append(enemy)

        # -- Draw a enemy on the platform
        enemy = arcade.Sprite("images/temp.png", SPRITE_SCALING)

        enemy.bottom = SPRITE_SIZE * 4
        enemy.left = SPRITE_SIZE * 4

        # Set boundaries on the left/right the enemy can't cross
        enemy.boundary_right = SPRITE_SIZE * 8
        enemy.boundary_left = SPRITE_SIZE * 3
        enemy.change_x = 2
        self.enemy_list.append(enemy)


        # -- Set up the player
        self.player_sprite = arcade.Sprite("images/test.png",SPRITE_SCALING/2)
        self.player_list.append(self.player_sprite)

        # Starting position of the player
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,self.wall_list,gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)


    def on_draw(self):
        """
                Render the screen.
                """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        # self.director.next_view()


    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Update the player based on the physics engine
        if not self.game_over:
            # Move the enemies
            self.enemy_list.update()

            # Check each enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                # If the enemy hit the left boundary, reverse
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            # --- Manage Scrolling ---

                # Keep track of if we changed the boundary. We don't want to call the
                # set_viewport command if we didn't change the view port.
            changed = False
                    # Scroll leftd
            left_boundary = self.view_left + VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundary:
                self.view_left -= left_boundary - self.player_sprite.left
                changed = True

                # Scroll right
            right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed = True
            if changed:
                arcade.set_viewport(self.view_left,SCREEN_WIDTH + self.view_left - 1,self.view_bottom,SCREEN_HEIGHT + self.view_bottom - 1)


            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit a worm. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over = True

class Sound:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.player = pyglet.media.load(file_name)

    def play(self):
        if self.player.is_queued:
            player = pyglet.media.load(self.file_name)
            player.play()
        else:
            self.player.play()


class PlaysoundException(Exception):
    pass


def text(char, line):
    arcade.draw_text(line, 20, 20, arcade.color.WHITE, font_size=20, anchor_x="center")


def _load_sound_library():
    """
    Special code for Windows so we grab the proper avbin from our directory.
    Otherwise hope the correct package is installed.
    """

    # lazy loading
    if not _load_sound_library._sound_library_loaded:
        _load_sound_library._sound_library_loaded = True
    else:
        return

    import pyglet_ffmpeg2
    pyglet_ffmpeg2.load_ffmpeg()


# Initialize static function variable
_load_sound_library._sound_library_loaded = False


def load_sound(file_name: str):
    """
    Load a sound. Support for .wav files. If ffmpeg is available, will work
    with ogg and mp3 as well.
    :param str file_name: Name of the sound file to load.
    :returns: Sound object
    :rtype: Sound
    """

    try:
        sound = Sound(file_name)
        return sound
    except Exception as e:
        print("Unable to load {str}.", e)
        return None


def play_sound(sound: Sound):
    """
    Play a sound.
    :param Sound sound: Sound loaded by load_sound. Do NOT use a string here for the filename.
    """
    if sound is None:
        print("Unable to play sound, no data passed in.")
    elif isinstance(sound, str):
        raise Exception(
            "Error, passed in a string as a sound. Make sure to use load_sound first, and use that result in play_sound.")
    try:
        sound.play()
    except Exception as e:
        print("Error playing sound.", e)


def stop_sound(sound: pyglet.media.Source):
    """
    Stop a sound that is currently playing.
    :param sound:
    """
    sound.pause()


def create_image(texture, x, y, wid, ht):
    # creats an image
    # try:
    image = arcade.load_texture(texture, mirrored=False, scale=0.5)
    arcade.draw_xywh_rectangle_textured(x, y, wid, ht, image, 0, 255, 1, 1)


# except:
#    print('nyanpasu')


_load_sound_library()
if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.
    You can ignore this whole section. Keep it at the bottom
    of your code.
    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector

    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = Chapter5View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()