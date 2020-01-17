import random
import arcade

WIDTH = 1200
HEIGHT = 600
MOVEMENT_SPEED = 10


class MyCollectCure (arcade.View):
    def __init__(self):
        super().__init__()

        self.wall_list = arcade.SpriteList()
        self.cure_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.virus_list = arcade.SpriteList()

        self.score = 0
        self.total_time = 0.0
        self.lives = 3

        arcade.set_background_color(arcade.color.BLACK)

        wall_texture = arcade.make_soft_square_texture(70, arcade.color.BLACK, outer_alpha=255)

       # Walls
        for x in range(32, WIDTH, 64):
            wall = arcade.Sprite()
            wall.center_x = x
            wall.center_y = 32
            wall.texture = wall_texture
            self.wall_list.append(wall)

            wall = arcade.Sprite()
            wall.center_x = x
            wall.center_y = HEIGHT - 32
            wall.texture = wall_texture
            self.wall_list.append(wall)

        for y in range(96, HEIGHT, 64):
            wall = arcade.Sprite()
            wall.center_x = 32
            wall.center_y = y
            wall.texture = wall_texture
            self.wall_list.append(wall)

            wall = arcade.Sprite()
            wall.center_x = WIDTH - 32
            wall.center_y = y
            wall.texture = wall_texture
            self.wall_list.append(wall)

        #Sprites
        virus_texture = arcade.make_soft_square_texture(30, arcade.color.RED, outer_alpha=255)

        for i in range(5):
            virus = arcade.Sprite()
            virus.texture = virus_texture
            virus.center_x = random.randrange(100, 900)
            virus.center_y = random.randrange(100, 500)
            while virus.change_x == 0 and virus.change_y == 0:
                virus.change_x = random.randrange(-2, 2)
                virus.change_y = random.randrange(-2, 2)

            self.virus_list.append(virus)

        cure_texture = arcade.make_soft_square_texture(40, arcade.color.NAVY_BLUE, outer_alpha=255)

        for i in range(30):
            cure = arcade.Sprite()
            cure.texture = cure_texture
            cure.center_x = random.randrange(100, 900)
            cure.center_y = random.randrange(100, 500)
            while cure.change_x == 0 and cure.change_y == 0:
                cure.change_x = random.randrange(-3, 3)
                cure.change_y = random.randrange(-3, 3)

            self.cure_list.append(cure)

        powerup_texture = arcade.make_soft_square_texture(30, arcade.color.GOLD, outer_alpha=255)

        for i in range(2):
            powerup = arcade.Sprite(center_x=1000, center_y=1200)
            powerup.texture = powerup_texture

            self.powerup_list.append(powerup)

        self.user = arcade.Sprite(center_x=100, center_y=90)
        self.user.texture = arcade.make_soft_circle_texture(30, arcade.color.WHITE, outer_alpha=255)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

        self.user.draw()
        self.virus_list.draw()
        self.cure_list.draw()
        self.powerup_list.draw()
        self.wall_list.draw()

        #tracks lives and cures left
        cure_count = (f"Cures Collected: {self.score}")
        arcade.draw_text(cure_count, (WIDTH - 260), (HEIGHT - 40), arcade.color.WHITE, 20)

        life_count = (f"Lives: {self.lives}")
        arcade.draw_text(life_count, 30, (HEIGHT - 40), arcade.color.WHITE, 20)

        if len(self.cure_list) == 0:
            win_text = "You have received the cure! "
            arcade.draw_text(win_text, (WIDTH/3-50), (HEIGHT- 200), arcade.color.WHITE, 25)
            arcade.draw_rectangle_filled(WIDTH/2, HEIGHT/2, 50, arcade.color.GREEN, 128)

        if self.lives <= 0:
            lose_text = "You failed in curing the viruses."
            arcade.draw_text(lose_text, (WIDTH/3-50), (HEIGHT-200), arcade.color.WHITE, 25)

        #timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"

        arcade.draw_text(output, (WIDTH - 750), (HEIGHT - 40), arcade.color.WHITE, 30)

    def on_update(self, delta_time):
        # checks if sprites collide with wall sprite
        for virus in self.virus_list:

            virus.center_x += virus.change_x
            walls_hit = arcade.check_for_collision_with_list(virus, self.wall_list)
            for wall in walls_hit:
                if virus.change_x > 0:
                    virus.right = wall.left
                elif virus.change_x < 0:
                    virus.left = wall.right
            if len(walls_hit) > 0:
                virus.change_x *= -1

            virus.center_y += virus.change_y
            walls_hit = arcade.check_for_collision_with_list(virus, self.wall_list)
            for wall in walls_hit:
                if virus.change_y > 0:
                    virus.top = wall.bottom
                elif virus.change_y < 0:
                    virus.bottom = wall.top
            if len(walls_hit) > 0:
                virus.change_y *= -1

        for cure in self.cure_list:

            cure.center_x += cure.change_x
            walls_hit = arcade.check_for_collision_with_list(cure, self.wall_list)
            for wall in walls_hit:
                if cure.change_x > 0:
                    cure.right = wall.left
                elif cure.change_x < 0:
                    cure.left = wall.right
            if len(walls_hit) > 0:
                cure.change_x *= -1

            cure.center_y += cure.change_y
            walls_hit = arcade.check_for_collision_with_list(cure, self.wall_list)
            for wall in walls_hit:
                if cure.change_y > 0:
                    cure.top = wall.bottom
                elif cure.change_y < 0:
                    cure.bottom = wall.top
            if len(walls_hit) > 0:
                cure.change_y *= -1

        for powerup in self.powerup_list:

            powerup.center_x += powerup.change_x
            walls_hit = arcade.check_for_collision_with_list(powerup, self.wall_list)
            for wall in walls_hit:
                if powerup.change_x > 0:
                    powerup.right = wall.left
                elif powerup.change_x < 0:
                    powerup.left = wall.right
            if len(walls_hit) > 0:
                powerup.change_x *= -1

            powerup.center_y += powerup.change_y
            walls_hit = arcade.check_for_collision_with_list(powerup, self.wall_list)
            for wall in walls_hit:
                if powerup.change_y > 0:
                    powerup.top = wall.bottom
                elif powerup.change_y < 0:
                    powerup.bottom = wall.top
            if len(walls_hit) > 0:
                powerup.change_y *= -1

            self.cure_list.update()
            self.powerup_list.update()
            self.virus_list.update()

            # list of all sprites that collided with the player.
            virus_hit_list = arcade.check_for_collision_with_list(self.user, self.virus_list)
            cure_hit_list = arcade.check_for_collision_with_list(self.user, self.cure_list)
            powerup_hit_list = arcade.check_for_collision_with_list(self.user, self.powerup_list)

            for virus in virus_hit_list:
                virus.remove_from_sprite_lists()
                self.score -= 2
                self.lives -= 1

            for cure in cure_hit_list:
                cure.remove_from_sprite_lists()
                self.score += 1

                # Calculate speed based on the keys pressed
        self.user.change_x = 0
        self.user.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.user.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.user.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.user.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.user.change_x = MOVEMENT_SPEED

        # To move the user sprite
        self.user.update()
        self.total_time += delta_time

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    window = MyGame(WIDTH, HEIGHT, "Collect the Cure")
    arcade.run()

if __name__ == "__main__":
    main()
