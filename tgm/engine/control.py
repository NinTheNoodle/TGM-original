from tgm.common import GameObject, sys_event
from tgm.drivers import get_engine

engine = get_engine()


class Updater(GameObject):
    def init(self):
        def update():
            self.parent.tags.select(sys_event.start).start()
            self.parent.tags.select(sys_event.update).update()
            self.parent.tags.select(sys_event.draw).draw()

        engine.tick(update, 60)
