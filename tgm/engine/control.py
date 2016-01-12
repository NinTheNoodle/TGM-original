from tgm.common import GameObject, sys_event
from tgm.drivers import get_controller

controller = get_controller()


class Updater(GameObject):
    def init(self):
        def update():
            self.parent.tags.select(sys_event.start).start()
            self.parent.tags.select(sys_event.update).update()
            self.parent.tags.select(sys_event.draw).draw()

        controller.tick(update, 60)
