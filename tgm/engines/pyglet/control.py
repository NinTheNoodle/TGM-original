from tgm.common import GameObject, sys_event
import pyglet


class Updater(GameObject):
    def init(self):
        def update(dt):
            self.parent.tags.select(sys_event.start).start()
            self.parent.tags.select(sys_event.update).update()
            self.parent.tags.select(sys_event.draw).draw()

        pyglet.clock.schedule_interval(update, 1/30)
