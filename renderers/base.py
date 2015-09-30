class Renderer(object):
    """
    Common renderer behavior
    """
    def reset(self):
        for position in range(self.pixel_count):
            self.set_pixel(position, (0, 0, 0))

    def set_all_pixels(self, rgbs):
        for position in range(self.pixel_count):
            self.set_pixel(position, rgbs[position])
