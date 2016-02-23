from tgm.system import GameObject, tgm_event, Inactive, Invisible
from tgm.drivers import get_engine
from . import RenderContext

engine = get_engine()


class Window(RenderContext):
    settings = {
        "width": 800,
        "height": 600
    }

    def create(self, width, height):
        self.window = engine.Window(width, height)

        def update(dt):
            self.window.update()

            self.parent.tags.select(
                GameObject[tgm_event.tgm_update_init],
                abort=GameObject[Inactive]
            ).tgm_update_init()

            self.parent.tags.select(
                GameObject[tgm_event.tgm_update],
                abort=GameObject[Inactive]
            ).tgm_update()

            self.parent.tags.select(
                GameObject[tgm_event.tgm_draw],
                abort=GameObject[Invisible]
            ).tgm_draw()

        self.window.schedule(update, 1 / 60)
