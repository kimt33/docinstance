"""Test docinstance.wrapper."""
import importlib
import os
import sys

from docinstance.content.description import DocDescription
from docinstance.content.section import DocSection
from docinstance.docstring import Docstring
from docinstance.wrapper import (
    docstring,
    docstring_current_module,
    docstring_recursive,
    kwarg_wrapper,
)
import pytest


def test_kwarg_wrapper():
    """Test docinstance.wrapper.kwarg_wrapper."""

    @kwarg_wrapper
    def test(func, x=1):
        """Test function."""
        func.x = x
        return func

    def f():  # pragma: no cover
        """Test function."""
        pass

    with pytest.raises(AttributeError):
        f.x
    g = test(f)
    assert g.x == 1
    g = test(f, x=2)
    assert g.x == 2

    @test
    def f():  # pragma: no cover
        """Test function."""
        pass

    assert f.x == 1

    @test(x=2)
    def f():  # pragma: no cover
        """Test function."""
        pass

    assert f.x == 2


def test_wrapper_docstring_on_func():
    """Test docinstance.wrapper.docstring on a function."""
    # no _docinstance
    @docstring
    def test():  # pragma: no cover
        """Test docstring.

        Parameters
        ----------
        x : int
            Something.

        """
        pass

    # NOTE: the indentation can be removed with inspect.cleandoc
    assert test.__doc__ == (
        "Test docstring.\n"
        "\n"
        "        Parameters\n"
        "        ----------\n"
        "        x : int\n"
        "            Something.\n\n"
        "        "
    )
    assert not hasattr(test, "_docinstance")

    # _docinstance
    docinstance = Docstring(
        [
            "Test docstring.",
            DocSection("parameters", DocDescription("x", types=int, descs="Something.")),
        ]
    )

    def test():  # pragma: no cover
        """Test function."""
        pass

    # FIXME: this is terrible because contents inside function is ignored when declaring a function
    # i.e. we cannot set the attribute of a function within a function definition. Docstrings are
    # special so they are not ignored. Using docstring that get parsed seems to be only option for
    # standalone functions
    test._docinstance = docinstance
    docstring(test)

    assert test.__doc__ == (
        "Test docstring.\n" "\n" "Parameters\n" "----------\n" "x : int\n" "    Something.\n\n"
    )
    assert test._docinstance == docinstance

    docstring(test, indent_level=2)
    assert test.__doc__ == (
        "Test docstring.\n"
        "\n"
        "        Parameters\n"
        "        ----------\n"
        "        x : int\n"
        "            Something.\n\n"
        "        "
    )
    assert test._docinstance == docinstance


def test_wrapper_docstring_on_class():
    """Test docinstance.wrapper.docstring on a class."""
    # no _docinstance
    @docstring
    class Test:  # pragma: no cover
        """Test docstring.

        Attributes
        ----------
        x : int
            Something.

        """

        def f(self):
            """Test function.

            Returns
            -------
            nothing

            """
            pass

    assert Test.__doc__ == (
        "Test docstring.\n\n"
        "        Attributes\n"
        "        ----------\n"
        "        x : int\n"
        "            Something.\n\n"
        "        "
    )
    assert not hasattr(Test, "_docinstance")

    # docinstance
    docinstance1 = Docstring(
        [
            "Test docstring.",
            DocSection("attributes", DocDescription("x", types=int, descs="Something.")),
        ]
    )
    docinstance2 = Docstring(["Test function.", DocSection("returns", "nothing")])

    # w/o indentation
    @docstring
    class Test:  # pragma: no cover
        """Test class."""

        _docinstance = docinstance1

        def f(self):
            """Do nothing."""
            pass

        f._docinstance = docinstance2

    assert Test.__doc__ == (
        "Test docstring.\n\n" "Attributes\n" "----------\n" "x : int\n" "    Something.\n\n"
    )
    assert Test._docinstance == docinstance1
    assert Test.f.__doc__ == "Do nothing."
    assert Test.f._docinstance == docinstance2

    # w/ indentation
    @docstring(indent_level=1)
    class Test:  # pragma: no cover
        """Test class."""

        _docinstance = docinstance1

        def f(self):
            """Test function."""
            pass

        f._docinstance = docinstance2

    assert Test.__doc__ == (
        "Test docstring.\n\n"
        "    Attributes\n"
        "    ----------\n"
        "    x : int\n"
        "        Something.\n\n"
        "    "
    )


def test_wrapper_docstring_recursive_on_class():
    """Test docinstance.wrapper.docstring_recursive on a class."""
    # no _docinstance
    @docstring_recursive
    class Test:  # pragma: no cover
        """Test docstring.

        Attributes
        ----------
        x : int
            Something.

        """

        def f(self):
            """Test function.

            Returns
            -------
            nothing

            """
            pass

    assert Test.__doc__ == (
        "Test docstring.\n\n"
        "        Attributes\n"
        "        ----------\n"
        "        x : int\n"
        "            Something.\n\n"
        "        "
    )
    assert not hasattr(Test, "_docinstance")
    assert Test.f.__doc__ == (
        "Test function.\n\n"
        "            Returns\n"
        "            -------\n"
        "            nothing\n\n"
        "            "
    )
    assert not hasattr(Test.f, "_docinstance")

    # docinstance
    docinstance1 = Docstring(
        [
            "Test docstring.",
            DocSection("attributes", DocDescription("x", types=int, descs="Something.")),
        ]
    )
    docinstance2 = Docstring(["Test function.", DocSection("returns", "nothing")])

    # w/o indentation
    @docstring_recursive
    class Test:  # pragma: no cover
        """Test class."""

        _docinstance = docinstance1

        def f(self):
            """Test function."""
            pass

        f._docinstance = docinstance2

    assert Test.__doc__ == (
        "Test docstring.\n\n" "Attributes\n" "----------\n" "x : int\n" "    Something.\n\n"
    )
    assert Test._docinstance == docinstance1
    assert Test.f.__doc__ == (
        "Test function.\n\n" "    Returns\n" "    -------\n" "    nothing\n\n" "    "
    )
    assert Test.f._docinstance == docinstance2

    # w indentation
    @docstring_recursive(indent_level=2)
    class Test:  # pragma: no cover
        """Test class."""

        _docinstance = docinstance1

        def f(self):
            """Test function."""
            pass

        f._docinstance = docinstance2

    assert Test.__doc__ == (
        "Test docstring.\n\n"
        "        Attributes\n"
        "        ----------\n"
        "        x : int\n"
        "            Something.\n\n"
        "        "
    )
    assert Test._docinstance == docinstance1
    assert Test.f.__doc__ == (
        "Test function.\n\n"
        "            Returns\n"
        "            -------\n"
        "            nothing\n\n"
        "            "
    )
    assert Test.f._docinstance == docinstance2


def test_docstring_current_module():
    """Test docinstance.wrapper.docstring_current_module on the current module."""
    global test_docstring_current_module
    test_docstring_current_module._docinstance = Docstring(
        ["Test docinstance.wrapper.docstring_current_module on the current module.", "Did it work?"]
    )

    def supplementary_docstring_current_module():
        """To be used to test docstring_current_module in test_docstring_current_module."""
        pass

    supplementary_docstring_current_module._docinstance = Docstring(
        [
            "Some docstring.",
            DocSection("parameters", DocDescription("x", types=int, descs="Example.")),
        ]
    )
    test_docstring_current_module.f = supplementary_docstring_current_module

    docstring_current_module()
    assert (
        test_docstring_current_module.__doc__
        == "Test docinstance.wrapper.docstring_current_module on the current module.\n\n"
        "    Did it work?\n\n"
        "    "
    )

    assert (
        test_docstring_current_module.f.__doc__ == "Some docstring.\n\n"
        "        Parameters\n"
        "        ----------\n"
        "        x : int\n"
        "            Example.\n\n"
        "        "
    )


def test_docstring_modify_import(tmp_path):
    """Test docinstance.wrapper.docstring_modify_import on module `dummy`."""
    assert not hasattr(importlib._bootstrap_external.SourceFileLoader.exec_module, "special_cases")
    # create temporary directory
    tmp_dir = tmp_path / "test"
    tmp_dir.mkdir()
    # create python file that calls docstring_modify_import
    path1 = tmp_dir / "dummy1.py"
    path1.write_text(
        "from docinstance.wrapper import docstring_modify_import\n" "docstring_modify_import()"
    )
    # create another python file with docstrings
    path2 = tmp_dir / "dummy2.py"
    path2.write_text(
        '''"""This will be replaced."""
from docinstance.docstring import Docstring
from docinstance.content.section import DocSection
from docinstance.content.description import DocDescription

_docinstance = Docstring([
    'Dummy module for testing docinstance.wrapper.docstring_modify_import.'
])


class DummyClass:
    """This too will be replaced."""

    _docinstance = Docstring([
        'Class for testing.',
        DocSection('attributes', DocDescription('x', types=str, descs='Example.'))
    ])
        '''
    )
    # create yet another python file with docstring_modify_import
    path3 = tmp_dir / "dummy3.py"
    path3.write_text(
        "from docinstance.wrapper import docstring_modify_import\n" "docstring_modify_import()"
    )

    # check that dummy2 is decorated
    sys.path.append(str(tmp_dir))
    import dummy1
    import dummy2 as test

    assert test.__doc__ == "Dummy module for testing docinstance.wrapper.docstring_modify_import."
    assert (
        test.DummyClass.__doc__ == "Class for testing.\n\n"
        "    Attributes\n"
        "    ----------\n"
        "    x : str\n"
        "        Example.\n\n"
        "    "
    )
    assert importlib._bootstrap_external.SourceFileLoader.exec_module.special_cases == set(
        [os.path.dirname(dummy1.__file__)]
    )

    # check that multiple function calls does not change anything
    import dummy3

    assert importlib._bootstrap_external.SourceFileLoader.exec_module.special_cases == set(
        [os.path.dirname(dummy3.__file__)]
    )

    # import package outside current directory
    import docinstance.utils

    # reload module because it has already been loaded via docinstance.wrapper
    importlib.reload(docinstance.utils)
    # check that the objects within docinstance.utils has not been touched by wrapper.
    with pytest.raises(AttributeError):
        docinstance.utils._docinstance
