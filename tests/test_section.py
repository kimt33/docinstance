"""Test docinstance.content.section."""
import pytest
from docinstance.content.section import (
    DocSection,
    Summary,
    ExtendedSummary,
    Parameters,
    Attributes,
    Methods,
    Returns,
    Yields,
    OtherParameters,
    Raises,
    Warns,
    Warnings,
    SeeAlso,
    Notes,
    References,
    Examples,
)
from docinstance.content.description import DocDescription


def test_init():
    """Test DocSection.__init__."""
    with pytest.raises(TypeError):
        DocSection(1, "")
    with pytest.raises(TypeError):
        DocSection(["1"], "")
    with pytest.raises(TypeError):
        DocSection("1", 1)
    with pytest.raises(TypeError):
        DocSection("1", {"1"})
    with pytest.raises(TypeError):
        DocSection("1", ["1", DocDescription("test")])
    with pytest.raises(TypeError):
        DocSection("1", [DocDescription("test"), "1"])

    test = DocSection("header name", "hello")
    assert test.header == "header name"
    assert test.contents == ["hello"]
    test = DocSection("header name", ["hello", "i am"])
    assert test.header == "header name"
    assert test.contents == ["hello", "i am"]
    doc1 = DocDescription("hello")
    doc2 = DocDescription("i am")
    test = DocSection("header name", doc1)
    assert test.header == "header name"
    assert test.contents == [doc1]
    test = DocSection("header name", [doc1, doc2])
    assert test.header == "header name"
    assert test.contents == [doc1, doc2]


def test_make_numpy_docstring():
    """Test DocSection.make_numpy_docstring."""
    # string content
    test = DocSection("header name", "hello")
    assert test.make_numpy_docstring(11, 0, 4) == "Header Name\n-----------\nhello\n\n"
    assert test.make_numpy_docstring(11, 0, 4) == "Header Name\n-----------\nhello\n\n"
    # multiple string contents
    test = DocSection("header name", ["hello", "i am"])
    assert test.make_numpy_docstring(11, 0, 4) == "Header Name\n-----------\nhello\n\ni am\n\n"
    # doc description
    test = DocSection("header name", DocDescription("var_name", types=str, descs="Example."))
    assert (
        test.make_numpy_docstring(20, 0, 4)
        == "Header Name\n-----------\nvar_name : str\n    Example.\n\n"
    )
    # multiple doc descriptions
    test = DocSection(
        "header name",
        [
            DocDescription("var_name1", types=str, descs="Example 1."),
            DocDescription("var_name2", types=int, descs="Example 2."),
        ],
    )
    assert (
        test.make_numpy_docstring(20, 0, 4)
        == "Header Name\n-----------\nvar_name1 : str\n    Example 1.\nvar_name2 : int\n"
        "    Example 2.\n\n"
    )
    # signature does nothing
    test = DocSection(
        "header name", DocDescription("var_name", signature="(a, b)", types=str, descs="Example.")
    )
    assert (
        test.make_numpy_docstring(20, 0, 4)
        == "Header Name\n-----------\nvar_name : str\n    Example.\n\n"
    )


def test_make_numpy_docstring_signature():
    """Test DocSection.make_numpy_docstring_signature."""
    test = DocSection(
        "header name", DocDescription("var_name", signature="(a, b)", types=str, descs="Example.")
    )
    assert (
        test.make_numpy_docstring_signature(20, 0, 4)
        == "Header Name\n-----------\nvar_name(a, b) : str\n    Example.\n\n"
    )


def test_make_google_docstring():
    """Test DocSection.make_google_docstring."""
    with pytest.raises(ValueError):
        test = DocSection("quite long header name", "")
        test.make_google_docstring(10, 0, 4)
    # no header
    test = DocSection("", "Some text.")
    assert test.make_google_docstring(10, 0, 4) == ("Some text.\n\n")
    # one docdescription
    test = DocSection(
        "header name", DocDescription("var_name", signature="(a, b)", types=str, descs="Example.")
    )
    assert test.make_google_docstring(35, 0, 4) == (
        "Header Name:\n" "    var_name (:obj:`str`): Example.\n\n"
    )
    # multiple docdescription
    test = DocSection(
        "header name",
        [
            DocDescription("var1", signature="(a, b)", types=str, descs="Example1."),
            DocDescription("var2", signature="(c)", types="int", descs="Example2."),
        ],
    )
    assert test.make_google_docstring(35, 0, 4) == (
        "Header Name:\n" "    var1 (:obj:`str`): Example1.\n" "    var2 (int): Example2.\n\n"
    )
    # one string
    test = DocSection("header name", "Some text.")
    assert test.make_google_docstring(14, 0, 4) == ("Header Name:\n" "    Some text.\n\n")
    assert test.make_google_docstring(13, 0, 4) == ("Header Name:\n" "    Some\n" "    text.\n\n")
    # multiple string
    test = DocSection("header name", ["Some text.", "Another text."])
    assert test.make_google_docstring(17, 0, 4) == (
        "Header Name:\n" "    Some text.\n\n" "    Another text.\n\n"
    )
    assert test.make_google_docstring(14, 0, 4) == (
        "Header Name:\n" "    Some text.\n\n" "    Another\n" "    text.\n\n"
    )
    assert test.make_google_docstring(13, 0, 4) == (
        "Header Name:\n" "    Some\n" "    text.\n\n" "    Another\n" "    text.\n\n"
    )


def test_make_rst_docstring():
    """Test DocSection.make_rst_docstring."""
    # no header
    test = DocSection("", "Some text.")
    assert test.make_rst_docstring(10, 0, 4) == ("Some text.\n\n")
    # normal header, one docdescription
    test = DocSection(
        "header name", DocDescription("var_name", signature="(a, b)", types=str, descs="Example.")
    )
    assert test.make_rst_docstring(35, 0, 4) == (
        ":Header Name:\n\n" ":param var_name: Example.\n" ":type var_name: :obj:`str`\n\n"
    )
    # normal header, multiple docdescription
    test = DocSection(
        "header name",
        [
            DocDescription("var1", signature="(a, b)", types=str, descs="Example1."),
            DocDescription("var2", signature="(c)", types="int", descs="Example2."),
        ],
    )
    assert test.make_rst_docstring(35, 0, 4) == (
        ":Header Name:\n\n"
        ":param var1: Example1.\n"
        ":type var1: :obj:`str`\n"
        ":param var2: Example2.\n"
        ":type var2: int\n\n"
    )
    # normal header, one string
    test = DocSection("header name", "Some text.")
    assert test.make_rst_docstring(13, 0, 4) == (":Header Name:\n\n" "Some text.\n\n")
    # normal header, multiple string
    test = DocSection("header name", ["Some text.", "Another text."])
    assert test.make_rst_docstring(13, 0, 4) == (
        ":Header Name:\n\n" "Some text.\n\n" "Another text.\n\n"
    )

    # special header, doc description
    test = DocSection(
        "see also",
        [
            DocDescription("var1", signature="(a, b)", types=str, descs="Example1."),
            DocDescription("var2", signature="(c)", types="int", descs="Example2."),
        ],
    )
    assert test.make_rst_docstring(35, 0, 4) == (
        ".. seealso::\n"
        "    :param var1: Example1.\n"
        "    :type var1: :obj:`str`\n"
        "    :param var2: Example2.\n"
        "    :type var2: int\n\n"
    )
    # special header, string
    test = DocSection("to do", ["Example 1, something.", "Example 2."])
    assert test.make_rst_docstring(20, 0, 4) == (
        ".. todo:: Example 1,\n" "    something.\n" "    Example 2.\n\n"
    )


def test_section_summary_init():
    """Test Summary.__init__."""
    with pytest.raises(TypeError):
        Summary(["summary"])
    with pytest.raises(TypeError):
        Summary(DocDescription("something"))
    test = Summary("very very long summary")
    assert test.header == ""
    assert test.contents == ["very very long summary"]


def test_section_summary_make_docstring():
    """Test Summary.make_docstring."""
    test = Summary("very very long summary")
    assert (
        test.make_docstring(25, 0, 4, summary_only=True, special=False)
        == "very very long summary\n\n"
    )
    assert (
        test.make_docstring(24, 0, 4, summary_only=True, special=False)
        == "\nvery very long summary\n\n"
    )
    assert (
        test.make_docstring(28, 0, 4, summary_only=True, special=False) == "very very long summary"
    )
    assert (
        test.make_docstring(25, 0, 4, summary_only=False, special=False)
        == "very very long summary\n\n"
    )
    assert (
        test.make_docstring(24, 0, 4, summary_only=False, special=False)
        == "\nvery very long summary\n\n"
    )
    assert (
        test.make_docstring(28, 0, 4, summary_only=False, special=False)
        == "very very long summary\n\n"
    )

    assert not (
        test.make_docstring(25, 0, 4, summary_only=True, special=True)
        == "very very long summary\n\n"
    )
    assert (
        test.make_docstring(26, 0, 4, summary_only=True, special=True)
        == "very very long summary\n\n"
    )
    assert not (
        test.make_docstring(28, 0, 4, summary_only=True, special=True) == "very very long summary"
    )
    assert (
        test.make_docstring(29, 0, 4, summary_only=True, special=True) == "very very long summary"
    )

    test = Summary("very very very very very very long summary")
    with pytest.raises(ValueError):
        test.make_docstring(30, 0, 4)


def test_section_extended_summary():
    """Test ExtendedSummary.__init__."""
    test = ExtendedSummary("This is an extended summary.")
    assert test.header == ""
    assert test.contents == ["This is an extended summary."]


def test_section_parameters():
    """Test Parameters.__init__."""
    desc1 = DocDescription("a", types=str, descs="Example 1.")
    desc2 = DocDescription("b", types=int, descs="Example 2.")
    test = Parameters([desc1, desc2])
    assert test.header == "parameters"
    assert test.contents == [desc1, desc2]


def test_section_attributes():
    """Test Attributes.__init__."""
    desc1 = DocDescription("a", types=str, descs="Example 1.")
    desc2 = DocDescription("b", types=int, descs="Example 2.")
    test = Attributes([desc1, desc2])
    assert test.header == "attributes"
    assert test.contents == [desc1, desc2]


def test_section_methods():
    """Test Methods.__init__."""
    desc1 = DocDescription("f", signature="(x, y)", types=int, descs="Example 1.")
    desc2 = DocDescription("g", signature="(z=1)", types=int, descs="Example 2.")
    test = Methods([desc1, desc2])
    assert test.header == "methods"
    assert test.contents == [desc1, desc2]


def test_section_returns():
    """Test Returns.__init__."""
    desc1 = DocDescription("a", types=int, descs="Example 1.")
    desc2 = DocDescription("b", types=str, descs="Example 2.")
    test = Returns([desc1, desc2])
    assert test.header == "returns"
    assert test.contents == [desc1, desc2]


def test_section_yields():
    """Test Yields.__init__."""
    desc = DocDescription("a", types=int, descs="Example 1.")
    test = Yields(desc)
    assert test.header == "yields"
    assert test.contents == [desc]


def test_section_otherparameters():
    """Test OtherParameters.__init__."""
    desc1 = DocDescription("a", types=int, descs="Example 1.")
    desc2 = DocDescription("b", types=str, descs="Example 2.")
    test = OtherParameters([desc1, desc2])
    assert test.header == "other parameters"
    assert test.contents == [desc1, desc2]


def test_section_raises():
    """Test Raises.__init__."""
    desc = DocDescription("TypeError", descs="If something.")
    test = Raises(desc)
    assert test.header == "raises"
    assert test.contents == [desc]


def test_section_warns():
    """Test Warns.__init__."""
    desc = DocDescription("Warning", descs="If something.")
    test = Warns(desc)
    assert test.header == "warns"
    assert test.contents == [desc]


def test_section_warnings():
    """Test Warnings.__init__."""
    test = Warnings("Not to be used.")
    assert test.header == "warnings"
    assert test.contents == ["Not to be used."]


def test_section_seealso():
    """Test SeeAlso.__init__."""
    test = SeeAlso("Some other code.")
    assert test.header == "see also"
    assert test.contents == ["Some other code."]


def test_section_notes():
    """Test Notes.__init__."""
    test = Notes("Some comment.")
    assert test.header == "notes"
    assert test.contents == ["Some comment."]


def test_section_references():
    """Test References.__init__."""
    test = References("Some reference.")
    assert test.header == "references"
    assert test.contents == ["Some reference."]


def test_section_examples():
    """Test Examples.__init__."""
    test = Examples("Some example.")
    assert test.header == "examples"
    assert test.contents == ["Some example."]
