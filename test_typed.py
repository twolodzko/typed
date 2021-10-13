import pytest

from typed import typed


def test_no_arguments():
    @typed
    def func():
        return None

    assert func() is None


def test_no_types():
    @typed
    def func(a, b, c):
        return a, b, c

    assert func(1, 2, 3) == (1, 2, 3)


def test_some_types():
    @typed
    def func(a, b: str, c: int):
        return a, b, c

    # valid types
    assert func(1, "2", 3) == (1, "2", 3)
    assert func("1", "2", 3) == ("1", "2", 3)

    # invalid types
    with pytest.raises(TypeError):
        func(1, 2, 3)

    with pytest.raises(TypeError):
        func(1, "2", "3")

    with pytest.raises(TypeError):
        func("1", 2, 3)

    with pytest.raises(TypeError):
        func("1", "2", "3")


def test_all_types():
    @typed
    def func(a: int, b: str, c: int):
        return a, b, c

    # valid types
    assert func(1, "2", 3) == (1, "2", 3)

    # invalid types
    with pytest.raises(TypeError):
        func("1", "2", 3)

    with pytest.raises(TypeError):
        func(1, 2, 3)


def test_named_argument():
    @typed
    def func(a: int, b: str, c: int):
        return a, b, c

    # valid types
    assert func(1, "2", c=3) == (1, "2", 3)

    # invalid types
    with pytest.raises(TypeError):
        func(1, "2", c="3")


def test_all_named_arguments():
    @typed
    def func(a: int, b: str, c: int):
        return a, b, c

    # valid types
    assert func(c=3, a=1, b="2") == (1, "2", 3)

    # invalid types
    with pytest.raises(TypeError):
        func(c=3, a=1, b=2)


def test_forced_named_arguments():
    @typed
    def func(*, a: int, b: str, c: int):
        return a, b, c

    # valid types
    assert func(c=3, a=1, b="2") == (1, "2", 3)

    # invalid types
    with pytest.raises(TypeError):
        func(c=3, a=1, b=2)


def test_defaults():
    @typed
    def func(a: int, b: str = "2", c: int = 3):
        return a, b, c

    # valid types
    assert func(1) == (1, "2", 3)

    # invalid types
    with pytest.raises(TypeError):
        func("1")


def test_class():
    class DummyClass:
        @typed
        def func(self, a, b: str):
            return a, b

    obj = DummyClass()

    # valid type
    assert obj.func(1, "2") == (1, "2")

    # invalid type
    with pytest.raises(TypeError):
        obj.func(1, 2)


def test_many_arguments():

    @typed
    def func(a, b, c: int, d: str, e: int = 5, f: str = "6", *, g: int = 7, h: str = "8"):
        return a, b, c, d, e, f, g, h

    # valid type
    assert func(1, "2", 3, "4") == (1, "2", 3, "4", 5, "6", 7, "8")

    # invalid type
    with pytest.raises(TypeError):
        func(1, "2", "3", "4")

    with pytest.raises(TypeError):
        func(1, "2", 3, 4)

    with pytest.raises(TypeError):
        func(1, "2", 3, "4", "5")

    with pytest.raises(TypeError):
        func(1, "2", 3, "4", e = "5")

    with pytest.raises(TypeError):
        func(1, "2", 3, "4", g = 7, e = 5, h = 8)
