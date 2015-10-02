
class Scene(object):
    def __init__(self):
        self.velocity_init = 400.0
        self.velocity_min = 3.0
        self.bounce_init = 0.85

        self.excitement_factor = 4.0
        self.gravity = 980.0
        self.dot_size = 2

        self.velocity = self.velocity_init
        self.bounce = self.bounce_init
        self.position = 0.0
        self.moment = None

    def render_to(self, renderer, moment):
        time_delta = self.calculate_time_delta(moment) * self.excitement_factor
        previous_position = self.position
        self.moment = moment

        self.adjust_state_for_time_delta(time_delta)
        self.handle_bounce()
        self.handle_reset()

        trail_start, trail_end = self.calculate_trail(previous_position)
        dot_start, dot_end = (self.position, self.position + self.dot_size)

        for i in range(renderer.pixel_count):
            rgb = (0, 0, 0)
            if trail_start <= i <= trail_end:
                rgb = (0, renderer.max_intensity, 0)
            if dot_start <= i <= dot_end:
                rgb = (0, 0, renderer.max_intensity)
            renderer.set_pixel(i, rgb)

    def calculate_time_delta(self, moment):
        if self.moment is None:
            return 0
        interval = moment - self.moment
        return interval.seconds + interval.microseconds/10e6

    def adjust_state_for_time_delta(self, time_delta):
        if time_delta > 0:
            position_delta = self.velocity * time_delta
            velocity_delta = self.gravity * time_delta
            self.position = max(0, self.position + position_delta)
            self.velocity = self.velocity - velocity_delta

    def handle_bounce(self):
        if self.velocity < 0 and self.position == 0:
            self.velocity = abs(self.velocity) * self.bounce
            self.bounce = self.bounce - self.bounce * 0.1

    def handle_reset(self):
        if self.position == 0 and self.velocity < self.velocity_min:
            self.velocity = self.velocity_init
            self.bounce = self.bounce_init

    def calculate_trail(self, previous_position):
        trail_length = 3.14 * self.dot_size * abs(self.velocity)/self.velocity_init - self.dot_size
        if previous_position <= self.position:
            return (self.position - trail_length, self.position)
        return (self.position, self.position + trail_length)

