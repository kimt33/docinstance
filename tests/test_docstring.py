"""Test docinstance.docstring."""
from docinstance.content.description import DocDescription
from docinstance.content.section import DocSection
from docinstance.docstring import Docstring
import pytest


def test_init():
    """Test Docstring.__init__."""
    with pytest.raises(TypeError):
        Docstring(1)
    with pytest.raises(TypeError):
        Docstring({"1"})
    with pytest.raises(TypeError):
        Docstring([1])
    with pytest.raises(TypeError):
        Docstring(["1", 1])
    with pytest.raises(ValueError):
        Docstring([])
    with pytest.raises(ValueError):
        Docstring("1", "nothing")
    with pytest.raises(ValueError):
        Docstring("1", None)

    test = Docstring("some text")
    assert isinstance(test.sections, list)
    assert len(test.sections) == 1
    assert isinstance(test.sections[0], DocSection)
    assert test.sections[0].header == ""
    assert test.sections[0].contents == ["some text"]

    test = Docstring(DocSection("some header", "Hello World"))
    assert isinstance(test.sections, list)
    assert len(test.sections) == 1
    assert isinstance(test.sections[0], DocSection)
    assert test.sections[0].header == "some header"
    assert test.sections[0].contents == ["Hello World"]

    test = Docstring([DocSection("some header", "Hello World"), "some text"])
    assert isinstance(test.sections, list)
    assert len(test.sections) == 2
    assert isinstance(test.sections[0], DocSection)
    assert test.sections[0].header == "some header"
    assert test.sections[0].contents == ["Hello World"]
    assert isinstance(test.sections[1], DocSection)
    assert test.sections[1].header == ""
    assert test.sections[1].contents == ["some text"]

    test = Docstring("some text", "numpy")
    assert test.default_style == "numpy"
    test = Docstring("some text", "rst")
    assert test.default_style == "rst"


def test_make_docstring():
    """Test Docstring.make_docstring."""
    test = Docstring(["summary", "extended summary", DocSection("parameters", "")])
    # standard input check
    with pytest.raises(TypeError):
        test.make_docstring(width=100.0)
    with pytest.raises(ValueError):
        test.make_docstring(width=-2)
    with pytest.raises(ValueError):
        test.make_docstring(width=0)
    with pytest.raises(TypeError):
        test.make_docstring(indent_level=2.0)
    with pytest.raises(ValueError):
        test.make_docstring(indent_level=-1)
    with pytest.raises(TypeError):
        test.make_docstring(tabsize=2.0)
    with pytest.raises(ValueError):
        test.make_docstring(tabsize=-2)
    with pytest.raises(ValueError):
        test.make_docstring(tabsize=0)
    with pytest.raises(NotImplementedError):
        test.make_docstring(style="random style")
    # bad ordering
    test = Docstring(["summary", DocSection("parameters", ""), "extended summary"])
    with pytest.raises(ValueError):
        test.make_docstring(style="numpy")
    # check summary errors
    test = Docstring([DocSection("parameters", DocDescription("something"))])
    with pytest.raises(ValueError):
        test.make_docstring()
    # one line summary
    test = Docstring("very very long summary")
    assert test.make_docstring(width=25) == "very very long summary\n\n"
    assert test.make_docstring(width=24) == "\nvery very long summary\n\n"
    # multiple line summary
    test = Docstring(["very very long summary", "extended summary"])
    assert test.make_docstring(width=25) == "very very long summary\n\nextended summary\n\n"
    assert test.make_docstring(width=24) == "\nvery very long summary\n\nextended summary\n\n"
    test = Docstring(DocSection("", ["very very long summary", "extended summary"]))
    assert test.make_docstring(width=25) == "very very long summary\n\nextended summary\n\n"
    assert test.make_docstring(width=24) == "\nvery very long summary\n\nextended summary\n\n"
    # other sections
    test = Docstring(
        [
            DocSection("", ["very very long summary", "extended summary"]),
            DocSection("parameters", DocDescription("var1", types=str, descs="Example.")),
        ]
    )
    assert (
        test.make_docstring(width=25) == "very very long summary\n\nextended summary\n\n"
        "Parameters\n----------\nvar1 : str\n    Example.\n\n"
    )
    assert (
        test.make_docstring(width=24) == "\nvery very long summary\n\nextended summary\n\n"
        "Parameters\n----------\nvar1 : str\n    Example.\n\n"
    )
    # numpy with signature
    test = Docstring(
        [
            "summary",
            DocSection(
                "methods", DocDescription("func1", signature="(a, b)", types=str, descs="Example.")
            ),
        ]
    )
    assert (
        test.make_docstring(width=25, style="numpy_signature")
        == "summary\n\nMethods\n-------\nfunc1(a, b) : str\n    Example.\n\n"
    )
    # google
    assert test.make_docstring(width=25, style="google") == (
        "summary\n\n" "Methods:\n" "    func1 (:obj:`str`):\n" "        Example.\n\n"
    )
    # rst
    assert test.make_docstring(width=25, style="rst") == (
        "summary\n\n" ":Methods:\n\n" ":param func1: Example.\n" ":type func1: :obj:`str`\n\n"
    )


def test_check_section_order():
    """Test Docstring.check_section_order."""
    test = Docstring(["summary", "extended", DocSection("parameters", ""), DocSection("warns", "")])
    assert test.check_section_order("numpy") is True
    test = Docstring(["summary", DocSection("parameters", ""), "extended", DocSection("warns", "")])
    assert test.check_section_order("numpy") is False
    test = Docstring(["summary", "extended", DocSection("warns", ""), DocSection("parameters", "")])
    assert test.check_section_order("numpy") is False
    # note that the unidentified seections are not permitted for numpy style
    test = Docstring(
        [
            "summary",
            DocSection("asdfdsaf", ""),
            "extended",
            DocSection("warns", ""),
            DocSection("parameters", ""),
        ]
    )
    with pytest.raises(ValueError):
        test.check_section_order("numpy")
    test = Docstring(
        [
            "summary",
            "extended",
            DocSection("warns", ""),
            DocSection("parameters", ""),
            DocSection("asdfdsaf", ""),
        ]
    )
    with pytest.raises(ValueError):
        test.check_section_order("numpy")

    # other styles do not enforce such ordering
    test = Docstring(
        [
            "summary",
            DocSection("asdfdsaf", ""),
            "extended",
            DocSection("warns", ""),
            DocSection("parameters", ""),
        ]
    )
    assert test.check_section_order("rst") is True
    assert test.check_section_order("random") is True
    # note that the unidentified sections are permitted for other styles
    # NOTE: following does not actually check for the effect of adding unidentified section for non
    # numpy style because all sections are unidentified for non numpy styles
    test = Docstring(
        [
            "summary",
            "extended",
            DocSection("warns", ""),
            DocSection("parameters", ""),
            DocSection("asdfdsaf", ""),
        ]
    )
    assert test.check_section_order("random") is True
