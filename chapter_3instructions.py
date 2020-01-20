import arcade

import settings


class InstructionsView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to Chapter 3!\n"
                         "To use the antidote, \n"
                         "you need a key for an ammunition tank to take the viruses out! \n" 
                         "But beware! The virus sent you in a world where its slime and fly minions \n"
                         "WILL KILL YOU IF YOU TOUCH THEM! \n"
                         "Dodge using the up, down, left, right keys and get the key for the tank! \n"
                         "Press the right key to continue", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def on_key_press(self, key, modifiers):
        self.director.next_view()


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
    my_view = InstructionsView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
