"""Test docinstance.content.description."""
from nose.tools import assert_raises
from docinstance.content.description import DocDescription


def test_init():
    """Test DocDescription.__init__."""
    assert_raises(TypeError, DocDescription, [])
    assert_raises(TypeError, DocDescription, 2)
    assert_raises(TypeError, DocDescription, 'test', signature=1)
    assert_raises(TypeError, DocDescription, 'test', signature='', types=1)
    assert_raises(TypeError, DocDescription, 'test', signature='', types=[1])
    assert_raises(TypeError, DocDescription, 'test', signature='', types={str})
    assert_raises(TypeError, DocDescription, 'test', signature='', types=[str, 1])
    assert_raises(TypeError, DocDescription, 'test', signature='', types=str, descs=1)
    assert_raises(TypeError, DocDescription, 'test', signature='', types=str, descs=[1])
    assert_raises(TypeError, DocDescription, 'test', signature='', types=str, descs={'1'})
    assert_raises(TypeError, DocDescription, 'test', signature='', types=str, descs=['1', 2])

    test = DocDescription('test')
    assert test.name == 'test'
    assert test.signature == ''
    assert test.types == []
    assert test.descs == []
    test = DocDescription('test', signature='1')
    assert test.signature == '1'
    test = DocDescription('test', types=str)
    assert test.types == [str]
    test = DocDescription('test', types=(str,))
    assert test.types == [str]
    test = DocDescription('test', descs='2')
    assert test.descs == ['2']
    test = DocDescription('test', descs=('2',))
    assert test.descs == ['2']


def test_types_str():
    """Test DocDescription.types_str."""
    test = DocDescription('test', types=[str, int, 'list of str'])
    assert test.types_str == ['str', 'int', 'list of str']


def test_make_numpy_docstring():
    """Test DocDescription.make_numpy_docstring."""
    # no type
    test = DocDescription('var_name', descs=['hello'])
    assert test.make_numpy_docstring(9, 0, 4) == 'var_name\n    hello\n'
    # one type
    test = DocDescription('var_name', types=str, descs=['hello'])
    assert_raises(ValueError, test.make_numpy_docstring, 13, 0, 4)
    assert_raises(ValueError, test.make_numpy_docstring, 14, 1, 2)
    assert test.make_numpy_docstring(14, 0, 4) == 'var_name : str\n    hello\n'
    assert test.make_numpy_docstring(16, 1, 2) == '  var_name : str\n    hello\n'
    # multiple types
    test = DocDescription('var_name', types=[str, int, bool], descs=['hello'])
    assert_raises(ValueError, test.make_numpy_docstring, 15, 0, 4)
    assert_raises(ValueError, test.make_numpy_docstring, 16, 1, 2)
    # NOTE: following raises an error even though width is big enough for 'var_name : {str,' because
    # the `utils.wrap` complains
    assert_raises(ValueError, test.make_numpy_docstring, 16, 0, 4)
    assert test.make_numpy_docstring(27, 0, 4) == 'var_name : {str, int, bool}\n    hello\n'
    assert (test.make_numpy_docstring(26, 0, 4) ==
            'var_name : {str, int,\n            bool}\n    hello\n')
    assert (test.make_numpy_docstring(27, 1, 2) ==
            '  var_name : {str, int,\n              bool}\n    hello\n')
    assert (test.make_numpy_docstring(17, 0, 4) ==
            'var_name : {str,\n            int,\n            bool}\n    hello\n')
    # signature does nothing
    test2 = DocDescription('var_name', signature='(a, b, c)', types=[str, int, bool],
                           descs=['hello'])
    assert test.make_numpy_docstring(17, 0, 4) == test2.make_numpy_docstring(17, 0, 4)
    # multiple paragraphs
    test = DocDescription('var_name', types=[str, int, bool],
                          descs=['description 1', 'description 2', 'description 3'])
    assert (test.make_numpy_docstring(27, 0, 4) ==
            'var_name : {str, int, bool}\n    description 1\n    description 2\n'
            '    description 3\n')


def test_make_numpy_docstring_signature():
    """Test DocDescription.make_numpy_docstring_signature."""
    test = DocDescription('var_name', signature='(a, b, c)', types=[str, int, bool],
                          descs=['hello'])
    assert (test.make_numpy_docstring_signature(36, 0, 4) ==
            'var_name(a, b, c) : {str, int, bool}\n    hello\n')
    assert (test.make_numpy_docstring_signature(26, 0, 4) ==
            'var_name(a, b, c) : {str,\n                     int,\n                     bool}\n'
            '    hello\n')
