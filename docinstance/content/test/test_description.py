"""Test docinstance.content.description."""
import pytest
from docinstance.content.description import DocDescription


def test_init():
    """Test DocDescription.__init__."""
    with pytest.raises(TypeError):
        DocDescription([])
    with pytest.raises(TypeError):
        DocDescription(2)
    with pytest.raises(TypeError):
        DocDescription('test', signature=1)
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types=1)
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types=[1])
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types={str})
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types=[str, 1])
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types=str, descs=1)
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types=str, descs=[1])
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types=str, descs={'1'})
    with pytest.raises(TypeError):
        DocDescription('test', signature='', types=str, descs=['1', 2])

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
    with pytest.raises(ValueError):
        test.make_numpy_docstring(13, 0, 4)
    with pytest.raises(ValueError):
        test.make_numpy_docstring(14, 1, 2)
    assert test.make_numpy_docstring(14, 0, 4) == 'var_name : str\n    hello\n'
    assert test.make_numpy_docstring(16, 1, 2) == '  var_name : str\n    hello\n'
    # multiple types
    test = DocDescription('var_name', types=[str, int, bool], descs=['hello'])
    with pytest.raises(ValueError):
        test.make_numpy_docstring(15, 0, 4)
    with pytest.raises(ValueError):
        test.make_numpy_docstring(16, 1, 2)
    # NOTE: following raises an error even though width is big enough for 'var_name : {str,' because
    # the `utils.wrap` complains
    with pytest.raises(ValueError):
        test.make_numpy_docstring(16, 0, 4)
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


def test_make_google_docstring():
    """Test DocDescription.make_google_docstring."""
    # no type, desc
    test = DocDescription('var_name', descs=['hello'])
    assert test.make_google_docstring(15, 0, 4) == 'var_name: hello\n'
    # no type, no descs
    test = DocDescription('var_name')
    assert test.make_google_docstring(9, 0, 4) == 'var_name:\n'
    with pytest.raises(ValueError):
        test.make_google_docstring(8, 0, 4)
    # one type, no descs
    test = DocDescription('var_name', types=str)
    assert test.make_google_docstring(22, 0, 4) == 'var_name (:obj:`str`):\n'
    with pytest.raises(ValueError):
        test.make_google_docstring(21, 0, 4)
    # one type, no descs
    test = DocDescription('var_name', types='str')
    assert test.make_google_docstring(15, 0, 4) == 'var_name (str):\n'
    with pytest.raises(ValueError):
        test.make_google_docstring(14, 0, 4)
    # many types, no descs
    test = DocDescription('var_name', types=['str', int])
    assert test.make_google_docstring(22, 0, 4) == ('var_name (str,\n'
                                                    '          :obj:`int`):\n')
    with pytest.raises(ValueError):
        test.make_google_docstring(21, 0, 4)
    assert test.make_google_docstring(23, 1, 1) == (' var_name (str,\n'
                                                    '           :obj:`int`):\n')
    # one type, desc
    test = DocDescription('var_name', types=str, descs=['hello'])
    assert test.make_google_docstring(22, 0, 4) == 'var_name (:obj:`str`):\n    hello\n'
    # FIXME
    assert test.make_google_docstring(24, 1, 2) == '  var_name (:obj:`str`):\n    hello\n'
    # multiple types
    test = DocDescription('var_name', types=[str, int, bool], descs=['hello'])
    with pytest.raises(ValueError):
        test.make_google_docstring(22, 0, 4)
    with pytest.raises(ValueError):
        test.make_google_docstring(24, 1, 2)
    assert test.make_google_docstring(23, 0, 4) == ('var_name (:obj:`str`,\n'
                                                    '          :obj:`int`,\n'
                                                    '          :obj:`bool`):\n'
                                                    '    hello\n')
    assert test.make_google_docstring(26, 1, 2) == ('  var_name (:obj:`str`,\n'
                                                    '            :obj:`int`,\n'
                                                    '            :obj:`bool`):\n'
                                                    '    hello\n')
    assert (test.make_google_docstring(35, 1, 2) ==
            ('  var_name (:obj:`str`, :obj:`int`,\n'
             '            :obj:`bool`): hello\n'))
    # signature does nothing
    test2 = DocDescription('var_name', signature='(a, b, c)', types=[str, int, bool],
                           descs=['hello'])
    assert test.make_google_docstring(23, 0, 4) == test2.make_google_docstring(23, 0, 4)
    # multiple paragraphs
    test = DocDescription('var_name', types=[str, int, bool],
                          descs=['description 1', 'description 2', 'description 3'])
    assert test.make_google_docstring(26, 0, 2) == ('var_name (:obj:`str`,\n'
                                                    '          :obj:`int`,\n'
                                                    '          :obj:`bool`):\n'
                                                    '  description 1\n'
                                                    '  description 2\n'
                                                    '  description 3\n')
