from tgm.system import GameObject
from tgm.system import sys_event
from tgm.system import Transform
from collections import defaultdict


collider_updates = set()


class Collider(GameObject):
    def create(self):
        self.bbox = [0, 0, 0, 0]
        self.points = []
        self.registered = False

        self.transform = Transform(self)
        self.transform_changed()

    @property
    def transformed_bbox(self):
        transform = self.transform.get_transform()
        return (
            self.bbox[0] + transform[0],
            self.bbox[1] + transform[1],
            self.bbox[2] + transform[0],
            self.bbox[3] + transform[1]
        )

    def set_points(self, *points):
        self.points = points
        self.update_bbox()

    def update_bbox(self):
        if self.points:
            x_zip, y_zip = zip(*self.points)
            self.bbox = [min(x_zip), min(y_zip), max(x_zip), max(y_zip)]
        else:
            self.bbox = [0, 0, 0, 0]
        self.update_world_mapping()

    def update_world_mapping(self):
        world = self.tags.get_first(CollisionWorld < GameObject)
        if self.registered:
            world.unregister_collider(self, *self.bbox)
        self.registered = True
        world.register_collider(self, *self.bbox)

    def is_colliding(self, other):
        raise NotImplemented("No collision test provided")

    @sys_event
    def get_collisions(self):
        update_colliders()
        world = self.tags.get_first(CollisionWorld < GameObject)
        possible = world.get_possible_collisions(1)
        collisions = []

        for collider in possible:
            if collider is not self and self.is_colliding(collider):
                collisions.append(collider)

        return collisions

    @sys_event
    def transform_changed(self):
        collider_updates.add(self)


class BoxCollider(Collider):
    def create(self, width, height):
        super(BoxCollider, self).create()
        self.set_points(
            (-width / 2, -height / 2),
            (width / 2, -height / 2),
            (width / 2, height / 2),
            (-width / 2, height / 2)
        )

    def is_colliding(self, other):
        if isinstance(other, BoxCollider):
            transform = self.transform.get_transform()
            bbox = (
                self.bbox[0] + transform[0],
                self.bbox[1] + transform[1],
                self.bbox[2] + transform[0],
                self.bbox[3] + transform[1]
            )
            transform = other.transform.get_transform()
            other_bbox = (
                self.bbox[0] + transform[0],
                self.bbox[1] + transform[1],
                self.bbox[2] + transform[0],
                self.bbox[3] + transform[1]
            )
            return collision_rectangle(bbox, other_bbox)
        raise NotImplemented("")

    def contains_point(self, x, y):
        return point_in_rectangle(x, y, *self.bbox)


class AABBCollider(Collider):
    def is_colliding(self, other):
        if isinstance(other, AABBCollider):
            return collision_rectangle(self.bbox, other.bbox)
        raise NotImplemented("")

    def contains_point(self, x, y):
        return point_in_rectangle(x, y, *self.bbox)


class CompositeCollider(Collider):
    pass


class CollisionWorld(GameObject):
    def create(self):
        self.world = defaultdict(lambda: set())
        self.resolution = 256

    def unregister_collider(self, collider, x1, y1, x2, y2):
        for x, y in zip(
                range(0, int(x2 - x1), self.resolution),
                range(0, int(y2 - y1), self.resolution)):
            pos = (x + x1, y + y1)
            self.world[pos].remove(collider)
            if not self.world[pos]:
                del self.world[pos]

    def register_collider(self, collider, x1, y1, x2, y2):
        for x, y in zip(
                range(0, int(x2 - x1), self.resolution),
                range(0, int(y2 - y1), self.resolution)):
            self.world[(x + x1, y + y1)].add(collider)

    def get_possible_collisions(self, bbox):
        return self.parent.tags.select(Collider)


def update_colliders():
    for collider in collider_updates:
        collider.update_bbox()
    collider_updates.clear()


def collision_rectangle(rect1, rect2):
    return (rect2[2] > rect1[0] and
            rect2[3] > rect1[1] and
            rect1[2] > rect2[0] and
            rect1[3] > rect2[1])


def point_in_rectangle(x, y, x1, y1, x2, y2):
    return x1 < x < x2 and y1 < y < y2


# http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def collision_polygon(poly1, poly2):
    return False


def collision_circle(circle1, circle2):
    return abs(
            (circle1[0] ** 2 + circle1[1] ** 2) ** 0.5 -
            (circle2[0] ** 2 + circle2[1] ** 2) ** 0.5
    ) < circle2[2] + circle2[2]
