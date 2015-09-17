import random
import datetime
import time
import signal

from neopixel import *
# LED strip configuration:

LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PERIOD         = 3*10*1000*1000
GRAVITY = 15.0
FLOOR = 2.0
BOUNCE = 0.8

class Ball(object):
    def __init__(self, v_init = None):
        self.reset(v_init=v_init)

    def reset(self, v_init = None):
        if v_init is None:
            self.v_init = 55.0
        elif v_init > 10:
            self.v_init = v_init
        else:
            self.v_init = 45.0
        self.color = (255, 0, 0)
        self.t_init = datetime.datetime.now()

    @property
    def time(self):
        return (datetime.datetime.now() - self.t_init).total_seconds()

    @property
    def pos(self):
        pos = self.v_init * self.time - GRAVITY * self.time ** 2
        if pos < FLOOR:
            self.reset(self.v_init*BOUNCE)
        return pos

    def pixel(self, i):
        pixel=max(0,(3.0-abs(i-self.pos)))/3.0
        return (i, 10, 10, 5 + int(100*pixel))


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

