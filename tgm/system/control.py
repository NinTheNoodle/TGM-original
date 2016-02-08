from tgm.system import Entity, sys_event
from tgm.drivers import get_engine

engine = get_engine()


class Updater(Entity):
    def create(self):
        def update():
            self.parent.tags.select(Entity[sys_event.update]).update()
            self.parent.tags.select(Entity[sys_event.draw]).draw()

        engine.tick(update, 60)
