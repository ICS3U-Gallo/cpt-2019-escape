import arcade
import settings
import os
import random

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

WIDTH = 800
HEIGHT = 600
TITLE = "A Simple Jumping Game"

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.5

VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

class Chapter3View(arcade.View):
    def __init__(self):
        super().__init__()  # Initializer

        # Set Background Colour
        arcade.set_background_color(arcade.color.BLACK)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite List
        self.wall_list = None
        self.enemy_list = None
        self.player_list = None
        self.key_list = None

        # Player Setup
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False

        self.half_width = WIDTH / 2
        self.half_height = HEIGHT / 2

    def on_show(self):
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()

        # Draw the ground
        for x in range(0, WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/planetMid.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        # Draw the two platforms
        for x in range(SPRITE_SIZE * 3, SPRITE_SIZE * 5, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/planet.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE * 4
            wall.left = x
            self.wall_list.append(wall)

        for x in range(SPRITE_SIZE * 3, SPRITE_SIZE * 5, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/planetMid.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE * 3
            wall.left = x + 250
            self.wall_list.append(wall)

        # Draw the crates
        for x in range(0, WIDTH, SPRITE_SIZE * 5):
            wall = arcade.Sprite(":resources:images/items/ladderMid.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE
            wall.left = x
            self.wall_list.append(wall)

        # -- Draw an enemy on the ground
        enemy = arcade.Sprite(":resources:images/enemies/slimeBlock.png", SPRITE_SCALING)

        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 2

        # Set enemy initial speed
        enemy.change_x = 2
        self.enemy_list.append(enemy)

        # -- Draw an enemy on the ground
        enemy = arcade.Sprite(":resources:images/enemies/slimeBlock.png", SPRITE_SCALING)

        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 8

        # Set enemy initial speed
        enemy.change_x = 2
        self.enemy_list.append(enemy)

        # -- Draw a enemy on the first platform
        enemy = arcade.Sprite(":resources:images/enemies/slimeBlock.png", SPRITE_SCALING)

        enemy.bottom = SPRITE_SIZE * 5
        enemy.left = SPRITE_SIZE * 4

        # Set boundaries on the left/right the enemy can't cross
        enemy.boundary_right = SPRITE_SIZE * 5
        enemy.boundary_left = SPRITE_SIZE * 3
        enemy.change_x = 1
        self.enemy_list.append(enemy)

        # -- Draw a enemy on the second platform
        enemy = arcade.Sprite(":resources:images/enemies/fly.png", SPRITE_SCALING)

        enemy.bottom = SPRITE_SIZE * 5
        enemy.left = SPRITE_SIZE * 7

        # Set boundaries on the left/right the enemy can't cross
        enemy.boundary_right = SPRITE_SIZE * 10
        enemy.boundary_left = SPRITE_SIZE * 5
        enemy.change_x = 3
        self.enemy_list.append(enemy)

        # Draw Key
        key = arcade.Sprite(":resources:images/items/keyYellow.png", SPRITE_SCALING)

        key.bottom = SPRITE_SIZE
        key.left = x + 90
        self.key_list.append(key)

        # -- Set up the player
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/robot/robot_idle.png", SPRITE_SCALING)
        self.player_list.append(self.player_sprite)

        # Starting position of the player
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()  # keep as first line

        # Draw everything below here.
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.key_list.draw()

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

            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit a worm. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over = True
                retry = RetryView(self)
                self.window.show_view(retry)

            if len(arcade.check_for_collision_with_list(self.player_sprite, self.key_list)) > 0:
                winner = WinnerView(self)
                self.window.show_view(winner)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.ORANGE + (200,))

        arcade.draw_text("PAUSED", WIDTH / 2, HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         WIDTH / 2,
                         HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         WIDTH / 2,
                         HEIGHT / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            arcade.set_background_color(arcade.color.BLACK)
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = Chapter3View()
            self.window.show_view(game)



class WinnerView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.LEMON_MERINGUE)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("WINNER! YOU GOT THE KEY FOR THE AMMUNITION TANK!", WIDTH / 2, HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

        arcade.draw_text("Press Enter to Go to Next Level",
                         WIDTH / 2,
                         HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:  # reset game
            self.director.next_view()


class RetryView(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.FLAME)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("DEFEAT", WIDTH / 2, HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        arcade.draw_text("Press Spacebar to Retry",
                         WIDTH / 2,
                         HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:  # reset game
            game = Chapter4View()
            self.window.show_view(game)


def main():
    from utils import FakeDirector

    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    game = Chapter3View()
    game.director = FakeDirector(close_on_next_view=True)
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
