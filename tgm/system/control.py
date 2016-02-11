from tgm.system import Entity, sys_event
from tgm.drivers import get_engine

engine = get_engine()


class Updater(Entity):
    def create(self):
        def update():
            engine.next_frame()
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

        engine.tick(update, 60)


class Inactive(Entity):
    pass


class Invisible(Entity):
    pass
