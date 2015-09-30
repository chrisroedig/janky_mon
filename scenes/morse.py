# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
from neopixel import *
import signal

# LED strip configuration:

LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)



LETTER_CODE = {
        'A': '.-',     'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',
        ' ': '',
        }

DASH_LENGTH = 6
DOT_LENGTH = 2
SPACE_LENGTH = 2
CHAR_SPACE_LENGTH = 4
WORD_SPACE_LENGTH = 8

# Main program logic follows:
def get_strip():
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	return strip

def convert_word(msg):
    code_arr = []
    for letter in msg.upper():
        letter_code = LETTER_CODE[letter]
        for char in letter_code:
            if char == '.':
                code_arr += [True]*DOT_LENGTH
            elif char == '-':
                code_arr += [True]*DASH_LENGTH
            else:
                raise Exception('shiiiiit')
            code_arr += [False]*SPACE_LENGTH
        code_arr += [False]*CHAR_SPACE_LENGTH
    code_arr += [False]*WORD_SPACE_LENGTH
    return code_arr


def window_word(msg, offset):
    msg_code_arr = convert_word(msg)
    code_arr = ([False]*LED_COUNT) + msg_code_arr + ([False]*LED_COUNT)
    offset = offset % (len(msg_code_arr)+LED_COUNT)
    output = code_arr[offset:LED_COUNT+offset]
    return output


def pixellate_word(msg, offset, strip):
    output = []
    for i, pixel in enumerate(window_word(msg, offset)):
        strip.setPixelColorRGB(i, 10, 10, 5+100*pixel)
    strip.show()

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
    offset = 0
    while not STOP_FLAG:
        pixellate_word('hello world', offset, strip)
        offset += 1
        time.sleep(0.05)
