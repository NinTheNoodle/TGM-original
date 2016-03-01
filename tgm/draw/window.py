from tgm.system import GameObject, tgm_event, Inactive, Invisible
from tgm.drivers import get_engine
from tgm.draw import RenderContext

engine = get_engine()


class Window(RenderContext):
    settings = {
        "width": 800,
        "height": 600
    }

    def on_create(self, width, height):
        self.context = engine.Window(width, height)

        def update(dt):
            self.context.update()

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
                abort=GameObject[Invisible],
                stop=RenderContext
            ).tgm_draw()

        self.context.schedule(update, 1 / 60)


class View(RenderContext):
    def create(self, width, height):
        self.context = engine.Context(width, height)

    @tgm_event
    def tgm_draw(self):
        pass
