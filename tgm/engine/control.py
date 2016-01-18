from tgm.common import GameObject, sys_event
from tgm.drivers import get_engine

engine = get_engine()


class Updater(GameObject):
    def create(self):
        def update():
            self.parent.tags.select(GameObject["start"]).start()
            self.parent.tags.select(GameObject["update"]).update()
            self.parent.tags.select(GameObject["draw"]).draw()

        engine.tick(update, 60)
