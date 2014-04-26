# -*- coding: utf-8 -*-


__all__ = ['JSONSchema', 'Mapping', 'object_property']


class Value:

    def __init__(self, schema, name):
        assert isinstance(schema, NamedJSONSchema)
        assert isinstance(name, str)

        self.schema = schema
        self.name = name

    def __get__(self, inst, owner):
        if inst is None:
            return self.schema.schema

        return inst.__dict__[self.name]

    def __set__(self, inst, value):
        inst.__dict__[self.name] = value


class JSONSchema:

    def __init__(self, title=None, description=None, default=None,
                 type=None, all_of=None, any_of=None, one_of=None, not_=None,
                 format=None):  # difinitions
        # metadata
        self.title = title
        self.description = description
        self.default = default

        # general validators
        self.type = type
        self.all_of = all_of
        self.any_of = any_of
        self.one_of = one_of
        self.not_ = not_

        # semantic validation
        self.format = format

    def bind(self, obj):
        # TODO: validate and handle exception
        return self.type.bind(obj)


class NamedJSONSchema(JSONSchema):

    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    def new(self, name):
        return Value(self, name)


def object_property(name):
    def receive(func):
        return NamedJSONSchema(name, func())
    return receive


class MappingMeta(type):

    def __new__(cls, name, bases, namespace):
        registry = {}

        for key, value in namespace.items():
            if not isinstance(value, JSONSchema):
                continue

            if not isinstance(value, NamedJSONSchema):
                value = NamedJSONSchema(key, value)

            namespace[key] = value.new(value.name)
            registry[key] = value

        return super().__new__(cls, name, bases, namespace)


class Mapping(metaclass=MappingMeta):

    @classmethod
    def _bind(cls, obj):
        # TODO: support custom constructor
        inst = cls()

        for key, value in vars(cls).items():
            if not isinstance(value, Value):
                continue

            setattr(inst, key, obj.get(value.name))

        return inst
