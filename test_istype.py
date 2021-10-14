from types import NoneType
from istype import istype


def test_simple_types():

    assert istype(42, int)
    assert istype("lorem ipsum", str)
    assert istype(None, NoneType)
    assert istype(None, None)

    assert not istype(42, str)
    assert not istype("lorem ipsum", int)
    assert not istype(None, int)


def test_user_defined_class():
    class DummyClass:
        ...

    obj = DummyClass()

    assert istype(obj, DummyClass)
    assert not istype(None, DummyClass)
