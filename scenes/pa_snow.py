import time
import random
import threading
import math
import json
from data import forecastio
from pusherclient import Pusher

FLAKE_COLOR = (220, 250,255 )
FALL_RATE = 6.0
FLAKE_PERIOD = 8.0
PUSHER_CLIENT_KEY = '339fb0632e1d5b4e2acf'
PRO_COLOR = (247, 147, 0)
RETRO_COLOR = (223, 19, 79)


class Scene(object):
    """
      Dots on a.....strip...
    """
    def __init__(self):
        self.dots = []
        self.cleanup()
	self.connect_to_pusher()

    def connect_to_pusher(self):
        print 'setting up pusher'
        self.pusher_client = Pusher(PUSHER_CLIENT_KEY, secure=True)
        self.pusher_client.connection.bind(
            'pusher:connection_established', self.subscribe_on_pusher)
        self.pusher_client.connect()

    def subscribe_on_pusher(self, data):
        print 'pusher connected'
        self.pusher_channel = self.pusher_client.subscribe('pa_channel')
        self.pusher_channel.bind('pa_event', self.new_pa)
        print 'pusher subscribed'
    
    def new_pa(self, data_str):
        try:
          data = json.loads(data_str)
          if data.get('is_retrospective', False):
             self.new_flake(RETRO_COLOR)
          else:
             self.new_flake(PRO_COLOR)
        except Exception as err:
          print err

    @property
    def fall_rate(self):
        return FLAKE_PERIOD*(1.0+0.1*random.random())

    def new_flake(self, color):
        self.dots.append({
          'time': time.time(),
          'velocity': self.fall_rate,
	  'color': color,
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
            dot['color'] = dot['color']
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


