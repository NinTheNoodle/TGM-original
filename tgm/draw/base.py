from tgm.system import Entity, sys_event
from tgm.drivers import get_engine

engine = get_engine()


class RenderContext(Entity):
    def create(self, width, height):
        self.texture = engine.Texture(width, height)

    @sys_event
    def render(self):
        self.parent.tags.select(
            Entity[sys_event.render],
            stop=Entity[RenderContext] - Entity[self],
            abort=self
        ).render()
