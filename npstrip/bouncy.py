import random
import datetime
import time
import signal
import colorsys

from neopixel import *
# LED strip configuration:

LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PERIOD         = 3*10*1000*1000
GRAVITY = 20.0
FLOOR = 0.0
BOUNCE = 0.9
V_INIT = 4.4
V_MIN = 0.05

class Ball(object):
    def __init__(self, v_init = V_INIT):
        self.reset(v_init=v_init)

    def reset(self, v = V_INIT):
        if v < V_MIN:
            self.v_init = V_INIT
        else:
            self.v_init = v
        hue = random.random()
        self.color = tuple([ int(c * 255) for c in colorsys.hsv_to_rgb( hue, 1 , 1 )])
        self.t_init = datetime.datetime.now()

    @property
    def time(self):
        return (datetime.datetime.now() - self.t_init).total_seconds()

    @property
    def pos(self):
        pos = 60 * (self.v_init * self.time - GRAVITY * self.time ** 2)
        if pos < FLOOR:
            self.reset(self.v_init*BOUNCE)
        return pos

    def pixel(self, i):
        val = max(0,(3.0-abs(i-self.pos)))/3.0
        return (i,)+tuple([int(ch*val) for ch in self.color])


def get_strip():
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	return strip

STOP_FLAG = False

def stop():
    global STOP_FLAG
    STOP_FLAG = True


def run():
    global STOP_FLAG
    signal.signal(signal.SIGTERM, stop)
    strip = get_strip()
    for i in range(60):
        strip.setPixelColorRGB(i, 0, 0, 0)
    strip.show()
    b = Ball()
    while not STOP_FLAG:
        for i in range(60):
            strip.setPixelColorRGB(*b.pixel(i))
        strip.show()
        time.sleep(0.05)
