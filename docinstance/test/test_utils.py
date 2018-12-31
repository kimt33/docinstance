import pytest
import docinstance.utils


def test_wrap():
    """Test docinstance.utils.wrap."""
    # normal usage
    assert (docinstance.utils.wrap('hello my name is', width=5, indent_level=0, tabsize=4)
            == ['hello', 'my', 'name', 'is'])
    assert (docinstance.utils.wrap('hello my name is', width=6, indent_level=1, tabsize=1)
            == [' hello', ' my', ' name', ' is'])
    assert (docinstance.utils.wrap('hello my name is', width=10, indent_level=2, tabsize=2)
            == ['    hello', '    my', '    name', '    is'])
    assert (docinstance.utils.wrap('hello\n    my', width=20, indent_level=0, tabsize=4)
            == ['hello', '    my'])
    assert (docinstance.utils.wrap('hello\n    my', width=20, indent_level=1, tabsize=4)
            == ['    hello', '        my'])
    assert (docinstance.utils.wrap('.. math:\n\n    1 + 2\n', width=20, indent_level=0, tabsize=4)
            == ['.. math:', '', '    1 + 2', ''])
    # white spaces
    assert (docinstance.utils.wrap('    hello', width=9, indent_level=0, tabsize=4)
            == ['    hello'])
    assert (docinstance.utils.wrap('    hello', width=8, indent_level=0, tabsize=4) == ['hello'])
    assert (docinstance.utils.wrap('hello ', width=8, indent_level=0, tabsize=4) == ['hello'])
    assert (docinstance.utils.wrap('    hello my   ', width=9, indent_level=0, tabsize=4)
            == ['    hello', 'my'])
    assert (docinstance.utils.wrap('    hello   my   name   is    ', width=8, indent_level=0,
                                   tabsize=4) == ['hello', 'my', 'name', 'is'])
    assert (docinstance.utils.wrap('\n\n    hello   my   name   is\n\n', width=5, indent_level=0,
                                   tabsize=4) == ['', '', 'hello', 'my', 'name', 'is', '', ''])
    assert (docinstance.utils.wrap('\n\n    hello\n   my   name   is\n\n', width=5, indent_level=0,
                                   tabsize=4) == ['', '', 'hello', '   my', 'name', 'is', '', ''])
    # example
    assert (docinstance.utils.wrap('  Text that will be wrapped into different lines such that each'
                                   ' line is indented and is less than the given length.', width=30)

            == ['  Text that will be wrapped',
                'into different lines such that',
                'each line is indented and is',
                'less than the given length.'])

    # too much indentation
    with pytest.raises(ValueError):
        docinstance.utils.wrap('hello my name is', width=5, indent_level=3, tabsize=4)
    # long words
    with pytest.raises(ValueError):
        docinstance.utils.wrap('hello my name is', width=1, indent_level=0, tabsize=1)
    with pytest.raises(ValueError):
        docinstance.utils.wrap('hello my name is', width=5, indent_level=1, tabsize=1)
    # subsequent indent
    assert (docinstance.utils.wrap('a b c d e', width=4, indent_level=0, tabsize=4,
                                   subsequent_indent='xxx') ==
            ['a b', 'xxxc', 'xxxd', 'xxxe'])
    assert (docinstance.utils.wrap('a b c d e', width=4, indent_level=1, tabsize=1,
                                   subsequent_indent='xx') ==
            [' a b', ' xxc', ' xxd', ' xxe'])
    with pytest.raises(ValueError):
        docinstance.utils.wrap('a b c d e', width=4, indent_level=0, tabsize=4,
                               subsequent_indent='xxxx')


def test_wrap_indent_subsequent():
    """Test docinstance.utils.wrap_indent_subsequent."""
    assert (docinstance.utils.wrap_indent_subsequent('a b c d e', width=4, indent_level=1,
                                                     tabsize=3) ==
            ['a b', '   c', '   d', '   e'])
    with pytest.raises(ValueError):
        docinstance.utils.wrap_indent_subsequent('a b c d e', width=4, indent_level=1, tabsize=4)


def test_extract_members():
    """Test docinstance.utils.extract_members."""
    class Test:  # pragma: no cover
        @property
        def f(self):
            return 1

        def g(self):
            return 2

        h = pytest

    assert docinstance.utils.extract_members(Test) == {'f': Test.f, 'g': Test.g}
