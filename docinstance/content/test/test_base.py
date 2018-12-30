"""Test docinstance.content.base."""
import pytest
from docinstance.content.base import DocContent


class ModDocContent(DocContent):
    """DocContent where the init does not raise an error."""
    def __init__(self):
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
        pass
    test2 = Empty()
    test2.x = 1
    assert not test1 == test2
    test2 = {'x': 1}
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
        pass
    test2 = Empty()
    test2.x = 1
    assert test1 != test2
    test2 = {'x': 1}
    assert test1 != test2


def test_base_make_numpy_docstring():
    """Test DocContent.make_numpy_docstring."""
    test = ModDocContent()
    with pytest.raises(NotImplementedError):
        test.make_numpy_docstring(100, 0, 4)


def test_base_make_google_docstring():
    """Test DocContent.make_google_docstring."""
    test = ModDocContent()
    with pytest.raises(NotImplementedError):
        test.make_google_docstring(100, 0, 4)


def test_base_make_rst_docstring():
    """Test DocContent.make_rst_docstring."""
    test = ModDocContent()
    with pytest.raises(NotImplementedError):
        test.make_rst_docstring(100, 0, 4)
