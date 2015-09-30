from neopixel import *

import base

class Renderer(base.Renderer):
    """
    A Renderer that renders to the LED strip
    """
    def __init__(self,
            led_count      = 60,      # Number of LED pixels.
            led_pin        = 18,      # GPIO pin connected to the pixels (must support PWM!).
            led_freq_hz    = 800000,  # LED signal frequency in hertz (usually 800khz)
            led_dma        = 5,       # DMA channel to use for generating signal (try 5)
            led_brightness = 128,     # Set to 0 for darkest and 255 for brightest
            led_invert     = False,   # True to invert the signal (when using NPN transistor level shift)
            period         = 3*10*1000*1000):
        self.led_count = led_count
        self.led_brightness = led_brightness
        self.strip = Adafruit_NeoPixel(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness)
        self.strip.begin()

    @property
    def pixel_count(self):
        return self.led_count

    @property
    def max_intensity(self):
        return self.led_brightness

    def set_pixel(self, position, rgb):
        self.strip.setPixelColorRGB(position, *rgb)

    def flip(self):
        self.strip.show()


