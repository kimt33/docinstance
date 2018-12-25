"""Test docinstance.section."""
from nose.tools import assert_raises
from docinstance.section import DocSection
from docinstance.description import DocDescription


def test_init():
    """Test DocSection.__init__."""
    assert_raises(TypeError, DocSection, 1, '')
    assert_raises(TypeError, DocSection, ['1'], '')
    assert_raises(TypeError, DocSection, '1', 1)
    assert_raises(TypeError, DocSection, '1', {'1'})
    assert_raises(TypeError, DocSection, '1', ['1', DocDescription('test')])
    assert_raises(TypeError, DocSection, '1', [DocDescription('test'), '1'])

    test = DocSection('header name', 'hello')
    assert test.header == 'header name'
    assert test.contents == ['hello']
    test = DocSection('header name', ['hello', 'i am'])
    assert test.header == 'header name'
    assert test.contents == ['hello', 'i am']
    doc1 = DocDescription('hello')
    doc2 = DocDescription('i am')
    test = DocSection('header name', doc1)
    assert test.header == 'header name'
    assert test.contents == [doc1]
    test = DocSection('header name', [doc1, doc2])
    assert test.header == 'header name'
    assert test.contents == [doc1, doc2]


def test_make_numpy_docstring():
    """Test DocSection.make_numpy_docstring."""
    # string content
    test = DocSection('header name', 'hello')
    assert test.make_numpy_docstring(11, 0, 4) == 'Header Name\n-----------\nhello\n\n'
    assert test.make_numpy_docstring(11, 0, 4) == 'Header Name\n-----------\nhello\n\n'
    # multiple string contents
    test = DocSection('header name', ['hello', 'i am'])
    assert test.make_numpy_docstring(11, 0, 4) == 'Header Name\n-----------\nhello\n\ni am\n\n'
    # doc description
    test = DocSection('header name', DocDescription('var_name', types=str, descs='Example.'))
    assert (test.make_numpy_docstring(20, 0, 4) ==
            'Header Name\n-----------\nvar_name : str\n    Example.\n\n')
    # multiple doc descriptions
    test = DocSection('header name', [DocDescription('var_name1', types=str, descs='Example 1.'),
                                      DocDescription('var_name2', types=int, descs='Example 2.')])
    assert (test.make_numpy_docstring(20, 0, 4) ==
            'Header Name\n-----------\nvar_name1 : str\n    Example 1.\nvar_name2 : int\n'
            '    Example 2.\n\n')
    # signature does nothing
    test = DocSection('header name',
                      DocDescription('var_name', signature='(a, b)', types=str, descs='Example.'))
    assert (test.make_numpy_docstring(20, 0, 4) ==
            'Header Name\n-----------\nvar_name : str\n    Example.\n\n')


def test_make_numpy_docstring_signature():
    """Test DocSection.make_numpy_docstring_signature."""
    test = DocSection('header name',
                      DocDescription('var_name', signature='(a, b)', types=str, descs='Example.'))
    assert (test.make_numpy_docstring_signature(20, 0, 4) ==
            'Header Name\n-----------\nvar_name(a, b) : str\n    Example.\n\n')


def test_make_google_docstring():
    """Test DocSection.make_google_docstring."""
    test = DocSection('header name',
                      DocDescription('var_name', signature='(a, b)', types=str, descs='Example.'))
    assert_raises(NotImplementedError, test.make_google_docstring, 20, 0, 4)


def test_make_rst_docstring():
    """Test DocSection.make_rst_docstring."""
    test = DocSection('header name',
                      DocDescription('var_name', signature='(a, b)', types=str, descs='Example.'))
    assert_raises(NotImplementedError, test.make_rst_docstring, 20, 0, 4)
