from tgm.system import GameObject, tgm_event, common_ancestor
from tgm.collision.collision_tests import point_in_polygon


class Collider(GameObject):
    partition_threshold = 10

    def on_create(self, points):
        self.points = points
        self.optimizations = {}
        self.colliders = set()

    def register_collider(self, collider):
        self.colliders.add(collider)

    def unregister_collider(self, collider):
        self.colliders.remove(collider)

    @tgm_event
    def tgm_get_collisions(self, query=GameObject):
        return self.parents[CollisionMask].get_collisions(self, query)

    def get_collisions(self, collider, query=GameObject):
        if self.is_colliding(collider):
            return {self.parent}
        return set()

    def is_colliding(self, other):
        return self.optimizations.get(type(other), self.collision_poly)(other)

    def collision_disc(self, other):
        return True

    def collision_poly(self, other):
        if not self.collision_disc(other):
            return False

        obj1 = self
        obj2 = other

        points = obj1.get_transformed_points(obj2)

        for x, y in obj2.points:
            if obj1.contains_point(x, y, points):
                return True

        for x, y in points:
            if obj2.contains_point(x, y):
                return True

        return False

    def contains_point(self, x, y, points=None):
        if points is None:
            points = self.points
        return point_in_polygon(x, y, points)

    def get_transformed_points(self, other):
        rtn = []

        for point in self.points:
            x, y, rot, x_scale, y_scale = self.transform.get_offset(
                other.transform, point + (0, 1, 1)
            )
            rtn.append((x, y))

        return rtn


class CollisionMask(Collider):
    def get_collisions(self, collider, query=GameObject):
        found = set()
        if True or self.is_colliding(collider):
            for col in self.tags.select((Collider - self) < query):
                found.update(col.get_collisions(collider, query))
        return found


class BoxCollider(Collider):
    def on_create(self, width, height):
        width /= 2
        height /= 2
        super().on_create([
            (-width, -height),
            (width, -height),
            (width, height),
            (-width, height)
        ])


class Collision(object):
    def __init__(self):
        self.objects = set()

    def __bool__(self):
        return bool(self.objects)
