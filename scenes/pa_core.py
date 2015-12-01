from pusherclient import Pusher
import json
import time
import random
import threading
import math


PUSHER_CLIENT_KEY = '339fb0632e1d5b4e2acf'
PRO_COLOR = (247, 147, 0)
RETRO_COLOR = (223, 19, 79)
PULSE_DELAY = 0.5
PULSE_LENGTH = 0.5


class Scene(object):
    """
      Dots on a.....strip...
    """
    def __init__(self):
        self.dots = []
        self.pusher_thread = threading.Thread(target=self.connect_to_pusher)
        self.pusher_thread.start()
        self.cleanup()

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

    def add_dot(self,color):
        self.dots.append({
            'time': time.time(),
            'color': color,
          })

    def new_pa(self, data_str):
        try:
          data = json.loads(data_str)
          if data.get('is_retrospective', False):
             self.add_dot(RETRO_COLOR)
          else:
             self.add_dot(PRO_COLOR)
        except Exception as err:
          print err

    def pixel_pair(self, dot):
        age = time.time() - dot['time']
        b_pos = int(30*min(age/PULSE_DELAY,1.0))
        t_pos = int(60-30*min(age/PULSE_DELAY,1.0))
        color = self.pixel_color(dot['color'], dot['time'])
        return [
          dict(dot, color=color, pos=b_pos),
          dict(dot, color=color, pos=t_pos)
        ]

    def pixel_color(self, base_color,time):
        amp = 0.5+0.5*math.e**(-((time-PULSE_DELAY)/PULSE_LENGTH)**2.0)
        return tuple([int(amp*c) for c in base_color])

    @property
    def pixels(self):
        pixel_dots = []
        for dot in self.dots:
          pixel_dots += self.pixel_pair(dot)
        return pixel_dots

    def render_to(self, renderer, moment):
        for pix in self.pixels:
            renderer.set_pixel(pix['pos'], pix['color'])
        return

    def cleanup(self):
        threading.Timer(0.25, self.cleanup).start()
        if len(self.dots) <= 0:
            return
        if self.last_dot.get('expired', False):
          self.dots = self.dots[1:]

    @property
    def last_dot(self):
        last = self.dots[0]
        last['expired'] = (time.time() - last['time']) > 3*PULSE_DELAY
        return last


if __name__ == '__main__':
    s= Scene()
    while True:
        time.sleep(0.1)
        print s.pixels
        print '\n'


