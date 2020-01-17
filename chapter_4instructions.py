import arcade

import settings


class Chapter4Instructions(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        instructions = "Use the WASD keys to move around"
        instructions2 = "Use the mouse to shoot the antidote"
        instructions3 = "You now have to cure the viruses!"
        instructions4 = "Press SPACE to continue"
        arcade.draw_text(instructions3, settings.WIDTH/2, settings.HEIGHT/1.5,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text(instructions, settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text(instructions2, settings.WIDTH/2, settings.HEIGHT/2-50,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text(instructions4, settings.WIDTH/2, settings.HEIGHT/3,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.director.next_view()


if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = Chapter2View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
