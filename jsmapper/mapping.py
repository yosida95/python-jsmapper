# -*- coding: utf-8 -*-

from .schema import JSONSchema

__all__ = ['Mapping', 'object_property']


class MappingProperty:

    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    def new(self, name):
        return Value(self, name)

    def bind(self, obj):
        # validation will not be executed
        if self.schema.type is None:
            return obj

        return self.schema.type.bind(obj)


def object_property(name):
    def receive(func):
        return MappingProperty(name, func())
    return receive


class Value:

    def __init__(self, schema, name):
        assert isinstance(schema, MappingProperty)
        assert isinstance(name, str)

        self.schema = schema
        self.name = name

    def __get__(self, inst, owner):
        if inst is None:
            return self.schema

        return inst.__dict__.get(self.name)

    def __set__(self, inst, value):
        inst.__dict__[self.name] = value

    def bind(self, inst, obj):
        return self.__set__(inst, self.schema.bind(obj))


class MappingMeta(type):

    def __new__(cls, name, bases, namespace):
        for key, value in namespace.items():
            if not isinstance(value, (JSONSchema, MappingProperty)):
                continue

            if isinstance(value, JSONSchema):
                value = MappingProperty(key, value)

            namespace[key] = value.new(value.name)

        return super().__new__(cls, name, bases, namespace)


class Mapping(metaclass=MappingMeta):

    @classmethod
    def _properties(cls):
        for base in cls.__mro__:
            for key, value in vars(base).items():
                if not isinstance(value, Value):
                    continue
                elif cls is not base and getattr(cls, key) is not value.schema:
                    continue

                yield value

    @classmethod
    def _bind(cls, obj):
        # TODO: support custom constructor
        inst = cls()

        for value in cls._properties():
            if value.name not in obj:
                continue

            value.bind(inst, obj.get(value.name))

        return inst

    @classmethod
    def _to_dict(self):
        return {
            value.schema.name: value.schema.schema.to_dict()
            for value in self._properties()
        }
