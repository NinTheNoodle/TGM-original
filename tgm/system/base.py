import operator
import collections
import os
import sys
from weakref import WeakKeyDictionary, ref, WeakSet

auto_call = WeakKeyDictionary()
game_objects = WeakSet()
destroyed_game_objects = WeakSet()


def is_tag(obj):
    try:
        if issubclass(obj, BaseTag):
            return True
    except TypeError:
        pass

    if isinstance(obj, BaseTag):
        return True

    return False


def get_all(candidate, query, stop=None, abort=None):
    if abort is not None and has_tags(candidate, abort):
        return set()

    rtn = run_query(candidate, query)
    if rtn:
        return rtn

    if candidate.parent is None:
        return set()

    if stop is not None and has_tags(candidate, stop):
        return set()

    return get_all(candidate.parent, query, stop, abort)


def select_all(candidate, query, stop=None, abort=None, enabled_only=True):
    if enabled_only and candidate.disabled:
        return set()

    if abort is not None and has_tags(candidate, abort):
        return set()

    rtn = run_query(candidate, query)

    if stop is not None and has_tags(candidate, stop):
        return rtn

    for child in candidate.children:
        rtn.update(select_all(child, query, stop, abort))

    return rtn


def run_query(candidate, query):
    if query is candidate:
        return {candidate}

    simple_operations = {
        "&": set.intersection,
        "|": set.union,
        "^": set.symmetric_difference,
        "-": set.difference
    }

    if isinstance(query, TagGroup):
        operation = query.operation
        obj1 = query.obj1
        obj2 = query.obj2
        if operation in simple_operations:
            return simple_operations[operation](run_query(candidate, obj1),
                                                run_query(candidate, obj2))

        if operation == "<":
            if has_tags(candidate, obj1) and has_tags(candidate.parent, obj2):
                return run_query(candidate, obj1)
            if has_tags(candidate, obj2) and any(
                    has_tags(child, obj1) for child in candidate.children):
                return set.union(
                    *(
                        run_query(child, obj1)
                        for child in candidate.children
                    )
                )
            return set()

        if operation == ">":
            if has_tags(candidate, obj2) and has_tags(candidate.parent, obj1):
                return run_query(candidate.parent, obj1)
            if has_tags(candidate, obj1) and any(
                    has_tags(child, obj2) for child in candidate.children):
                return run_query(candidate, obj1)
            return set()

        raise ValueError("Unsupported operator on tag")

    if isinstance(query, Tag):
        if not isinstance(candidate, query._tgm_class):
            return set()

        for item in query._tgm_test_attributes:
            if not hasattr(candidate, item):
                return set()

        for key, value in query._tgm_attributes.items():
            try:
                if getattr(candidate, key) != value:
                    return set()
            except AttributeError:
                return set()

        for subquery in query._tgm_children:
            if not any(has_tags(child, subquery)
                       for child in candidate.children):
                return set()

        for test in query._tgm_tests:
            if not test(candidate):
                return set()

        return {candidate}

    if isinstance(query, GameObject):
        return set()

    if isinstance(candidate, query):
        return {candidate}

    return set()


def has_tags(candidate, query):
    if query is candidate:
        return True

    simple_operations = {
        "&": operator.and_,
        "|": operator.or_,
        "^": operator.xor
    }

    if isinstance(query, TagGroup):
        operation = query.operation
        obj1 = query.obj1
        obj2 = query.obj2
        if operation in simple_operations:
            return simple_operations[operation](has_tags(candidate, obj1),
                                                has_tags(candidate, obj2))

        if operation == "-":
            if obj2 is None:
                return not has_tags(candidate, obj1)
            return has_tags(candidate, obj1) and not has_tags(candidate, obj2)

        if operation == "<":
            obj1, obj2 = obj2, obj1
            operation = ">"

        if operation == ">":
            if has_tags(candidate, obj2) and has_tags(candidate.parent, obj1):
                return True
            return has_tags(candidate, obj1) and any(
                    has_tags(child, obj2)
                    for child in candidate.children
            )

        raise ValueError("Unsupported operator on tag")

    if isinstance(query, Tag):
        if not isinstance(candidate, query._tgm_class):
            return False

        for item in query._tgm_test_attributes:
            if not hasattr(candidate, item):
                return False

        for key, value in query._tgm_attributes.items():
            try:
                if getattr(candidate, key) != value:
                    return False
            except AttributeError:
                return False

        for subquery in query._tgm_children:
            if not any(has_tags(child, subquery)
                       for child in candidate.children):
                return False

        for test in query._tgm_tests:
            if not test(candidate):
                return False

        return True

    if isinstance(query, GameObject):
        return False

    return isinstance(candidate, query)


class EventGroup(object):
    def __init__(self, namespace, **event_groups):
        events = set()
        for group in event_groups.values():
            for event in group:
                if event in events:
                    raise ValueError("event '{}' listed more than once".format(
                        event
                    ))
                events.add(event)
        self._events = frozenset(events)
        self._namespace = namespace + "_"

    def _validate_event(self, name):
        if not name.startswith(self._namespace):
            raise AttributeError(
                "event '{}' should start with '{}'".format(
                    name,
                    self._namespace
                )
            )

        if name[len(self._namespace):] not in self._events:
            raise AttributeError("event '{}' is not defined".format(name))

    def __call__(self, func):
        self._validate_event(func.__name__)

        def add_tag(entity, name):
            EventTag(entity, name, self)

        auto_call[func] = add_tag
        return func

    def __getattr__(self, event):
        self._validate_event(event)
        return EventTag["name":event, "group":self]


class Selection(object):
    def __init__(self, results):
        self._results = results

    def __iter__(self):
        yield from self._results

    def __getitem__(self, item):
        return list(self._results)[item]

    def __bool__(self):
        return bool(self._results)

    def __getattr__(self, item):
        return AttributeSelection([getattr(result, item)
                                   for result in self._results])

    def __repr__(self):
        return "Selection({!r})".format(self._results)


class AttributeSelection(object):
    def __init__(self, results):
        self._results = results

    def __iter__(self):
        yield from self._results

    def __call__(self, *args, **kwargs):
        rtn = []
        for result in self._results:
            rtn.append(result(*args, **kwargs))
        return rtn

    def __getattr__(self, item):
        return AttributeSelection([getattr(result, item)
                                   for result in self._results])


class TagStore(object):
    def __init__(self, owner):
        self.owner = ref(owner)

    def get_all(self, query, stop=None, abort=None):
        return Selection(get_all(self.owner(), query, stop, abort))

    def get_first(self, query, stop=None, abort=None):
        try:
            return next(iter(get_all(self.owner(), query, stop, abort)))
        except StopIteration:
            raise IndexError("No results found in get_first")

    def select(self, query, stop=None, abort=None, enabled_only=True):
        return Selection(select_all(
            self.owner(), query, stop, abort, enabled_only))

    def satisfies_query(self, query):
        return has_tags(self.owner, query)


class BaseTag(object):
    def __and__(self, other):
        return TagGroup(self, other, "&")

    def __or__(self, other):
        return TagGroup(self, other, "|")

    def __sub__(self, other):
        return TagGroup(self, other, "-")

    def __xor__(self, other):
        return TagGroup(self, other, "^")

    def __neg__(self):
        return TagGroup(GameObject, self, "-")

    def __gt__(self, other):
        return TagGroup(self, other, ">")

    def __lt__(self, other):
        return TagGroup(self, other, "<")


class Tag(BaseTag):
    def __init__(self, cls, attributes, test_attributes, children, tests):
        self._tgm_attributes = attributes.copy()
        self._tgm_test_attributes = test_attributes.copy()
        self._tgm_children = children
        self._tgm_class = cls
        self._tgm_tests = tests

    def __repr__(self):
        data = ""

        data += ", ".join(repr(child) for child in self._tgm_children)

        if data and self._tgm_test_attributes:
            data += ","

        data += ", ".join(repr(item) for item in self._tgm_test_attributes)

        if data and self._tgm_attributes:
            data += ","

        data += ", ".join(
            "{}={!r}".format(key, value)
            for key, value in self._tgm_attributes.items()
            if key is not "__class__"
        )

        return "Tag:{}({})".format(self._tgm_class.__name__, data)


class TagGroup(BaseTag):
    def __init__(self, obj1, obj2, operation):
        self.obj1 = obj1
        self.obj2 = obj2
        self.operation = operation

    def __repr__(self):
        if self.operation == "u-":
            return "(-{!r})".format(self.obj2)

        return "({!r} {} {!r})".format(self.obj1, self.operation, self.obj2)


class MetaGameObject(type, BaseTag):
    def __getitem__(cls, args):
        if not isinstance(args, tuple):
            args = (args,)

        attributes = {}
        test_attributes = []
        children = []
        tests = []

        for arg in args:
            if isinstance(arg, slice):
                if arg.step is not None:
                    raise ValueError(
                            "Too many colons in tag attribute assignment")
                if arg.start is None:
                    raise ValueError(
                            "Misplaced colon in tag attribute assignment")
                if not isinstance(arg.start, str):
                    raise ValueError("Tag attribute name must be a string")
                attributes[arg.start] = arg.stop
            elif isinstance(arg, str):
                test_attributes.append(arg)
            elif is_tag(arg) or isinstance(arg, GameObject):
                children.append(arg)
            else:
                tests.append(arg)

        return Tag(cls, attributes, test_attributes, children, tests)


class GameObject(object, metaclass=MetaGameObject):
    def __init__(self, parent, *args, **kwargs):
        if isinstance(parent, (list, tuple)):
            parent, *self._tgm_meta = parent
        else:
            self._tgm_meta = []

        self.init_args = args
        self.init_kwargs = kwargs
        self.children = set()
        self.tags = TagStore(self)
        self.disabled = False
        self._tgm_depth = 0
        game_objects.add(self)

        self.parent = parent

        class_dict = {}
        for cls in reversed(self.__class__.mro()):
            class_dict.update(cls.__dict__)

        for name, value in class_dict.items():
            if isinstance(value, collections.Hashable):
                if value in auto_call:
                    auto_call[value](self, name)

        if hasattr(self, "on_create"):
            self.on_create(*args, **kwargs)

    def destroy(self):
        destroyed_game_objects.add(self)
        for child in self.children.copy():
            child.destroy()
        self.on_destroy()
        if self.parent is not None:
            self.on_remove_child(self)
            self.parent.children.remove(self)

    def on_destroy(self):
        pass

    def on_add_child(self, child):
        pass

    def on_remove_child(self, child):
        pass

    @property
    def dir(self):
        return os.path.dirname(sys.modules[self.__class__.__module__].__file__)

    @property
    def computed_depth(self):
        if self.parent is None:
            return (self.depth,)
        return (self.depth,) + self.parent.computed_depth

    @property
    def depth(self):
        return self._tgm_depth

    @depth.setter
    def depth(self, value):
        from tgm.system import tgm_event
        self._tgm_depth = value
        self.tags.select(
            GameObject[tgm_event.tgm_depth_update]
        ).tgm_depth_update()

    @property
    def transform(self):
        from .transform import Transform
        if not hasattr(self, "_tgm_transform"):
            self._tgm_transform = Transform(self)
        return self._tgm_transform

    @property
    def x(self):
        return self.transform.x

    @x.setter
    def x(self, value):
        self.transform.x = value

    @property
    def y(self):
        return self.transform.y

    @y.setter
    def y(self, value):
        self.transform.y = value

    @property
    def rotation(self):
        return self.transform.rotation

    @rotation.setter
    def rotation(self, value):
        self.transform.rotation = value

    @property
    def x_scale(self):
        return self.transform.x_scale

    @x_scale.setter
    def x_scale(self, value):
        self.transform.x_scale = value

    @property
    def y_scale(self):
        return self.transform.y_scale

    @y_scale.setter
    def y_scale(self, value):
        self.transform.y_scale = value

    def collisions(self, query=None):
        from tgm.system import tgm_event

        if query is None:
            query = GameObject

        return set(x for y in self.tags.select(
            GameObject[tgm_event.tgm_get_collisions]
        ).tgm_get_collisions(query) for x in y)

    @property
    def parent(self):
        return self._tgm_parent

    @parent.setter
    def parent(self, parent):
        update = hasattr(self, "parent")

        if getattr(self, "parent", None) is not None:
            self.parent.on_remove_child(self)
            self.parent.children.remove(self)
        self._tgm_parent = parent
        if parent is not None:
            parent.children.add(self)
            self.parent.on_add_child(self, *self._tgm_meta)

        if update:
            from tgm.system import tgm_event
            self.tags.select(
                GameObject[tgm_event.tgm_ancestor_update],
                enabled_only=False
            ).ancestor_update()


class EventTag(GameObject):
    def on_create(self, name, group):
        self.name = name
        self.group = group


class Group(GameObject):
    pass
