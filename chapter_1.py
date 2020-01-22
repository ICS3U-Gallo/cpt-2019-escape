import arcade

import settings

WIDTH = 500
HEIGHT = 500

LEVEL = [
    "X P XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X   XXXXXXX                            X",
    "X  XXXXXXX  XX  XX  XX XXXXXXX   XXXX  X",
    "X       XX  XXXXXX  X XXXXXXXX   XXXX  X",
    "X        X  XXX        XXXXXXX   XXXX  X",
    "XXXXXX  XX  XXX        XXXXXXX   XXXX  X",
    "XXXXXX  XX  XXXXXX  XX XXXXXXX   XXXX  X",
    "XXXXXX  XX  XXXXXX  XX XXXXXXX   XXXX  X",
    "XXXXXX  XX  XXXXXX  XX XXXXXXX   XXXX  X",
    "XXXXXX  XX  XXXXXX  XX XXXXXXX   XXXX  X",
    "XXXXXX  XX  XXXXXX  XX XXXXXXX   XXXX  X",
    "XXXXXX  XX  XXXXXX  XX XXXXXXX   XXXX  X",
    "XXXXXX        XXXX               XXXX  X",
    "X  XXX        XXXX  XXXXXXX  XXXXXXXX  X",
    "X  XXX  XXXXXXXXXXX   XXXXX  XXXXXXXX  X",
    "X         XXXXXXXXXX  XXXXX  XXXXXXXX  X",
    "X      X         XXX         XXXXXXXX  X",
    "XX XX  XXXXXX   XXXXX   XXXXXXXXXXXXX  X",
    "X  XXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXX  X",
    "X X  XXXXXXXXXX                  XXXX  X",
    "X X  X                  XXXXXXX  XXXX  X",
    "X XX  X     XXXXXXXXX  XXXXXXXX  XXXX  X",
    "X      XXX  XXXXXXXXX  XXXX      XXXX  X",
    "XXXXX  XXX  X           XXX  XXXXXXXX  X",
    "XX   XXX    X           XXXX  XXXXXXX  X",
    "XX   XX    XXXXXXX  X  XXXXX     XXXX  X",
    "XX           XXXX  XXXXXXXXX    XXXXX  X",
    "XXXXX XXXXXXXXXXXX      XXXXXXXXXXXXX  X",
    "XXXX   X                         XXXX  X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX"
]


class MyMaze(arcade.View):
    def __init__(self):
        super().__init__()
        self.director = None
        arcade.set_background_color(arcade.color.BLACK)
        # self.set_location(400, 200)

        self.player_x = 40
        self.player_y = 590
        self.speed = 1

        self.playerRight = False
        self.playerLeft = False
        self.playerUp = False
        self.playerDown = False

        self.sprite_player = arcade.Sprite(center_x=self.player_x, center_y=self.player_y)
        self.sprite_player.texture = arcade.make_soft_square_texture(16, arcade.color.WHITE, outer_alpha=255)

        self.spriteList = arcade.SpriteList()
        for y in range(len(LEVEL)):
            for x in range(len(LEVEL[y])):
                # Get the Character at each x, y coordinate
                # NOTE the order of the y and x in the next line
                character = LEVEL[y][x]
                # Calculate the screen x, y coordinates
                screen_x = 10 + (x * 20)
                screen_y = 590 - (y * 20)
                if character == "X":
                    self.sprite2 = arcade.Sprite(center_x=screen_x, center_y=screen_y)
                    self.sprite2.texture = arcade.make_soft_square_texture(20, arcade.color.RED, outer_alpha=255)
                    self.spriteList.append(self.sprite2)

    def on_draw(self):
        arcade.start_render()
        if self.player_y < 1:
            arcade.draw_text("MISSION ACCOMPLISHED!", 225, 300, arcade.color.WHITE, 28)
        elif self.player_y > 590:
            self.player_x = 40
            self.player_y = 590
            self.sprite_player.set_position(center_x=self.player_x, center_y=self.player_y)
            self.spriteList.draw()
            self.sprite_player.draw()
        else:
            self.spriteList.draw()
            self.sprite_player.set_position(center_x=self.player_x, center_y=self.player_y)
            self.sprite_player.draw()

    def on_update(self, delta_time):
        # used if here instead of elif so that if both keys are pressed, the player does not move anywhere
        if self.playerRight:
            if not self.sprite_player.collides_with_list(self.spriteList):
                self.player_x = self.player_x + self.speed
            if self.player_y < 1:
                self.director.next_view()

        if self.playerLeft:
            if not self.sprite_player.collides_with_list(self.spriteList):
                self.player_x = self.player_x - self.speed

        if self.playerUp:
            if not self.sprite_player.collides_with_list(self.spriteList):
                self.player_y = self.player_y + self.speed

        if self.playerDown:
            if not self.sprite_player.collides_with_list(self.spriteList):
                self.player_y = self.player_y - self.speed


    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.playerRight = True
        if key == arcade.key.LEFT:
            self.playerLeft = True
        if key == arcade.key.UP:
            self.playerUp = True
        if key == arcade.key.DOWN:
            self.playerDown = True

            
    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            if self.sprite_player.collides_with_list(self.spriteList):
                self.player_x = self.player_x - self.speed
            self.playerRight = False
        if key == arcade.key.LEFT:
            if self.sprite_player.collides_with_list(self.spriteList):
                self.player_x = self.player_x + self.speed
            self.playerLeft = False
        if key == arcade.key.UP:
            if self.sprite_player.collides_with_list(self.spriteList):
                self.player_y = self.player_y - self.speed
            self.playerUp = False
        if key == arcade.key.DOWN:
            if self.sprite_player.collides_with_list(self.spriteList):
                self.player_y = self.player_y + self.speed
            self.playerDown = False


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
    my_view = MyMaze()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
