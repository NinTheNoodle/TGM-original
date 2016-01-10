from tgm.common import GameObject, sys_event
from tgm.engine2d.transform import Transform, transform_event
import pyglet


class Window(GameObject):
    def init(self):
        self.window = pyglet.window.Window()

        @self.window.event
        def on_draw():
            self.parent.tags.select(sys_event.render).render("hi")


class Sprite(GameObject):
    def init(self):
        self.image = pyglet.image.load(
            r"C:\Users\Docopoper\Desktop\Python Projects"
            r"\In Progress\ContributorTest\python.png"
        )
        self.sprite = pyglet.sprite.Sprite(self.image)
        self.transform = Transform(parent=self)

    @sys_event
    def render(self, hi):
        self.sprite.draw()

    @sys_event
    def draw(self):
        self.sprite.set_position(*self.transform.get_pos())
        print(self.transform.get_pos())
