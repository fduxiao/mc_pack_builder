"""
Let's think about a python class defined as follows.

class A:
    a = 1
    b = 2


There isn't any easy way to save or load it to/from json/nbt/bson. But I only use
basic datatype here. Naturally, we want to serialize an instance of A as `{"a": 1, "b": 2}`.
A solution is to make a dump/load function of A so that we are able to serialize a class like that.
It is a bit tiring to always add those dump/load functions, e.g., is there any good way to add the
fields while the dump/load functions are automatically added? The answer is to use __set__ and __get__!

I call such a class a :py:class:`NaturalModel`, which should be compatible with basic python objects,
which are further compatible with json or nbt. In general, a natural model is a dict with the obvious
dump/load, while some fields with __set__ and __get__ provided to access those data easily. Again,
a natural model may also be a field of another dict, so it's quite natural to build it from the reference.
"""


class NaturalModel:
    """
    The base class of load and dump
    """
    def load(self, obj):
        pass

    def dump(self):
        pass


class Field(NaturalModel):
    """
    To access model data more easily
    """
    def __init__(self, name=None, default=None):
        self.name = name
        self.default = default

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not isinstance(instance, DictModel):
            raise TypeError("Only allowed to use on DictModel")
        return instance.get(self.name, self.default)

    def check_value(self, value) -> bool:
        return True

    def __set__(self, instance, value):
        if not isinstance(instance, DictModel):
            raise TypeError("Only allowed to use on DictModel")
        if not self.check_value(value):
            raise ValueError(f"{value} is not allowed for {type(self)}")
        instance.set(self.name, value)


class IntField(Field):
    def check_value(self, value) -> bool:
        return isinstance(value, int)


class DictModel(NaturalModel):
    """
    Of course
    """
    def __init__(self, *, data=None, name=None):
        if data is None:
            data = dict()
        self.dict = data
        self.name = name

    def parse_path(self, path: str):
        path = path.split('/')
        parent = self.dict
        while True:
            if len(path) == 1:
                return parent, path[0]
            prefix = path.pop(0)
            if prefix not in parent:
                parent[prefix] = dict()
            parent = parent[prefix]

    def __getitem__(self, item):
        return self.dict[item]

    def get(self, key, default=None):
        parent, key = self.parse_path(key)
        if key not in parent:
            parent[key] = default
        return parent[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def set(self, key, value):
        parent, key = self.parse_path(key)
        parent[key] = value
        return value

    def dump(self):
        return self.dict

    def load(self, obj: dict):
        self.dict = obj

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not isinstance(instance, DictModel):
            raise TypeError("Only allowed to use on DictModel")
        if self.name not in instance.dict:
            instance.dict[self.name] = dict()
        return type(self)(data=instance.dict[self.name])

    def __set__(self, instance, value):
        if not isinstance(instance, DictModel):
            raise TypeError("Only allowed to use on DictModel")
        if isinstance(value, DictModel):
            value = value.dict
        instance.dict[self.name] = value
