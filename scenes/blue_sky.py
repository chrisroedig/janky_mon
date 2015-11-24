import time
import math

BASE_BLUE = (86,133,181)
BLEACH_AMP = 1.0
TOTAL_AMPLITUDE = 0.2

class Scene(object):
    """
      Dots on a.....strip...
    """
    def render_to(self, renderer, moment):
      for i in range(60):
        renderer.set_pixel(i, self.pixel(i))

    def pixel(self, i):
      bleach = 255*BLEACH_AMP*math.sin(2*math.pi*(i+6*time.time())/60.0)**2
      bleach_c = (bleach, bleach, bleach)
      magnitude = TOTAL_AMPLITUDE/(1.0 + BLEACH_AMP)
      return tuple([int(sum(c)*magnitude) for c in zip(bleach_c, BASE_BLUE)])


if __name__== '__main__':
    s= Scene()
    while True:
        time.sleep(0.1)
        # print s.pixel(0)
        print [ s.pixel(i) for i in  range(60)]
        print '\n'


