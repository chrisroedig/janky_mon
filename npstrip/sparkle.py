# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *
from datetime import datetime
from datetime import timedelta
import random
import math
import signal

# LED strip configuration:

LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
SCARY          = 0.1     # fraction of scared pixels


class Spark(object):
  def __init__(self):
    self.reset()

  def reset(self, imax=60):
    self.start_time = datetime.now()
    self.age_offset = random.random()
    self.amplitude = 0.6 + 0.38*random.random()
    self.position = int(imax*random.random())
    self.time_constant = 1.0 + 1.0*random.random()
    self.mix = int(255*random.random())
    self.scared = int(SCARY > random.random())

  @property
  def age(self):
    return (datetime.now()-self.start_time).total_seconds()+self.age_offset

  @property
  def current_amplitude(self):
    return self.amplitude*(math.e**(-self.age/self.time_constant))

  @property
  def pixel_data(self):
    if self.age>3*self.time_constant:
	self.reset()
    return (
	self.position,
	int(255*self.scared*self.current_amplitude),
        int(self.mix*self.current_amplitude*(1.0-self.scared)),
        int((255-self.mix)*self.current_amplitude*(1.0-self.scared))
	)

# Main program logic follows:
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

    sparks = [Spark() for i in range(20)]

    while not STOP_FLAG:
        for s in sparks:
            strip.setPixelColorRGB(*s.pixel_data)
        strip.show()
        time.sleep(0.01)

if __name__ == '__main__':
  sparkle()
  print('done')
