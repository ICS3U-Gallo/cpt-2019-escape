import arcade
import math
import os
import random

import settings

from menu import MenuView
from chapter_2 import MyCollectCure
from chapter_2Instructions import InstructionsView
from chapter_3instructions import Chapter3InstructionsView
from chapter_3 import Chapter3View
from chapter_3ending import Chapter3EndingView
from chapter_4 import Chapter4View
from chapter_4instructions import Chapter4Instructions
from chapter_5 import Chapter5View

class Director(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.view_index = 0
        self.views = [
            MenuView,
            InstructionsView,
            MyCollectCure,
            Chapter3InstructionsView
            Chapter3View,
            Chapter3EndingView
            Chapter4Instructions
            Chapter4View,
            Chapter5View
        ]
        self.next_view()

    def next_view(self):
        next_view = self.views[self.view_index]()
        next_view.director = self
        self.show_view(next_view)
        self.view_index = (self.view_index + 1) % len(self.views)


def main():
    window = Director(settings.WIDTH, settings.HEIGHT, "CPT Structure")
    arcade.run()


if __name__ == "__main__":
    main()
