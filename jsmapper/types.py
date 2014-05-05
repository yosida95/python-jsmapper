# -*- coding: utf-8 -*-

from .schema import (
    JSONSchema,
    JSONSchemaBase,
    Property,
)
from .mapping import (
    Mapping,
    MappingProperty,
)

NoneType = type(None)

__all__ = [
    'Array', 'Boolean', 'Integer', 'Number', 'Null', 'Object', 'String'
]


class PrimitiveType(JSONSchemaBase):

    def bind(self, obj):
        return obj

    def to_dict(self):
        return super().to_dict(lambda: dict(type=self.__name__))

    def is_primitive(self):
        return True


class Array(PrimitiveType):
    __name__ = 'array'

    items = Property('items', (JSONSchema, list, NoneType))
    additional_items = Property('additionalItems', bool, True)
    max_items = Property('maxItems', (int, NoneType))
    min_items = Property('minItems', (int, NoneType))
    unique_items = Property('uniqueItems', bool, False)

    def __init__(self,
                 items=None, additional_items=True,
                 max_items=None, min_items=None, unique_items=False):
        self.items = items
        self.additional_items = additional_items
        self.max_items = max_items
        self.min_items = min_items
        self.unique_items = unique_items

    def bind(self, obj):
        if isinstance(self.items, JSONSchema):
            return [self.items.bind(item) for item in obj]
        elif isinstance(self.items, list):
            result = [schema.bind(item)
                      for schema, item in zip(self.items, obj)]
            result.extend(obj[len(self.items):])
            return result

        return super().bind(obj)


class Boolean(PrimitiveType):
    __name__ = 'boolean'


class Numeric(PrimitiveType):
    multiple_of = Property('multipleOf', (int, NoneType), None)
    maximum = Property('maximum', (int, NoneType), None)
    exclusive_maximum = Property('exclusiveMaximum', bool, False)
    minimum = Property('minimum', (int, NoneType), None)
    exclusive_minimum = Property('exclusiveMinimum', bool, False)

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
        if isinstance(v, type) and issubclass(v, Mapping):
            return True
        elif isinstance(v, dict):
            return all(
                isinstance(key, str) and isinstance(
                    value, (dict, JSONSchema, MappingProperty)
                )
                for key, value in v.items()
            )

        return False

    def required_to_dict(properties):
        result = []
        for prop in properties:
            if isinstance(prop, MappingProperty):
                prop = prop.name

            result.append(prop)
        return result

    def properties_to_dict(value):
        if isinstance(value, type) and issubclass(value, Mapping):
            return value._to_dict()

        for key, schema in value.items():
            if isinstance(schema, MappingProperty):
                schema = schema.schema

            if isinstance(schema, JSONSchema):
                value[key] = schema.to_dict()

        return value

    def dependencies_to_dict(value):
        dependencies = {}
        for key, dependency in value.items():
            if isinstance(key, MappingProperty):
                key = key.name
            elif not isinstance(key, str):
                raise ValueError()

            if isinstance(dependency, list):
                for x in range(len(dependency)):
                    value = dependency[x]

                    if isinstance(value, MappingProperty):
                        value = value.name
                    elif not isinstance(value, str):
                        raise ValueError()

                    dependency[x] = value
            elif isinstance(dependency, (MappingProperty, JSONSchema)):
                if isinstance(dependency, MappingProperty):
                    dependency = dependency.schema
                dependency = dependency.to_dict()
            else:
                raise ValueError()

            dependencies[key] = dependency

        return dependencies

    max_properties = Property('maxProperties', (int, NoneType))
    min_properties = Property('minProperties', (int, NoneType))
    required = Property('required', list, [], required_to_dict)
    additional_properties = Property('additionalProperties', bool, True)
    properties = Property('properties', is_valid_property, {},
                          properties_to_dict)
    pattern_properties = Property('patternProperties', dict, {})
    dependencies = Property('dependencies', dict, {}, dependencies_to_dict)

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

    max_length = Property('maxLength', (int, NoneType), None)
    min_length = Property('minLength', (int, NoneType), None)
    pattern = Property('pattern', (str, NoneType), None)

    def __init__(self, max_length=None, min_length=None, pattern=None):
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
