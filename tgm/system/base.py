import operator
import weakref
from functools import partial

no_default = object()


class Feature(object):
    pass


class TagAttribute(Feature):
    def __init__(self, setter=lambda x: x, default=no_default):
        self.data = {}
        self.setter = setter
        self.default = default

    def __get__(self, instance, owner):
        if self.default is not no_default:
            return self.data.get(instance, self.default)

        try:
            return self.data[instance]
        except KeyError:
            raise AttributeError("TagAttribute accessed before assigned to")

    def __set__(self, instance, value):
        value = self.setter(value)

        if instance in self.data:
            instance.tags.index.remove((self, self.data[instance]))

        self.data[instance] = value
        instance.tags.index.add((self, value))


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

        return EventTag(name=event, group=self)


class EventMethod(Feature):
    """
    Substitute for a normal Python method
    automatically tags its own existence
    """
    def __init__(self, function, group):
        self.function = function
        self.group = group

    def init(self, instance):
        EventTag(parent=instance, name=self.function.__name__, group=self.group)

    def __get__(self, instance, owner):
        return partial(self.function, instance)


class Parent(Feature):
    def __init__(self):
        self.parents = weakref.WeakKeyDictionary()

    def __get__(self, instance, cls):
        try:
            return self.parents[instance]
        except KeyError:
            raise AttributeError("'{}' has no parent".format(instance))

    def destroy(self, instance):
        self.parents[instance].children.remove(instance)

    def __set__(self, instance, parent):
        if self.parents.get(instance, None) is not None:
            self.parents[instance].children.remove(instance)

        self.parents[instance] = parent

        if parent is not None:
            parent.children.add(instance)


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
        self.child_tags = {}
        self.index = set()

    def get(self, query, stop=None):
        if self.satisfies_query(query):
            return self.owner

        try:
            parent = self.owner.parent
        except AttributeError:
            raise IndexError("top of tree reached without match")

        if self.satisfies_query(stop):
            raise ValueError("stop query fulfilled before a match was found")

        return parent.tags.get(query)

    def select(self, query):
        return Selection(self._select(query))

    def _select(self, query):
        test = self.owner
        rtn = set()

        if test.tags.satisfies_query(query):
            rtn.add(test)

        for child in test.children:
            rtn.update(child.tags._select(query))

        return rtn

    def _compare_tags(self, tag_obj1, tag_obj2, operation):
        if tag_obj1.__class__ != tag_obj2.__class__:
            return False

        return operation(tag_obj1.tags.index, tag_obj2.tags.index)

    def satisfies_query(self, query):
        if query in (True, False, None):
            return bool(query)

        if isinstance(query, GameObjectGroup):
            if query.obj2 is not None:
                return query.operation(
                    self.satisfies_query(query.obj1),
                    self.satisfies_query(query.obj2)
                )
            else:
                return query.operation(
                    self.satisfies_query(query.obj1)
                )

        for child in self.owner.children:
            if (child.__class__ == query.__class__ and
                    child.tags.index >= query.tags.index):
                return True

        return False


class GameObject(object):
    parent = Parent()

    def __init__(self, *args, **kwargs):
        self.children = set()
        self.tags = TagStore(self)
        self.features = []

        set_features = {}

        class_dict = {}
        for cls in reversed(self.__class__.mro()):
            class_dict.update(cls.__dict__)

        for name, value in class_dict.items():
            if isinstance(value, Feature):
                self.features.append(value)
                if name in kwargs:
                    set_features[name] = kwargs.pop(name)

        self.init_args = args
        self.init_kwargs = kwargs

        for feature in self.features:
            if hasattr(feature, "init"):
                feature.init(self)

        for name, value in set_features.items():
            setattr(self, name, value)

        if hasattr(self, "init"):
            self.init(*args, **kwargs)

    def destroy(self):
        for feature in self.features:
            if hasattr(feature, "destroy"):
                feature.destroy(self)

    def __and__(self, other):
        if isinstance(other, GameObject):
            return GameObjectGroup(self, other, operator.and_)
        raise NotImplemented()

    def __or__(self, other):
        if isinstance(other, GameObject):
            return GameObjectGroup(self, other, operator.or_)
        raise NotImplemented()

    def __sub__(self, other):
        if isinstance(other, GameObject):
            return GameObjectGroup(self, other, operator.sub)
        raise NotImplemented()

    def __xor__(self, other):
        if isinstance(other, GameObject):
            return GameObjectGroup(self, other, operator.xor)
        raise NotImplemented()

    def __neg__(self):
        return GameObjectGroup(self, None, operator.not_)

    def __gt__(self, other):
        if isinstance(other, GameObject) or other is True:
            return GameObjectGroup(self, other, operator.gt)

    def __lt__(self, other):
        if isinstance(other, GameObject) or other is True:
            return GameObjectGroup(self, other, operator.lt)


class EventTag(GameObject):
    name = TagAttribute()
    group = TagAttribute()


class GameObjectGroup(GameObject):
    def init(self, obj1, obj2, operation):
        self.obj1 = obj1
        self.obj2 = obj2
        self.operation = operation

    @property
    def parent(self):
        return None

    @parent.setter
    def parent(self, value):
        raise AttributeError(
            "'GameObjectGroup' object cannot have a parent set")
