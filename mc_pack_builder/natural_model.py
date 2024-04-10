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
import copy
import json
from nbtlib import serialize_tag
import nbtlib.tag as nbt  # included for later usage, e.g., one may want to write model.field = nbt.Byte(3)


def py2nbt(obj) -> nbt.Base:
    if isinstance(obj, nbt.Base):
        return obj
    if isinstance(obj, int):
        return nbt.Int(obj)
    if isinstance(obj, str):
        return nbt.String(obj)
    if isinstance(obj, bool):
        return nbt.Byte(int(obj))

    if isinstance(obj, Box):
        return py2nbt(obj.data)

    if isinstance(obj, NaturalModel):
        return py2nbt(obj.dump())

    if isinstance(obj, list):
        result = []
        for each in obj:
            result.append(py2nbt(each))
        return nbt.List(result)

    if isinstance(obj, dict):
        result = nbt.Compound()
        for key, value in obj.items():
            result[key] = py2nbt(value)
        return result
    raise NotImplementedError(type(obj))


class Box:
    """
    mimic a pointer in python.
    This can be used to make a lazy string for the commands and configuration
    """
    def __init__(self, data=None, get_cast=lambda x: x, set_cast=lambda x: x):
        self._data = data
        self._get_cast = get_cast
        self._set_cast = set_cast

    @property
    def data(self):
        return self._get_cast(self._data)

    @data.setter
    def data(self, value):
        self._data = self._set_cast(value)

    def simplify(self):
        return Box(self.data)

    def __call__(self, *args, **kwargs):
        return self.data(*args, **kwargs)

    def __str__(self):
        return str(self.data)

    def __add__(self, other):
        return Box(get_cast=lambda _: self.data + other)

    def __radd__(self, other):
        return Box(get_cast=lambda _: other + self.data)

    def __sub__(self, other):
        return Box(get_cast=lambda _: self.data - other)

    def __rsub__(self, other):
        return Box(get_cast=lambda _: other - self.data)


class NaturalModel:
    """
    The base class of load and dump
    """
    def load(self, obj):
        """
        load from python object

        :param obj:
        :return:
        """
        pass

    def dump(self):
        """
        dump to python object
        :return:
        """
        pass

    def to_json(self, indent=0, ensure_ascii=False):
        """
        dump to json string

        :param indent:
        :param ensure_ascii:
        :return:
        """
        data = self.dump()
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

    def dump_nbt(self):
        """
        dump to nbt object

        :return:
        """
        data = self.dump()
        return py2nbt(data)

    def to_nbt(self):
        """
        dump to nbt string

        :return:
        """
        return serialize_tag(self.dump_nbt())


class Field(NaturalModel):
    """
    To access model data more easily
    """
    def __init__(self, name=None, default=None, cast=None):
        self.name = name
        self.default = default
        if cast is not None:
            self.cast = cast

    def cast(self, x):
        return x

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not isinstance(instance, DictModel):
            raise TypeError("Only allowed to use on DictModel")
        return instance.get(self.name, self.default)

    def __set__(self, instance, value):
        value = self.cast(value)
        if not isinstance(instance, DictModel):
            raise TypeError("Only allowed to use on DictModel")
        instance.set(self.name, value)


class IntField(Field):
    def cast(self, x):
        return int(x)


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
            parent[key] = copy.deepcopy(default)
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
