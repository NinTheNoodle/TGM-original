from tgm.system import GameObject, tgm_event
from tgm.drivers import get_engine

engine = get_engine()


class Inactive(GameObject):
    pass


class Invisible(GameObject):
    pass
