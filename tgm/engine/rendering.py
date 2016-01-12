from tgm.common import GameObject, sys_event, TagAttribute
from tgm.engine.transform import Transform
from tgm.drivers import get_renderer

renderer = get_renderer()


class Window(GameObject):
    def init(self):
        self.window = renderer.get_window()

        def on_draw():
            self.parent.tags.select(sys_event.render).render("hi")

        renderer.render_loop(self.window, on_draw)


class Sprite(GameObject):
    visible = TagAttribute(default=True)

    def init(self):
        self.image = renderer.get_image(
            r"C:\Users\Docopoper\Desktop\Python Projects"
            r"\In Progress\ContributorTest\python.png"
        )
        self.sprite = renderer.get_sprite(self.image)
        self.transform = Transform(parent=self)

    @sys_event
    def render(self, hi):
        x, y = self.transform.get_pos()
        renderer.draw_sprite(self.sprite, x, y, 0, 1)
