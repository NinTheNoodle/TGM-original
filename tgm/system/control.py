from tgm.system import Entity, tgm_event
from tgm.drivers import get_engine

engine = get_engine()


class Inactive(Entity):
    pass


class Invisible(Entity):
    pass
