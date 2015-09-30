import math

PERIOD = 3*10*1000*1000

class Scene(object):
    def render_to(self, renderer, moment):
        useconds = moment.microsecond + (moment.second + 60 * (moment.minute % 3)) * 1000 * 1000.0
        for i in range(renderer.pixel_count):
            renderer.set_pixel(i, (
                xform(renderer.max_intensity, (i + 1) * useconds, 0),
                xform(renderer.max_intensity, (renderer.pixel_count - i) * useconds, 0.333),
                xform(renderer.max_intensity, (abs(i - (renderer.pixel_count/2)) + 1) * useconds, 0.666)
            ))

def xform(intensity, theta, phi):
    return int(intensity * 0.5 * (1.0 + math.cos(2 * 3.14159 * (theta/PERIOD + phi))))

