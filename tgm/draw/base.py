from tgm.system import Entity, tgm_event
from tgm.drivers import get_engine

engine = get_engine()


class RenderContext(Entity):
    @tgm_event
    def tgm_render(self):
        self.parent.tags.select(
            Entity[tgm_event.tgm_render],
            stop=Entity[RenderContext] - Entity[self],
            abort=self
        ).render()
