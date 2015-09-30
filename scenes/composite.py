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
        self.already_painted = { }

    @property
    def pixel_count(self):
        return self.delegate.pixel_count

    @property
    def max_intensity(self):
        return self.delegate.max_intensity

    def set_pixel(self, position, rgb):
        # Could do all kinds of fancy blending here
        # For now, just don't erase something that is already set
        r, g, b = rgb
        if r == 0 and g == 0 and b == 0 and self.already_painted.get(position, False):
            return
        self.already_painted[position] = True
        self.delegate.set_pixel(position, rgb)

