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

        def on_mouse_move(x, y):
            self.parent.tags.select(
                    Entity[sys_event.mouse_move]
            ).mouse_move(x, y)

        def on_mouse_press(button):
            self.parent.tags.select(
                    Entity[sys_event.mouse_press]
            ).mouse_press(button)

        def on_mouse_release(button):
            self.parent.tags.select(
                    Entity[sys_event.mouse_release]
            ).mouse_release(button)

        engine.render_loop(self.window, on_draw)
        engine.mouse_move_event(self.window, on_mouse_move)
        engine.mouse_press_event(self.window, on_mouse_press)
        engine.mouse_release_event(self.window, on_mouse_release)



