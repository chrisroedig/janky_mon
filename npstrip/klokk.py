import time

from neopixel import *
from datetime import datetime
import math
import signal



class SecondHand(object):

    def __init__(self):
        self.tick_color = (255,255,255)
        self.column_color = (255,0,0)

    @property
    def tick_pixels(self):
        pix={}
        pix[self.position]=self.tick_color
        return pix

    @property
    def column_pixels(self):
        sec = datetime.now().second
        pix = {}
        for i in range(sec):
            pix[i] = self.column_color
        return pix

    @property
    def pixels(self):
        pix = self.column_pixels
        pix.update(self.tick_pixels)
        return pix

    @property
    def position(self):
        sec = datetime.now().second
        usec = datetime.now().microsecond
        return 60-int((60.0-sec)*usec/1.0e6)


# LED strip configuration:

LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PERIOD         = 3*10*1000*1000

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
    s = SecondHand()

    while not STOP_FLAG:
        for pos, color in s.pixels.items():
            pxc =tuple([pos]+list(color))
            strip.setPixelColorRGB(**pxc)
        strip.show()
        time.sleep(.01)

if __name__ == '__main__':
  run()
  print('done')
