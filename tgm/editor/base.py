from tgm.system import GameObject, Level
import tgm


class Editor(GameObject):
    def on_create(self):
        tgm.collision.CollisionWorld(self)

    def start(self):
        self.sprite = tgm.draw.Sprite(
            self, r"C:\Users\Docopoper\Desktop"
                  r"\Python Projects\In Progress"
                  r"\TGM\tgm\editor\assets\back.png")
        self.sprite.x_scale = 1024 / self.sprite.width
        self.sprite.y_scale = 768 / self.sprite.height
        self.sprite.x = 1024 // 2
        self.sprite.y = 768 // 2
        self.sprite.depth = 5

        self.level = Level(
            self,
            r"C:\Users\Docopoper\Desktop\Python Projects\In Progress"
            r"\TGM\tgm\editor\assets\level_editor.json"
        )
