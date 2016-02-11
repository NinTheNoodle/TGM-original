from tgm.system import Entity, sys_event
from tgm.drivers import get_engine
from .base import RenderContext

engine = get_engine()


class Window(RenderContext):
    settings = {
        "width": 800,
        "height": 600
    }

    def create(self, width, height):
        self.window = engine.get_window(width, height)
        self.window.set_caption("TGM Sample")

        def on_draw():
            self.render()

        engine.render_loop(self.window, on_draw)
