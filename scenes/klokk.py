import math

class Scene(object):
    """
    Keeping time with drips and such
    """
    def __init__(self):
        self.tick_color = (255,100,50)
        self.column_color = (200,50,0)
        self.minute_color = (0,255,0)

    def render_to(self, renderer, moment):
        self.column_pixels(renderer, moment)
        self.tick_pixels(renderer, moment)
        self.minute_pixels(renderer, moment)

    def column_pixels(self, renderer, moment):
        for i in range(self.scale_to_pixels(moment.second, renderer.pixel_count)):
            renderer.set_pixel(i, self.column_color)

    def tick_pixels(self, renderer, moment):
        renderer.set_pixel(self.position(moment, renderer.pixel_count), self.tick_color)

    def minute_pixels(self, renderer, moment):
        renderer.set_pixel(self.scale_to_pixels(moment.minute, renderer.pixel_count), self.minute_color)

    def position(self, moment, pixel_count):
        sec = moment.second
        usec = moment.microsecond
        pos = self.scale_to_pixels(60 - int((60.0 - sec)*usec/1.0e6), pixel_count)
        return min(pixel_count - 1, pos)

    def scale_to_pixels(self, value, pixel_count):
        """
        Scale a time oriented 0-60 value to the number of pixels we are using
        """
        return int(pixel_count/60.0 * value)

