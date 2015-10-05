import math

import renderers.base as base

class Scene(object):
    """
    A scene that aggregates other scenes!
    """
    def __init__(self, scenes):
        self.scenes = scenes

    def render_to(self, renderer, moment):
        wrapper = RendererWrapper(renderer)
        for scene in self.scenes:
            scene.render_to(wrapper, moment)

class RendererWrapper(base.Renderer):
    def __init__(self, delegate):
        self.delegate = delegate

    @property
    def pixel_count(self):
        return self.delegate.pixel_count

    @property
    def max_intensity(self):
        return self.delegate.max_intensity

    def set_pixel(self, position, rgb):
        if rgb is None:
            return
        r, g, b = rgb
        self.delegate.set_pixel(position, rgb)

