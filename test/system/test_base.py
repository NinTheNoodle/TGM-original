import unittest
from tgm.system import GameObject, tgm_event, game_objects
from weakref import ref
import gc


class TestGameObject(unittest.TestCase):
    def test_transform_create(self):
        root = GameObject(None)
        child = GameObject(root)
        self.assertEqual(len(game_objects), 2)

        root.x = 5
        self.assertEqual(len(game_objects), 3)

        child.x = 5
        self.assertEqual(len(game_objects), 4)

        root.destroy()

    def test_simple_destroy(self):
        root = GameObject(None)

        weak = ref(root)

        root.destroy()
        del root

        gc.collect()
        self.assertIsNone(weak())
        self.assertFalse(game_objects)

    def test_child_destroy(self):
        root = GameObject(None)
        child = GameObject(root)

        weak = ref(child)

        child.destroy()
        del child

        gc.collect()
        self.assertIsNone(weak())
        self.assertSetEqual(root.children, set())
        self.assertEqual(len(game_objects), 1)

    def test_parent_destroy(self):
        root = GameObject(None)
        child = GameObject(root)

        weak_root = ref(root)
        weak_child = ref(child)

        root.destroy()
        del root
        del child

        gc.collect()
        self.assertIsNone(weak_root())
        self.assertIsNone(weak_child())
        self.assertFalse(game_objects)

    def test_event_destroy(self):
        class TestClass(GameObject):
            @tgm_event
            def tgm_update(self):
                pass

        root = TestClass(None)
        child = TestClass(root)

        weak_root = ref(root)
        weak_child = ref(child)

        root.destroy()
        del root
        del child

        gc.collect()
        self.assertIsNone(weak_root())
        self.assertIsNone(weak_child())
        self.assertFalse(game_objects)

    def test_transform_destroy(self):
        root = GameObject(None)
        child = GameObject(root)

        root.x = 5
        child.x = 5

        weak_root = ref(root)
        weak_child = ref(child)

        root.destroy()
        del root
        del child

        gc.collect()
        self.assertIsNone(weak_root())
        self.assertIsNone(weak_child())
        self.assertFalse(game_objects)
