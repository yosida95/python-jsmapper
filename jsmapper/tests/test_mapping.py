# -*- coding: utf-8 -*-

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

    assert isinstance(prop, MappingProperty)
    assert prop.name == 'property'
    assert prop.schema == schema


class Base(Mapping):
    foo = JSONSchema(type=Integer())
    bar = JSONSchema(type=Integer())


class Extended(Base):
    foo = JSONSchema(type=Integer())
    baz = JSONSchema(type=String())


def test_inheritance():
    assert {Base.foo, Base.bar} \
        == set(prop.schema for prop in Base._properties())
    assert {Extended.foo, Extended.bar, Extended.baz} \
        == set(prop.schema for prop in Extended._properties())
