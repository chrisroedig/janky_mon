import signal
import time

from datetime import datetime

# Imports and settings to control the show
import renderers.text as active_renderer
import scenes.klokk as klokk
import scenes.bouncy as bouncy
import scenes.composite as composite
UPDATE_INTERVAL = 0.1

def stop():
    global STOP_THE_SHOW
    STOP_THE_SHOW = True

def run():
    global STOP_THE_SHOW
    STOP_THE_SHOW = False

    signal.signal(signal.SIGTERM, stop)

    scene = composite.Scene([ klokk.Scene(), bouncy.Scene() ])
    renderer = active_renderer.Renderer()

    renderer.reset()

    while not STOP_THE_SHOW:
        scene.render_to(renderer, datetime.now())
        renderer.flip()
        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    print 'ctrl-c to stop this janky crap'
    run()
