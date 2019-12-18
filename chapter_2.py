
from platform import system
import arcade
import settings
import typing
import pyglet
import random

class Chapter1View(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Chapter 1", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        self.director.next_view()

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
        raise Exception("Error, passed in a string as a sound. Make sure to use load_sound first, and use that result in play_sound.")
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
    #creats an image
    #try:
        image = arcade.load_texture(texture, mirrored=False, scale=0.5)
        arcade.draw_xywh_rectangle_textured(x, y, wid, ht, image, 0, 255, 1, 1)
    #except:
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
    my_view = Chapter1View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
