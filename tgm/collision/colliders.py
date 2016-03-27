from tgm.system import GameObject, tgm_event, common_ancestor


class Collider(GameObject):
    def on_create(self, points):
        self.points = points
        self.optimizations = {}
        self.world = self.tags.get_first(CollisionWorld)

    def is_colliding(self, other):
        if self.world != other.world:
            return False
        return self.optimizations.get(type(other), self.collision_poly)(other)

    def collision_bbox(self, other):
        return True

    def collision_poly(self, other):
        if not self.collision_bbox(other):
            return False
        return True

    @property
    def bbox(self):
        if self.bbox_changed:
            x_zip, y_zip = zip(*self.transformed_points)
            self._bbox = min(x_zip), min(y_zip), max(x_zip), max(y_zip)
            self.bbox_changed = False
        return self._bbox

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value
        self.bbox_changed = True

    def relative_points(self, parent):
        self._transformed_points = []

        for point in self.points:
            x, y, rot, x_scale, y_scale = self.transform.get_transform(
                transform=point + (0, 1, 1),
                abort=parent
            )
            self._transformed_points.append((x, y))

        return self._transformed_points

    @tgm_event
    def tgm_update(self):
        pass


class CollisionWorld(GameObject):
    def get_possible_collisions(self, bbox, query):
        return self.tags.select(Collider < query)


class FalseCollider(object):
    def __init__(self, points):
        self.bbox = [0, 0, 0, 0]
