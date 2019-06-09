"""Test docinstance.content.base."""
from docinstance.content.base import DocContent
import pytest


class ModDocContent(DocContent):
    """DocContent where the init does not raise an error."""

    def __init__(self):
        """Initialize."""
        pass


def test_base_init():
    """Test DocContent.__init__."""
    with pytest.raises(NotImplementedError):
        DocContent()


def test_base_eq():
    """Test DocContent.__eq__."""
    test1 = ModDocContent()
    test1.x = 1
    test2 = ModDocContent()
    test2.x = 1
    assert test1 == test2
    test2.y = 2
    assert not test1 == test2

    class Empty:
        """Empty class."""

        pass

    test2 = Empty()
    test2.x = 1
    assert not test1 == test2
    test2 = {"x": 1}
    assert not test1 == test2


def test_base_ne():
    """Test DocContent.__ne__."""
    test1 = ModDocContent()
    test1.x = 1
    test2 = ModDocContent()
    test2.x = 1
    assert not test1 != test2
    test2.y = 2
    assert test1 != test2

    class Empty:
        """Empty class."""

        pass

    test2 = Empty()
    test2.x = 1
    assert test1 != test2
    test2 = {"x": 1}
    assert test1 != test2


def test_base_make_docstring():
    """Test DocContent.make_docstring."""
    test = ModDocContent()
    with pytest.raises(TypeError):
        test.make_docstring(100, 0, 4, "")
    with pytest.raises(TypeError):
        test.make_docstring(100, 0, 4, ["numpy"])

    test.make_docstring_test = lambda width, indent_level, tabsize: "answer"
    assert test.make_docstring(100, 0, 4, "test") == "answer"

    with pytest.raises(NotImplementedError):
        test.make_docstring(100, 0, 4, "numpy")
    with pytest.raises(NotImplementedError):
        test.make_docstring(100, 0, 4, "google")
    with pytest.raises(NotImplementedError):
        test.make_docstring(100, 0, 4, "rst")
