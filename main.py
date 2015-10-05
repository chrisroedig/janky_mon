import signal

from datetime import datetime

# Imports and settings to control the show
import renderers.led as active_renderer
import scenes.klokk as klokk
import scenes.bouncy as bouncy
import scenes.composite as composite

UPDATE_INTERVAL = 0.01

def stop():
    global renderer
    renderer.stop()

def run():
    signal.signal(signal.SIGTERM, stop)

    global renderer
    scene = composite.Scene([klokk.Scene(), bouncy.Scene()])
    renderer = active_renderer.Renderer()

    def update_scene():
        scene.render_to(renderer, datetime.now())
        renderer.flip()
        renderer.reset()

    renderer.drive(update_scene, UPDATE_INTERVAL)

if __name__ == '__main__':
    print 'ctrl-c to stop this janky crap'
    run()
