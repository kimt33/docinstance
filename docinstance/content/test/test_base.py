"""Test docinstance.content.base."""
import pytest
from docinstance.content.base import DocContent


class TestDocContent(DocContent):
    """DocContent where the init does not raise an error."""
    def __init__(self):
        pass


def test_base_init():
    """Test DocContent.__init__."""
    with pytest.raises(NotImplementedError):
        DocContent()


def test_base_make_numpy_docstring():
    """Test DocContent.make_numpy_docstring."""
    test = TestDocContent()
    with pytest.raises(NotImplementedError):
        test.make_numpy_docstring(100, 0, 4)


def test_base_make_google_docstring():
    """Test DocContent.make_google_docstring."""
    test = TestDocContent()
    with pytest.raises(NotImplementedError):
        test.make_google_docstring(100, 0, 4)


def test_base_make_rst_docstring():
    """Test DocContent.make_rst_docstring."""
    test = TestDocContent()
    with pytest.raises(NotImplementedError):
        test.make_rst_docstring(100, 0, 4)
