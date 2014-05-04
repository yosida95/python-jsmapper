# -*- coding: utf-8 -*-

from nose.tools import (
    eq_,
    ok_,
)

from ..mapping import (
    Mapping,
    MappingProperty,
    object_property,
)
from ..schema import JSONSchema
from ..types import (
    Integer,
    String,
)


def test_object_property():
    schema = JSONSchema()

    @object_property(name='property')
    def prop():
        return schema

    ok_(isinstance(prop, MappingProperty))
    eq_(prop.name, 'property')
    eq_(prop.schema, schema)


class Base(Mapping):
    foo = JSONSchema(type=Integer())
    bar = JSONSchema(type=Integer())


class Extended(Base):
    foo = JSONSchema(type=Integer())
    baz = JSONSchema(type=String())


def test_inheritance():
    eq_({Base.foo, Base.bar},
        set(prop.schema for prop in Base._properties()))
    eq_({Extended.foo, Extended.bar, Extended.baz},
        set(prop.schema for prop in Extended._properties()))
