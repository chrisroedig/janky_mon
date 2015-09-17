import random
import datetime
import time
import signal

LED_COUNT      = 60
GRAVITY = 10.0
FLOOR = 1.0
BOUNCE = 0.9

class Ball(object):
    def __init__(self, v_init = None):
        self.reset(v_init=v_init)

    def reset(self, v_init = None):
        if v_init is None:
            self.v_init = 35.0
        elif v_init > 5:
            self.v_init = v_init
        else:
            self.v_init = 45.0
        self.color = (255, 0, 0)
        self.t_init = datetime.datetime.now()

    @property
    def time(self):
        return (datetime.datetime.now() - self.t_init).total_seconds()

    @property
    def pos(self):
        pos = self.v_init * self.time - GRAVITY * self.time ** 2
        if pos < FLOOR:
            print 'BOUNCE'
            self.reset(self.v_init*BOUNCE)
        return pos

    def pixel(self, i):
        pixel=max(0,(3.0-abs(i-self.pos)))/3.0
        return (i, 10, 10, 5 + int(100*pixel))

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
    while not STOP_FLAG:
        for i in range(60):
            strip.setPixelColorRGB(*b.pixel(i))
        strip.show()
        time.sleep(0.05)

if __name__ == '__main__':
    b = Ball()
    def pp(x): print(x)
    for i in range(0,1000):
        for i in range(60):
            print b.pixel(i)
        time.sleep(0.1)
