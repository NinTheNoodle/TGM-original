from tgm.system import GameObject, tgm_event, Inactive, Invisible
from tgm.drivers import get_engine
from tgm.draw import RenderContext, quad

engine = get_engine()


class Window(RenderContext):
    def on_create(self, width, height, fps=60):
        self.context = engine.Window(width, height)

        def update(dt):
            self.context.update()
            self.x_scale = self.context.width / width
            self.y_scale = self.context.height / height

            self.tags.select(
                GameObject[tgm_event.tgm_update_init],
                abort=GameObject[Inactive]
            ).tgm_update_init()

            self.tags.select(
                GameObject[tgm_event.tgm_update],
                abort=GameObject[Inactive]
            ).tgm_update()

            self.tags.select(
                GameObject[tgm_event.tgm_draw],
                abort=GameObject[Invisible]
            ).tgm_draw()

        self.context.schedule(update, 1 / fps)

    def get_mouse_pos(self):
        x, y = self.context.get_mouse_pos()
        return self.transform.apply(x, y, 0, 1, 1)[:2]

    def get_mouse_buttons(self):
        return self.context.get_mouse_buttons()
