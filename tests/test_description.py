"""Test docinstance.content.description."""
from docinstance.content.description import DocDescription
import pytest


def test_init():
    """Test DocDescription.__init__."""
    with pytest.raises(TypeError):
        DocDescription([])
    with pytest.raises(TypeError):
        DocDescription(2)
    with pytest.raises(TypeError):
        DocDescription("test", signature=1)
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types=1)
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types=[1])
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types={str})
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types=[str, 1])
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types=str, descs=1)
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types=str, descs=[1])
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types=str, descs={"1"})
    with pytest.raises(TypeError):
        DocDescription("test", signature="", types=str, descs=["1", 2])

    test = DocDescription("test")
    assert test.name == "test"
    assert test.signature == ""
    assert test.types == []
    assert test.descs == []
    test = DocDescription("test", signature="1")
    assert test.signature == "1"
    test = DocDescription("test", types=str)
    assert test.types == [str]
    test = DocDescription("test", types=(str,))
    assert test.types == [str]
    test = DocDescription("test", descs="2")
    assert test.descs == ["2"]
    test = DocDescription("test", descs=("2",))
    assert test.descs == ["2"]


def test_types_str():
    """Test DocDescription.types_str."""
    test = DocDescription("test", types=[str, int, "list of str"])
    assert test.types_str == ["str", "int", "list of str"]


def test_make_docstring_numpy():
    """Test DocDescription.make_docstring_numpy."""
    # no type
    test = DocDescription("var_name", descs=["hello"])
    assert test.make_docstring_numpy(9, 0, 4) == "var_name\n    hello\n"
    # one type
    test = DocDescription("var_name", types=str, descs=["hello"])
    with pytest.raises(ValueError):
        test.make_docstring_numpy(13, 0, 4)
    with pytest.raises(ValueError):
        test.make_docstring_numpy(14, 1, 2)
    assert test.make_docstring_numpy(14, 0, 4) == "var_name : str\n    hello\n"
    assert test.make_docstring_numpy(16, 1, 2) == "  var_name : str\n    hello\n"
    # multiple types
    test = DocDescription("var_name", types=[str, int, bool], descs=["hello"])
    with pytest.raises(ValueError):
        test.make_docstring_numpy(15, 0, 4)
    with pytest.raises(ValueError):
        test.make_docstring_numpy(16, 1, 2)
    # NOTE: following raises an error even though width is big enough for 'var_name : {str,' because
    # the `utils.wrap` complains
    with pytest.raises(ValueError):
        test.make_docstring_numpy(16, 0, 4)
    assert test.make_docstring_numpy(27, 0, 4) == "var_name : {str, int, bool}\n    hello\n"
    assert (
        test.make_docstring_numpy(26, 0, 4)
        == "var_name : {str, int,\n            bool}\n    hello\n"
    )
    assert (
        test.make_docstring_numpy(27, 1, 2)
        == "  var_name : {str, int,\n              bool}\n    hello\n"
    )
    assert (
        test.make_docstring_numpy(17, 0, 4)
        == "var_name : {str,\n            int,\n            bool}\n    hello\n"
    )
    # signature does nothing
    test2 = DocDescription(
        "var_name", signature="(a, b, c)", types=[str, int, bool], descs=["hello"]
    )
    assert test.make_docstring_numpy(17, 0, 4) == test2.make_docstring_numpy(17, 0, 4)
    # multiple paragraphs
    test = DocDescription(
        "var_name",
        types=[str, int, bool],
        descs=["description 1", "description 2", "description 3"],
    )
    assert (
        test.make_docstring_numpy(27, 0, 4)
        == "var_name : {str, int, bool}\n    description 1\n    description 2\n"
        "    description 3\n"
    )


def test_make_docstring_numpy_signature():
    """Test DocDescription.make_docstring_numpy_signature."""
    test = DocDescription(
        "var_name", signature="(a, b, c)", types=[str, int, bool], descs=["hello"]
    )
    assert (
        test.make_docstring_numpy_signature(36, 0, 4)
        == "var_name(a, b, c) : {str, int, bool}\n    hello\n"
    )
    assert (
        test.make_docstring_numpy_signature(26, 0, 4)
        == "var_name(a, b, c) : {str,\n                     int,\n                     bool}\n"
        "    hello\n"
    )


def test_make_docstring_google():
    """Test DocDescription.make_docstring_google."""
    # no type, desc
    test = DocDescription("var_name", descs=["hello"])
    assert test.make_docstring_google(15, 0, 4) == "var_name: hello\n"
    # no type, no descs
    test = DocDescription("var_name")
    assert test.make_docstring_google(9, 0, 4) == "var_name:\n"
    with pytest.raises(ValueError):
        test.make_docstring_google(8, 0, 4)
    # one type, no descs
    test = DocDescription("var_name", types=str)
    assert test.make_docstring_google(22, 0, 4) == "var_name (:obj:`str`):\n"
    with pytest.raises(ValueError):
        test.make_docstring_google(21, 0, 4)
    # one type, no descs
    test = DocDescription("var_name", types="str")
    assert test.make_docstring_google(15, 0, 4) == "var_name (str):\n"
    with pytest.raises(ValueError):
        test.make_docstring_google(14, 0, 4)
    # many types, no descs
    test = DocDescription("var_name", types=["str", int])
    assert test.make_docstring_google(22, 0, 4) == ("var_name (str,\n" "          :obj:`int`):\n")
    with pytest.raises(ValueError):
        test.make_docstring_google(21, 0, 4)
    assert test.make_docstring_google(23, 1, 1) == (" var_name (str,\n" "           :obj:`int`):\n")
    # one type, desc
    test = DocDescription("var_name", types=str, descs=["hello"])
    assert test.make_docstring_google(22, 0, 4) == "var_name (:obj:`str`):\n    hello\n"
    # FIXME
    assert test.make_docstring_google(24, 1, 2) == "  var_name (:obj:`str`):\n    hello\n"
    # multiple types
    test = DocDescription("var_name", types=[str, int, bool], descs=["hello"])
    with pytest.raises(ValueError):
        test.make_docstring_google(22, 0, 4)
    with pytest.raises(ValueError):
        test.make_docstring_google(24, 1, 2)
    assert test.make_docstring_google(23, 0, 4) == (
        "var_name (:obj:`str`,\n"
        "          :obj:`int`,\n"
        "          :obj:`bool`):\n"
        "    hello\n"
    )
    assert test.make_docstring_google(26, 1, 2) == (
        "  var_name (:obj:`str`,\n"
        "            :obj:`int`,\n"
        "            :obj:`bool`):\n"
        "    hello\n"
    )
    assert test.make_docstring_google(35, 1, 2) == (
        "  var_name (:obj:`str`, :obj:`int`,\n" "            :obj:`bool`): hello\n"
    )
    # signature does nothing
    test2 = DocDescription(
        "var_name", signature="(a, b, c)", types=[str, int, bool], descs=["hello"]
    )
    assert test.make_docstring_google(23, 0, 4) == test2.make_docstring_google(23, 0, 4)
    # multiple paragraphs
    test = DocDescription(
        "var_name",
        types=[str, int, bool],
        descs=["description 1", "description 2", "description 3"],
    )
    assert test.make_docstring_google(26, 0, 2) == (
        "var_name (:obj:`str`,\n"
        "          :obj:`int`,\n"
        "          :obj:`bool`):\n"
        "  description 1\n"
        "  description 2\n"
        "  description 3\n"
    )


def test_make_docstring_rst():
    """Test DocDescription.make_docstring_rst."""
    # only name
    test = DocDescription("var_name")
    assert test.make_docstring_rst(16, 0, 1) == ":param var_name:\n"
    assert test.make_docstring_rst(17, 1, 1) == " :param var_name:\n"
    with pytest.raises(ValueError):
        test.make_docstring_rst(15, 0, 4)
    # name + desc
    test = DocDescription("var_name", descs="hello")
    assert test.make_docstring_rst(22, 0, 1) == ":param var_name: hello\n"
    assert test.make_docstring_rst(21, 0, 1) == (":param var_name:\n" " hello\n")
    assert test.make_docstring_rst(21, 0, 4) == (":param var_name:\n" "    hello\n")
    test = DocDescription("var_name", descs=["hello my name is", "Example 2."])
    assert test.make_docstring_rst(25, 0, 4) == (
        ":param var_name: hello my\n" "    name is\n" "    Example 2.\n"
    )
    # name + type
    test = DocDescription("var_name", types=["str", int])
    assert test.make_docstring_rst(20, 0, 2) == (
        ":param var_name:\n" ":type var_name: str,\n" "  :obj:`int`\n"
    )
    # name + desc + type
    test = DocDescription("var_name", types=["str", int], descs=["Example 1.", "Example 2."])
    assert test.make_docstring_rst(27, 0, 4) == (
        ":param var_name: Example 1.\n"
        "    Example 2.\n"
        ":type var_name: str,\n"
        "    :obj:`int`\n"
    )
