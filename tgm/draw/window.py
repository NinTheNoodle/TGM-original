from tgm.system import Entity, sys_event, Inactive, Invisible
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
                Entity[sys_event.update_init],
                abort=Entity[Inactive]
            ).update_init()

            self.parent.tags.select(
                Entity[sys_event.update],
                abort=Entity[Inactive]
            ).update()

            self.parent.tags.select(
                Entity[sys_event.draw],
                abort=Entity[Invisible]
            ).draw()

        self.window.schedule(update, 1 / 60)
