import time
import random
import threading
import math
from data import forecastio

FLAKE_COLOR = (220, 250,255 )
FALL_RATE = 6.0
FLAKE_PERIOD = 8.0


class Scene(object):
    """
      Dots on a.....strip...
    """
    def __init__(self):
        self.dots = []
        self.cleanup()
        self.new_flake()

    @property
    def next_flake(self):
        w = forecastio.get_weather()
        if w.get('currently') is None:
          return FLAKE_PERIOD
        prob = float(w['currently']['precipProbability'])
        return FLAKE_PERIOD*(1.1-prob**2)*(1.0+0.1*random.random())

    @property
    def fall_rate(self):
        w = forecastio.get_weather()
        if w.get('currently') is None:
          return FALL_RATE
        intens = float(w['currently']['precipIntensity'])
        return FALL_RATE*(1.0+intens)*(0.7+0.3*random.random())


    def new_flake(self):
        threading.Timer(self.next_flake, self.new_flake).start()
        self.dots.append({
          'time': time.time(),
          'velocity': self.fall_rate,
          'amp': 1.0-0.7*random.random()
          })

    def cleanup(self):
        threading.Timer(0.25, self.cleanup).start()
        if len(self.dots) <= 0:
            return
        if self.last_dot.get('expired', False):
          self.dots = self.dots[1:]

    @property
    def last_dot(self):
        last = self.dots[0]
        age = time.time() - last['time']
        pos = 60 - age*last['velocity']
        last['expired'] = pos < 0
        return last


    @property
    def pixels(self):
        pixel_dots = []
        for dot in self.dots:
            age = time.time() - dot['time']
            dot['pos'] = int(60 - age*dot['velocity'])
            dot['color'] = tuple([int(dot['amp']*c) for c in FLAKE_COLOR])
            if dot['pos'] >= 0:
              pixel_dots.append(dot)
        return pixel_dots


    def render_to(self, renderer, moment):
        for pix in self.pixels:
            renderer.set_pixel(pix['pos'], pix['color'])
        return

if __name__ == '__main__':
    s= Scene()
    while True:
        time.sleep(0.1)
        print s.pixels
        print '\n'


