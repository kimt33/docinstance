from nose.tools import assert_raises
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
    # white spaces are removed
    assert (docinstance.utils.wrap('\n\n    hello   my   name   is\n\n', width=5, indent_level=0,
                                   tabsize=4) == ['hello', 'my', 'name', 'is'])
    # too much indentation
    assert_raises(ValueError,
                  docinstance.utils.wrap, 'hello my name is', width=5, indent_level=3, tabsize=4)
    # long words
    assert_raises(ValueError,
                  docinstance.utils.wrap, 'hello my name is', width=1, indent_level=0, tabsize=1)
    assert_raises(ValueError,
                  docinstance.utils.wrap, 'hello my name is', width=5, indent_level=1, tabsize=1)


def test_extract_members():
    """Test docinstance.utils.extract_members."""
    class Test:
        @property
        def f(self):
            return 1

        def g(self):
            return 2

        h = assert_raises

    assert docinstance.utils.extract_members(Test) == {'f': Test.f, 'g': Test.g}
