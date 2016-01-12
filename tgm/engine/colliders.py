from tgm.common import GameObject
from .events import event as col_event


class Collider(GameObject):
    @col_event
    def get_collisions(self):
        return [6, 6]
