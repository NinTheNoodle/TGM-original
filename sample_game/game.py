from tgm.system import GameObject, tgm_event


class Rotater(GameObject):
    def on_create(self, rot):
        self.rot = rot

    @tgm_event
    def tgm_update(self):
        self.rotation += self.rot
