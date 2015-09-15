# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *
from datetime import datetime
import math
import signal

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

def xform(theta, phi):
    return int(LED_BRIGHTNESS*0.5*(1.+math.cos(2*3.14159*(theta/PERIOD+phi))))

def run():
    global STOP_FLAG
    signal.signal(signal.SIGTERM, stop)
    strip = get_strip()
    for i in range(60):
        strip.setPixelColorRGB(i, 0, 0, 0)
    strip.show()

    while not STOP_FLAG:
        now = datetime.now()
        useconds = now.microsecond+(now.second+60*(now.minute%3))*1000*1000.0
        for i in range(60):
            strip.setPixelColorRGB(i,
                xform((i+1)*useconds, 0),
                xform((60-i)*useconds, 0.333),
                xform((abs(i-30)+1)*useconds, 0.666)
            )
        strip.show()

if __name__ == '__main__':
  run()
  print('done')
