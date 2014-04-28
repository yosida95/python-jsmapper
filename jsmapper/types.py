# -*- coding: utf-8 -*-

from . import Mapping

NoneType = type(None)

__all__ = [
    'Array', 'Boolean', 'Integer', 'Number', 'Null', 'Object', 'String'
]


class TypeAttribute:

    def __init__(self, property_name, types, default=None):
        assert isinstance(property_name, str)
        assert isinstance(types, (tuple, type)) or callable(types)

        self.property_name = property_name
        self.types = types
        self.default = default

    def set_member_name(self, value):
        self.member_name = value

    def __get__(self, inst, owner):
        if inst is None:
            return self

        return inst.__dict__.get(self.member_name)

    def __set__(self, inst, value):
        if isinstance(self.types, (tuple, type)):
            assert isinstance(value, self.types)
        else:
            assert self.types(value)

        inst.__dict__[self.member_name] = value


class PrimitiveTypeMeta(type):

    def __new__(cls, name, bases, namespace):
        for key, value in namespace.items():
            if isinstance(value, TypeAttribute):
                value.set_member_name(key)

        return super().__new__(cls, name, bases, namespace)


class PrimitiveType(metaclass=PrimitiveTypeMeta):

    def bind(self, obj):
        return obj


class Array(PrimitiveType):
    __name__ = 'array'

    items = TypeAttribute('items', (list, NoneType))
    additional_items = TypeAttribute('additionalItems', bool, True)
    max_items = TypeAttribute('maxItems', (int, NoneType))
    min_items = TypeAttribute('minItems', (int, NoneType))
    unique_items = TypeAttribute('uniqueItems', bool, False)

    def __init__(self,
                 items=None, additional_items=True,
                 max_items=None, min_items=None, unique_items=False):
        self.items = items
        self.additional_items = additional_items
        self.max_items = max_items
        self.min_items = min_items
        self.unique_items = unique_items


class Boolean(PrimitiveType):
    __name__ = 'boolean'


class Numeric(PrimitiveType):
    multiple_of = TypeAttribute('multipleOf', (int, NoneType), None)
    maximum = TypeAttribute('maximum', (int, NoneType), None)
    exclusive_maximum = TypeAttribute('exclusiveMaximum', bool, False)
    minimum = TypeAttribute('minimum', (int, NoneType), None)
    exclusive_minimum = TypeAttribute('exclusiveMinimum', bool, False)

    def __init__(self,
                 multiple_of=None, maximum=None, exclusive_maximum=False,
                 minimum=None, exclusive_minimum=False):
        self.multiple_of = multiple_of
        self.maximum = maximum
        self.exclusive_maximum = exclusive_maximum
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum


class Integer(Numeric):
    __name__ = 'integer'


class Number(Numeric):
    __name__ = 'number'


class Null(PrimitiveType):
    __name__ = 'null'


class Object(PrimitiveType):
    __name__ = 'object'

    def is_valid_property(v):
        return isinstance(v, dict)\
            or isinstance(v, type) and issubclass(v, Mapping)

    max_properties = TypeAttribute('maxProperties', (int, NoneType))
    min_properties = TypeAttribute('minProperties', (int, NoneType))
    required = TypeAttribute('required', list, [])
    additional_properties = TypeAttribute('additionalProperties', bool, True)
    properties = TypeAttribute('properties', is_valid_property, {})
    pattern_properties = TypeAttribute('patternProperties', dict, {})
    dependencies = TypeAttribute('dependencies', dict, {})

    def __init__(self,
                 max_properties=None, min_properties=None, required=[],
                 additional_properties=True, properties={},
                 pattern_properties={}, dependencies={}):
        self.max_properties = max_properties
        self.min_properties = min_properties
        self.required = required
        self.additional_properties = additional_properties
        self.properties = properties
        self.pattern_properties = pattern_properties
        self.dependencies = dependencies

    def bind(self, obj):
        if isinstance(self.properties, (dict, NoneType)):
            return super().bind(obj)

        return self.properties._bind(obj)


class String(PrimitiveType):
    __name__ = 'string'

    max_length = TypeAttribute('maxLength', (int, NoneType), None)
    min_length = TypeAttribute('minLength', (int, NoneType), None)
    pattern = TypeAttribute('pattern', (str, NoneType), None)

    def __init__(self, max_length=None, min_length=None, pattern=None):
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
