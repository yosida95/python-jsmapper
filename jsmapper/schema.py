# -*- coding: utf-8 -*-

import jsonschema

from .exceptions import ValidationError

__all__ = ['JSONSchema']

NoneType = type(None)


class Property:

    def __init__(self, property_name, types=None, default=None, to_dict=None):
        assert isinstance(property_name, str)
        assert isinstance(types, (tuple, type, NoneType)) or callable(types)
        assert isinstance(to_dict, NoneType) or callable(to_dict)

        self.property_name = property_name
        self.types = types
        self.default = default
        self.to_dict_func = to_dict

    def to_dict(self, value):
        if self.to_dict_func:
            return self.to_dict_func(value)
        elif isinstance(value, JSONSchemaBase):
            return value.to_dict()

        return value

    def set_member_name(self, value):
        self.member_name = value

    def __get__(self, inst, owner):
        if inst is None:
            return self

        return inst.__dict__.get(self.member_name)

    def __set__(self, inst, value):
        if isinstance(self.types, (tuple, type)):
            assert isinstance(value, self.types)
        elif callable(self.types):
            assert self.types(value)

        inst.__dict__[self.member_name] = value


class JSONSchemaMeta(type):

    def __init__(cls, name, bases, namespace):
        for key, value in vars(cls).items():
            if not isinstance(value, Property):
                continue

            value.set_member_name(key)

        return super().__init__(name, bases, namespace)


class JSONSchemaBase(metaclass=JSONSchemaMeta):

    def to_dict(self, base=dict):
        dct = base()

        for base in self.__class__.__mro__:
            for attr in vars(base).values():
                if not isinstance(attr, Property):
                    continue

                value = attr.to_dict(getattr(self, attr.member_name))
                if value == attr.default:
                    continue

                dct[attr.property_name] = value

        return dct

    def is_primitive(self):
        return False


class JSONSchema(JSONSchemaBase):

    def is_valid_type(v):
        return isinstance(v, JSONSchemaBase) and v.is_primitive()\
            or isinstance(v, NoneType)

    schema = Property('$schema', str, "")
    title = Property('title', str, "")
    description = Property('description', str, "")
    default = Property('default')
    ref = Property('$ref', str, "")

    enum = Property("enum", (list, NoneType))
    type = Property('type', is_valid_type)
    all_of = Property('allOf', (list, NoneType))
    any_of = Property('anyOf', (list, NoneType))
    one_of = Property('oneOf', (list, NoneType))
    not_ = Property('not', lambda v: isinstance(v, (JSONSchema, NoneType)))

    format = Property('format', str, "")

    def __init__(self,
                 schema="", title="", description="", default=None, ref="",
                 enum=None, type=None, all_of=None, any_of=None, one_of=None,
                 not_=None, format=""):  # difinitions
        # metadata
        self.schema = schema
        self.title = title
        self.description = description
        self.default = default
        self.ref = ref

        # general validators
        self.enum = enum
        self.type = type
        self.all_of = all_of
        self.any_of = any_of
        self.one_of = one_of
        self.not_ = not_

        # semantic validation
        self.format = format

    def bind(self, obj, *args, **kwargs):
        self.validate(obj, *args, **kwargs)
        return self.type.bind(obj)

    def validate(self, obj, *args, **kwargs):
        try:
            jsonschema.validate(obj, self.to_dict(), *args, **kwargs)
        except jsonschema.ValidationError as why:
            raise ValidationError() from why

    def to_dict(self):
        dct = super().to_dict()
        if self.type:
            dct.update(dct['type'])

        return dct
