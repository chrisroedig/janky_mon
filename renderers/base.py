import time

class Renderer(object):
    """
    Common renderer behavior
    """
    def stop(self):
        self.stopped = True

    def drive(self, driver, interval):
        self.stopped = False
        while not self.stopped:
            driver()
            time.sleep(interval)

    def reset(self):
        for position in range(self.pixel_count):
            self.set_pixel(position, None)

