# -*- coding: utf-8 -*-

from . import Mapping

NoneType = type(None)


class PrimitiveType:

    def bind(self, obj):
        return obj


class Array(PrimitiveType):
    __name__ = 'array'

    def __init__(self,
                 items=None, additional_items=True,
                 max_items=None, min_items=None, unique_items=False):
        assert isinstance(items, ())
        assert isinstance(additional_items, bool)
        assert isinstance(max_items, (int, NoneType))
        assert isinstance(min_items, (int, NoneType))
        assert isinstance(unique_items, bool)

        self.items = items
        self.additional_items = additional_items
        self.max_items = max_items
        self.min_items = min_items
        self.unique_items = unique_items


class Boolean(PrimitiveType):
    __name__ = 'boolean'


class Numeric(PrimitiveType):

    def __init__(self,
                 multiple_of=None, maximum=None, exclusive_maximum=False,
                 minimum=None, exclusive_minimum=False):
        assert isinstance(multiple_of, (int, NoneType))
        assert isinstance(maximum, (int, NoneType))
        assert isinstance(exclusive_maximum, bool)
        assert isinstance(minimum, (int, NoneType))
        assert isinstance(exclusive_minimum, (int, NoneType))

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

    def __init__(self,
                 max_properties=None, min_properties=None, required=[],
                 additional_properties=True, properties={},
                 pattern_properties={}, dependencies={}):
        assert isinstance(max_properties, (int, NoneType))
        assert isinstance(min_properties, (int, NoneType))
        assert isinstance(required, list)
        assert isinstance(additional_properties, bool)
        assert isinstance(properties, dict) or issubclass(properties, Mapping)
        assert isinstance(pattern_properties, dict)
        assert isinstance(dependencies, dict)

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

    def __init__(self, max_length=None, min_length=None, pattern=None):
        assert isinstance(max_length, (int, NoneType))
        assert isinstance(min_length, (int, NoneType))
        assert isinstance(pattern, (str, NoneType))

        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
