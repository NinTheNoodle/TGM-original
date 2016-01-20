import operator
import weakref
from functools import partial

no_default = object()


def get_all(candidate, query, stop=None):
    rtn = run_query(candidate, query)
    if rtn:
        return rtn

    if candidate.parent is None:
        return set()

    if stop is not None and has_tags(candidate, stop):
        return set()

    return get_all(candidate.parent, query)


def select_all(candidate, query, stop=None):
    rtn = set()

    rtn.update(run_query(candidate, query))

    if stop is not None and has_tags(candidate, stop):
        return rtn

    for child in candidate.children:
        rtn.update(select_all(child, query))

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
            if getattr(candidate, key, no_default) != value:
                return set()

        for subquery in query._tgm_children:
            if not any(has_tags(child, subquery)
                       for child in candidate.children):
                return set()

        return {candidate}

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
            if getattr(candidate, key, no_default) != value:
                return False

        for subquery in query._tgm_children:
            if not any(has_tags(child, subquery)
                       for child in candidate.children):
                return False

        return True

    return isinstance(candidate, query)


class Feature(object):
    pass


class EventGroup(object):
    def __init__(self, *events):
        self._events = frozenset(events)

    def __call__(self, func):
        func_name = func.__name__

        if func_name not in self._events:
            raise AttributeError("event '{}' is not defined".format(func_name))

        return EventMethod(func, self)

    def __getattr__(self, event):
        if event not in self._events:
            raise AttributeError("event '{}' is not defined".format(event))

        return EventTag["name":event, "group":self]


class EventMethod(Feature):
    """
    Substitute for a normal Python method
    automatically tags its own existence
    """
    def __init__(self, function, group):
        self.function = function
        self.group = group

    def init(self, instance):
        EventTag(instance, self.function.__name__, self.group)

    def __get__(self, instance, owner):
        return partial(self.function, instance)


class Selection(object):
    def __init__(self, results):
        self._results = results

    def __iter__(self):
        yield from self._results

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
        self.owner = owner

    def get_all(self, query, stop=None):
        return Selection(get_all(self.owner, query, stop))

    def get_first(self, query, stop=None):
        try:
            return next(iter(get_all(self.owner, query, stop)))
        except StopIteration:
            raise IndexError("No results found in get_first")

    def select(self, query):
        return Selection(select_all(self.owner, query))

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
    def __init__(self, cls, attributes, test_attributes, children):
        self._tgm_attributes = attributes.copy()
        self._tgm_test_attributes = test_attributes.copy()
        self._tgm_children = children
        self._tgm_class = cls

    def __repr__(self):
        return "Tag:{}({}{}{}{}{})".format(
                self._tgm_class.__name__,
                ", ".join(repr(child) for child in self._tgm_children),
                ", "
                if self._tgm_children and self._tgm_test_attributes else "",
                ", ".join(repr(item) for item in self._tgm_test_attributes),
                ", "
                if self._tgm_test_attributes and self._tgm_attributes else "",
                ", ".join(
                        "{}={!r}".format(key, value)
                        for key, value in self._tgm_attributes.items()
                        if key is not "__class__"
                )
        )


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
            else:
                children.append(arg)

        return Tag(cls, attributes, test_attributes, children)


class GameObject(object, metaclass=MetaGameObject):
    def __init__(self, parent, *args, **kwargs):
        self.children = set()
        self.tags = TagStore(self)
        self.features = []
        self.parent = parent

        class_dict = {}
        for cls in reversed(self.__class__.mro()):
            class_dict.update(cls.__dict__)

        for name, value in class_dict.items():
            if isinstance(value, Feature):
                self.features.append(value)

        self.init_args = args
        self.init_kwargs = kwargs

        for feature in self.features:
            if hasattr(feature, "init"):
                feature.init(self)

        if hasattr(self, "create"):
            self.create(*args, **kwargs)

    def destroy(self):
        for feature in self.features:
            if hasattr(feature, "destroy"):
                feature.destroy(self)

    @property
    def parent(self):
        return self._tgm_parent

    @parent.setter
    def parent(self, parent):
        update = hasattr(self, "parent")

        if getattr(self, "parent", None) is not None:
            self.parent.children.remove(self)
        self._tgm_parent = parent
        if parent is not None:
            parent.children.add(self)

        if update:
            from tgm.common import sys_event
            self.tags.select(
                    GameObject[sys_event.ancestor_update]
            ).ancestor_update()


class EventTag(GameObject):
    def create(self, name, group):
        self.name = name
        self.group = group

