from platform import system
import arcade
import settings
import typing
import pyglet
import random
import os
import math

x = 100
y = 100
SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SCALING_LASER = 0.065
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
BULLET_SPEED = 10
story=-1
lines=0
a=0
hp=100

text_line_0=['padoru','100','','line for the main character to saoy','replace this text with actual lines',
             'padoru', '500','','this is a test line lol', 'does this code work ']
text_line_1=['padoru','100','','line for the main character to saoy','replace this text with actual lines',
             'padoru', '500','','this is a test line lol', 'does this code work ']




SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "omae wa mou shinderu nani"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = SCREEN_WIDTH/2

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
        self.bullet_list=None
        self.enemy1_list=None
        self.ebullet_list=None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False
        self.frame_count = 0
    def on_show(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy1_list=arcade.SpriteList()
        self.ebullet_list=arcade.SpriteList()

        # Draw the walls on the bottom
        for x in range(0, 800, SPRITE_SIZE):
            wall = arcade.Sprite("images/grass.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            wall.damage=0
            self.wall_list.append(wall)

        for x in range(SPRITE_SIZE * 16, SPRITE_SIZE * 31, SPRITE_SIZE):
            wall = arcade.Sprite("images/grass.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            wall.damage=0
            self.wall_list.append(wall)

        for x in range(SPRITE_SIZE * 34, SPRITE_SIZE * 41, SPRITE_SIZE):
            wall = arcade.Sprite("images/grass.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            wall.damage=0
            self.wall_list.append(wall)

        for x in range(SPRITE_SIZE * 52, SPRITE_SIZE * 60, SPRITE_SIZE):
            wall = arcade.Sprite("images/grass.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            wall.damage=0
            self.wall_list.append(wall)

        # Draw the platform
        for x in range(SPRITE_SIZE * 3, SPRITE_SIZE * 8, SPRITE_SIZE):
            wall = arcade.Sprite("images/grass.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE * 3
            wall.left = x
            wall.damage=0
            self.wall_list.append(wall)


        # Draw the crates
        for x in range(0, 800, SPRITE_SIZE * 5):
            wall = arcade.Sprite("images/wood.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE
            wall.left = x
            wall.damage=0
            self.wall_list.append(wall)

        for i in range(10):
            wall = arcade.Sprite("images/wood.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE*(i+1)
            wall.left = SPRITE_SIZE*16
            wall.damage=1
            self.wall_list.append(wall)


        # -- Draw an enemy on the ground


        enemy = arcade.Sprite("images/virus_red.png", SPRITE_SCALING/2)


        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 17

        # Set enemy initial speed
        enemy.change_x = 10
        enemy.boundary_right = SPRITE_SIZE * 31
        enemy.boundary_left = SPRITE_SIZE * 16
        enemy.damage = 0
        self.enemy_list.append(enemy)



        enemy = arcade.Sprite("images/virus_blue.png", SPRITE_SCALING/2)


        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 2

        # Set enemy initial speed
        enemy.change_x = 2
        enemy.damage=1
        self.enemy_list.append(enemy)

        # -- Draw a enemy on the platform


        enemy = arcade.Sprite("images/virus_blue.png", SPRITE_SCALING/2)


        enemy.bottom = SPRITE_SIZE * 4
        enemy.left = SPRITE_SIZE * 4

        # Set boundaries on the left/right the enemy can't cross
        enemy.boundary_right = SPRITE_SIZE * 8
        enemy.boundary_left = SPRITE_SIZE * 3
        enemy.change_x = 2
        enemy.damage=1
        self.enemy_list.append(enemy)


        # Add top-left enemy ship
        enemy = arcade.Sprite("images/virus_red.png", 0.5)
        enemy.center_x = SPRITE_SIZE*50
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy1_list.append(enemy)

        # Add top-right enemy ship
        enemy = arcade.Sprite("images/virus_red.png", 0.5)
        enemy.center_x = SPRITE_SIZE*62
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy1_list.append(enemy)


        # -- Set up the player

        self.player_sprite = arcade.Sprite("images/test.png",SPRITE_SCALING)

        self.player_list.append(self.player_sprite)

        # Starting position of the player
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,self.wall_list,gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color((188, 212, 230)	)


    def on_draw(self):
        global story
        global lines
        global text_line_0
        global text_line_1
        global a
        """
                Render the screen.
                """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        create_image('images/mahou.png', SPRITE_SIZE*35, SPRITE_SIZE, SPRITE_SIZE*4, SPRITE_SIZE*4)
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.enemy1_list.draw()
        self.ebullet_list.draw()
        arcade.draw_text('hp: '+str(hp), self.player_sprite.center_x-SCREEN_WIDTH/2+10, 10, arcade.color.RED, 20)
        if story==-1:
            music=load_sound('souwnd/bgm_maoudamashii_fantasy11.mp3')
            play_sound(music)
            story=0
        elif story==0:
            if len(text_line_0)//5<=lines:
                sound=load_sound("sound/game_swordman-start1.mp3")
                play_sound(sound)
                story=11
                lines=0

            else:

                img_pos=int(text_line_0[lines*5+1])
                #arcade.draw_xywh_rectangle_filled(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,(255, 0, 0, 100)) good for death screen
                arcade.draw_xywh_rectangle_filled(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,(0, 0, 0, 150))

                create_image('images/'+text_line_0[lines*5]+text_line_0[lines*5+2]+'.png', img_pos, 0, 300,450)
                arcade.draw_xywh_rectangle_filled(25,25,SCREEN_WIDTH-50,145,(0, 0, 0, 150))
                arcade.draw_text(text_line_0[lines*5], 150, 130, arcade.color.WHITE, 20)
                for i in range(2):
                    arcade.draw_text(text_line_0[lines*5+i+3], 150, 100-(30*i), arcade.color.WHITE, 20)
        elif story==1:
            if len(text_line_1)//5<=lines:
                sound=load_sound("sound/game_swordman-start1.mp3")
                play_sound(sound)
                story=11
                lines=0
                self.player_sprite.center_x = SPRITE_SIZE*55

            else:

                img_pos=int(text_line_1[lines*5+1])
                #arcade.draw_xywh_rectangle_filled(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,(255, 0, 0, 100)) good for death screen
                arcade.draw_xywh_rectangle_filled(self.player_sprite.center_x-SCREEN_WIDTH/2,0,SCREEN_WIDTH*1.2,SCREEN_HEIGHT,(0, 0, 0, 150))

                create_image('images/'+text_line_1[lines*5]+text_line_1[lines*5+2]+'.png', img_pos+self.player_sprite.center_x, 0, 300,450)
                arcade.draw_xywh_rectangle_filled(self.player_sprite.center_x+25-SCREEN_WIDTH/2,25,SCREEN_WIDTH-50,145,(0, 0, 0, 150))
                arcade.draw_text(text_line_1[lines*5], self.player_sprite.center_x-150-SCREEN_WIDTH/2, 130, arcade.color.WHITE, 20)
                for i in range(2):
                    arcade.draw_text(text_line_1[lines*5+i+3], self.player_sprite.center_x-150, 100-(30*i), arcade.color.WHITE, 20)
        if self.game_over or self.player_sprite.center_y < -11:
            arcade.draw_xywh_rectangle_filled(self.player_sprite.center_x-SCREEN_WIDTH/2,0,SCREEN_WIDTH*2,SCREEN_HEIGHT*2,(255, 0, 0, 100))
            create_image('images/game_over.png', self.player_sprite.center_x-SCREEN_WIDTH/4, 200, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            arcade.draw_text('GAME OVER', self.player_sprite.center_x-128, 150, arcade.color.WHITE, 40)
            if a==0:
                sound=load_sound("sound/game_swordman-faint1.mp3")
                play_sound(sound)
                a+=1

    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
                sound=load_sound("sound/game_swordman-attack1.mp3")
                play_sound(sound)
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

    def on_mouse_press(self, x, y, button, modifiers):
        global lines
        global story
        if story!=11:
            lines+=1
        else:
            bullet = arcade.Sprite("images/padoru.png", SPRITE_SCALING_LASER)

            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            dest_x = x+self.view_left
            dest_y = y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            bullet.angle = math.degrees(angle)
            print(f"Bullet angle: {bullet.angle:.2f}")

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED
            sound=load_sound('sound/game_swordman-attack3.mp3')
            play_sound(sound)

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        global story
        """ Movement and game logic """

        # Update the player based on the physics engine
        if self.player_sprite.center_x>SPRITE_SIZE*35 and self.player_sprite.center_x<SPRITE_SIZE*40:
            story=1

        if not self.game_over and story==11 and self.player_sprite.center_y>-11:
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
        """ Movement and game logic """

        # Call update on all sprites
        self.bullet_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            hit_list2 = arcade.check_for_collision_with_list(bullet, self.enemy_list)


            # If it did, get rid of the bullet
            if len(hit_list) > 0 or len(hit_list2) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for enemy in hit_list2:
                if enemy.damage==1:
                    enemy.remove_from_sprite_lists()
            for wall in hit_list:
                if wall.damage==1:
                    wall.remove_from_sprite_lists()
            #    self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > 1000 or bullet.top < -11 or bullet.right < -2019 or bullet.left > 3100588100:
                bullet.remove_from_sprite_lists()


        self.frame_count += 1
        global hp
        for bullet in self.ebullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            hit_list2 = arcade.check_for_collision_with_list(bullet, self.player_list)



            # If it did, get rid of the bullet
            if len(hit_list) > 0 or len(hit_list2) > 0:
                bullet.remove_from_sprite_lists()
            # For every coin we hit, add to the score and remove the coin
            for player in hit_list2:
                hp-=random.randint(1, 50)
                hit_list2.clear()
            for wall in hit_list:
                if wall.damage==1:
                    wall.remove_from_sprite_lists()
            #    self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > 1000 or bullet.top < -11 or bullet.right < -2019 or bullet.left > 3100588100:
                bullet.remove_from_sprite_lists()
        # Loop through each enemy that we have
        for enemy in self.enemy1_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)-90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite("images/virus_blue.png", SPRITE_SCALING_LASER)
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.ebullet_list.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.ebullet_list:
            if bullet.top < -11:
                bullet.remove_from_sprite_lists()

        self.ebullet_list.update()




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
