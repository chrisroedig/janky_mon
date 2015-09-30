import math

class Scene(object):
    """
    Keeping time with drips and such
    """
    def __init__(self):
        self.bg_color = (0,0,50)
        self.tick_color = (255,100,50)
        self.column_color = (200,50,0)
        self.minute_color = (0,255,0)

    def render_to(self, renderer, moment):
        renderer.set_all_pixels(self.pixels(renderer.pixel_count, moment))

    def pixels(self, pixel_count, moment):
        pixels = self.bg_pixels(pixel_count)
        pixels = self.column_pixels(pixels, moment)
        pixels = self.tick_pixels(pixels, moment)
        pixels = self.minute_pixels(pixels, moment)
        return pixels

    def bg_pixels(self, pixel_count):
        return [self.bg_color] * pixel_count

    def column_pixels(self, pixels, moment):
        for i in range(self.scale_to_pixels(moment.second, pixels)):
            pixels[i] = self.column_color
        return pixels

    def tick_pixels(self, pixels, moment):
        pixels[self.position(moment, pixels)] = self.tick_color
        return pixels

    def minute_pixels(self, pixels, moment):
        pixels[self.scale_to_pixels(moment.minute, pixels)] = self.minute_color
        return pixels

    def position(self, moment, pixels):
        sec = moment.second
        usec = moment.microsecond
        pos = self.scale_to_pixels(60 - int((60.0 - sec)*usec/1.0e6), pixels)
        return min(len(pixels) - 1, pos)

    def scale_to_pixels(self, value, pixels):
        """
        Scale a time oriented 0-60 value to the number of pixels we are using
        """
        return int(len(pixels)/60.0 * value)

