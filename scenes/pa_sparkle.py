from pusherclient import Pusher
import json
import time
import random
import threading
import math


PUSHER_CLIENT_KEY = '339fb0632e1d5b4e2acf'

PRO_COLOR = (247, 147, 0)
RETRO_COLOR = (223, 19, 79)
DECAY_TIME = 10.0

class Scene(object):
    """
      Dots on a.....strip...
    """
    def __init__(self):
        self.dots = []
        self.pusher_thread = threading.Thread(target=self.connect_to_pusher)
        self.pusher_thread.start()

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
            'pos': random.randint(0, 59)
          })

    def cleanup(self):
        if len(self.dots) <= 0:
            return
        last_spark = self.dots[0]
        if time.time() - last_spark['time'] > 90:
          self.dots = self.dots[1:]

    def new_pa(self, data_str):
        try:
          data = json.loads(data_str)
          if data.get('is_retrospective', False):
             self.add_dot(RETRO_COLOR)
          else:
             self.add_dot(PRO_COLOR)
        except Exception as err:
          print err

    @property
    def pixels(self):
        pixel_dots = []
        for dot in self.dots:
          age = time.time() - dot['time']
          amp = math.e**(-(age/DECAY_TIME))
          old_c = dot['color']
          new_c = tuple([int(amp*c) for c in old_c])
          pixel_dots.append({'pos':dot['pos'], 'color':new_c})
        return pixel_dots


    def render_to(self, renderer, moment):
        for pix in self.pixels:
            renderer.set_pixel(pix['pos'], pix['color'])
        return

if __name__ == '__main__':
    s= Scene()
    while True:
        time.sleep(1.0)
        s.cleanup()
        print s.pixels
        print '\n\n'


