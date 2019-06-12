"""Test docinstance.parser.napoleon."""
from docinstance.parser.numpy import parse_numpy as parse_ref_numpy
import pytest

pytest.importorskip("sphinxcontrib.napoleon")
from docinstance.parser.napoleon import parse_numpy


def test_parse_numpy():
    """Tests docinstance.numpy.parse_numpy."""
    # summary
    docstring = "summary"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
    docstring = "summary\n"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
    docstring = "\nsummary\n"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
    docstring = "\n\nsummary\n"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__

    # extended
    docstring = "summary\n\nblock1\n\nblock2"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
    docstring = "\nsummary\n\nblock1\n\nblock2"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
    docstring = "\nsummary\n\n\n\nblock2\n\n"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
    docstring = "\n\nsummary\n\nblock1\n\nblock2"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
    # extended + permitted headers
    docstring = "summary\n\nblock1\n\nblock2\n\nParameters\n----------\nstuff"
    assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__

    for header in ["parameters", "attributes", "other parameters", "returns", "yields"]:
        # name + multiple descriptions
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc\n    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        # NOTE: in the returns section, if only the name is given, napoleon treats it as a type.
        # However, DocDescription requires that the name be provided. So the type is stored as a
        # name instead to make it compatible with the existing writer.
        assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
        # name + types + multiple descriptions
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : str\n    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : {{str, int}}\n"
            "    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        # NOTE: multiple types are not separated and are treated in bulk in napoleon
        assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
            docstring
        ).make_docstring(style="numpy")
        # name + types
        docstring = "summary\n\n{0}\n{1}\nabc: str\ndef: int".format(
            header.title(), "-" * len(header)
        )
        assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__

    for header in ["methods", "raises"]:
        # name + multiple descriptions
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc\n    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
        # name + types + multiple descriptions
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : str\n    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
            docstring
        ).make_docstring(style="numpy")
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : {{str, int}}\n"
            "    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        # assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
        assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
            docstring
        ).make_docstring(style="numpy")
        # name + signature + multiple descriptions
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y)\n    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        # assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
        assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
            docstring
        ).make_docstring(style="numpy_signature")
        # name + types + signature + multiple descriptions
        docstring = (
            "summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y) : str\n    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        # assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
        assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
            docstring
        ).make_docstring(style="numpy_signature")
        # name + types + signature + multiple descriptions - extended summary
        docstring = (
            "summary\n\n{0}\n{1}\nabc(x, y) : str\n    description1.\n"
            "    description2.".format(header.title(), "-" * len(header))
        )
        # assert parse_numpy(docstring).__dict__ == parse_ref_numpy(docstring).__dict__
        assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
            docstring
        ).make_docstring(style="numpy_signature")
        # name + types
        docstring = "summary\n\n{0}\n{1}\nabc : str\ndef : int".format(
            header.title(), "-" * len(header)
        )
        assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
            docstring
        ).make_docstring(style="numpy_signature")

    # See also
    docstring = (
        "summary\n\nblock1\n\nblock2\n\nSee Also\n--------\nsome_place.\n" "some_other_place."
    )
    assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
        docstring
    ).make_docstring(style="numpy")
    # NOTE: napoleon cuts off the see also past the first word so the following docstring will have
    # entries "some" and "some" for napoleon.
    # docstring = (
    #     "summary\n\nblock1\n\nblock2\n\nSee Also\n--------\nsome place.\n"
    #     "some other place."
    # )

    # References
    docstring = "summary\n\nblock1\n\nblock2\nReferences\n----------\nsome ref.\n" "some other ref."
    assert parse_numpy(docstring).make_docstring(style="numpy") == parse_ref_numpy(
        docstring
    ).make_docstring(style="numpy")
    # NOTE: if references are separated by two newlines, then the docinstances' parser removes the
    # newline, where as napoleon's keeps it
    # docstring = (
    #     "summary\n\nblock1\n\nblock2\nReferences\n----------\nsome ref.\n\n"
    #     "some other ref."
    # )
