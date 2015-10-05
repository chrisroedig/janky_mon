import base
import sys

from colorama import Fore, Back, Style

class Renderer(base.Renderer):
    """
    A Renderer that renders to text in the terminal
    """
    def __init__(self):
        self.columns = 80
        self.buffer = [ None ] * self.columns

    @property
    def pixel_count(self):
        return self.columns

    @property
    def max_intensity(self):
        return 100

    def set_pixel(self, position, rgb):
        self.buffer[position] = rgb

    def pick_closest_color(self, rgb):
        if rgb is None:
            return Fore.RESET + Back.RESET + Style.RESET_ALL

        r, g, b = rgb
        if r == g and g == b:
            if r == self.max_intensity:
                return Back.WHITE
            if r == 0:
                return Back.BLACK
            return Back.GREY
        if r > g and r > b:
            return Back.RED
        if g > r and g > b:
            return Back.GREEN
        return Back.BLUE

    def flip(self):
        for position in range(self.columns):
            sys.stdout.write(self.pick_closest_color(self.buffer[position]) + ' ')
            self.buffer[position] = None

        print Fore.RESET + Back.RESET + Style.RESET_ALL

