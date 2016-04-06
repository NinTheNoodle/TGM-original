from tgm.system import run, Level
from tgm.engine import DefaultEngine
from tgm.draw import Window
from tgm.collision import CollisionMask


def setup():
    window = Window(None, 800, 600)
    world = CollisionMask(window, [])
    engine = DefaultEngine(world)

    Level(engine, "sample_game/test_level.json")

run(setup)
