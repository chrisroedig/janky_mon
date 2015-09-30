import base
import sys

from colorama import Fore, Back, Style

class Renderer(base.Renderer):
    """
    A Renderer that renders to text in the terminal
    """
    def __init__(self):
        self.columns = 80
        self.buffer = [ Back.BLACK ] * self.columns

    @property
    def pixel_count(self):
        return self.columns

    @property
    def max_intensity(self):
        return 100

    def set_pixel(self, position, rgb):
        self.buffer[position] = self.pick_closest_color(rgb)

    def pick_closest_color(self, rgb):
        r, g, b = rgb
        if r > g and r > b:
            return Back.RED
        if g > r and g > b:
            return Back.BLUE
        return Back.GREEN

    def flip(self):
        for position in range(self.columns):
            sys.stdout.write(self.buffer[position] + ' ')
            self.buffer[position] = Fore.BLACK

        print(Fore.RESET + Back.RESET + Style.RESET_ALL)


