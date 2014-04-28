# -*- coding: utf-8 -*-

__all__ = ['Reference', 'JSONSchema']

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

    def __new__(cls, name, bases, namespace):
        for key, value in namespace.items():
            if isinstance(value, Property):
                value.set_member_name(key)

        return super().__new__(cls, name, bases, namespace)


class JSONSchemaBase(metaclass=JSONSchemaMeta):

    def to_dict(self, base=dict):
        dct = base()
        dct.update({
            attr.property_name: value
            for attr, value in (
                (attr, attr.to_dict(getattr(self, attr.member_name)))
                for attr in vars(self.__class__).values()
                if isinstance(attr, Property)
            )
            if value != attr.default
        })
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

    type = Property('type', is_valid_type)
    all_of = Property('allOf', (list, NoneType))
    any_of = Property('anyOf', (list, NoneType))
    one_of = Property('oneOf', (list, NoneType))
    not_ = Property('not', lambda v: isinstance(v, (JSONSchema, NoneType)))

    format = Property('format', str, "")

    def __init__(self, schema="", title="", description="", default=None,
                 type=None, all_of=None, any_of=None, one_of=None, not_=None,
                 format=""):  # difinitions
        # metadata
        self.schema = schema
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

    def to_dict(self):
        dct = super().to_dict()
        if self.type:
            dct.update(dct['type'])

        return dct


class Reference(JSONSchemaBase):

    url = Property('$ref', str)

    def __init__(self, url):
        self.url = url