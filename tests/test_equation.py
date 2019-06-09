"""Test docinstance.content.equation."""
from docinstance.content.equation import DocEquation
import pytest


def test_init():
    """Test DocEquation.__init__."""
    with pytest.raises(TypeError):
        DocEquation(1)
    with pytest.raises(TypeError):
        DocEquation(["x + 1", "y + 2"])
    test = DocEquation("a + b = 2")
    assert test.equations == ["a + b = 2"]
    test = DocEquation("a + b &= 2\\\\\nc + d &= 3")
    assert test.equations == ["a + b &= 2\\\\", "c + d &= 3"]
    test = DocEquation("a + b &= 2\\\\\nc + d &= 3\\\\\n")
    assert test.equations == ["a + b &= 2\\\\", "c + d &= 3\\\\"]
    test = DocEquation("a + b &= 2\\\\\nc + d &= 3\\\\")
    assert test.equations == ["a + b &= 2\\\\", "c + d &= 3\\\\"]


def test_make_numpy_docstring():
    """Test DocEquation.make_numpy_docstring."""
    test = DocEquation("a + b = 2")
    assert test.make_numpy_docstring(19, 0, 4) == ".. math:: a + b = 2\n\n"
    assert test.make_numpy_docstring(18, 0, 4) == ".. math::\n\n    a + b = 2\n\n"
    with pytest.raises(ValueError):
        test.make_numpy_docstring(8, 0, 4)
    test = DocEquation("a + b &= 2\\\\\nc + d &= 3\\\\\n")
    assert (
        test.make_numpy_docstring(18, 0, 4) == ".. math::\n\n"
        "    a + b &= 2\\\\\n"
        "    c + d &= 3\\\\\n\n"
    )
    test = DocEquation("a + b &= 2\\\\\nc + d &= 3\n")
    assert (
        test.make_numpy_docstring(18, 0, 4) == ".. math::\n\n"
        "    a + b &= 2\\\\\n"
        "    c + d &= 3\n\n"
    )
    test = DocEquation("a + b &= 2\nc + d &= 3\n")
    assert (
        test.make_numpy_docstring(18, 0, 4) == ".. math::\n\n"
        "    a + b &= 2\n"
        "    c + d &= 3\n\n"
    )
