import signal
import npstrip.clock
import npstrip.morse
import time
# LED strip configuration:

LED_COUNT = 60      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal

STOP_FLAG = False


def get_strip():
    st = neopixel.Adafruit_NeoPixel(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    st.begin()
    return st


def stop():
    npstrip.clock.stop()


def run():
    npstrip.clock.run()


if __name__ == '__main__':
    print 'ctrl-c to stop this janky crap'
    run()
