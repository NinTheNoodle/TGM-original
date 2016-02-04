from tgm.system import GameObject, sys_event
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

        def on_mouse_move(x, y):
            self.parent.tags.select(
                    GameObject[sys_event.mouse_move]
            ).mouse_move(x, y)

        engine.render_loop(self.window, on_draw)
        engine.mouse_move_event(self.window, on_mouse_move)



