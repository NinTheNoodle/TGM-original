from tgm.system import GameObject, tgm_event
from tgm.drivers import get_engine

engine = get_engine()


class RenderContext(GameObject):
    @tgm_event
    def tgm_render(self):
        self.parent.tags.select(
            GameObject[tgm_event.tgm_render],
            stop=GameObject[RenderContext] - GameObject[self],
            abort=self
        ).render()
