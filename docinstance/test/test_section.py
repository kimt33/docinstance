"""Test docinstance.section."""
from nose.tools import assert_raises
from docinstance.section import (DocSection, Summary, ExtendedSummary, Parameters, Attributes,
                                 Methods, Returns, Yields, OtherParameters, Raises, Warns, Warnings,
                                 SeeAlso, Notes, References, Examples)
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


def test_section_summary():
    """Test Summary.__init__."""
    test = Summary('This is a summary.')
    assert test.header == ''
    assert test.contents == ['This is a summary.']


def test_section_extended_summary():
    """Test ExtendedSummary.__init__."""
    test = ExtendedSummary('This is an extended summary.')
    assert test.header == ''
    assert test.contents == ['This is an extended summary.']


def test_section_parameters():
    """Test Parameters.__init__."""
    desc1 = DocDescription('a', types=str, descs='Example 1.')
    desc2 = DocDescription('b', types=int, descs='Example 2.')
    test = Parameters([desc1, desc2])
    assert test.header == 'parameters'
    assert test.contents == [desc1, desc2]


def test_section_attributes():
    """Test Attributes.__init__."""
    desc1 = DocDescription('a', types=str, descs='Example 1.')
    desc2 = DocDescription('b', types=int, descs='Example 2.')
    test = Attributes([desc1, desc2])
    assert test.header == 'attributes'
    assert test.contents == [desc1, desc2]


def test_section_methods():
    """Test Methods.__init__."""
    desc1 = DocDescription('f', signature='(x, y)', types=int, descs='Example 1.')
    desc2 = DocDescription('g', signature='(z=1)', types=int, descs='Example 2.')
    test = Methods([desc1, desc2])
    assert test.header == 'methods'
    assert test.contents == [desc1, desc2]


def test_section_returns():
    """Test Returns.__init__."""
    desc1 = DocDescription('a', types=int, descs='Example 1.')
    desc2 = DocDescription('b', types=str, descs='Example 2.')
    test = Returns([desc1, desc2])
    assert test.header == 'returns'
    assert test.contents == [desc1, desc2]


def test_section_yields():
    """Test Yields.__init__."""
    desc = DocDescription('a', types=int, descs='Example 1.')
    test = Yields(desc)
    assert test.header == 'yields'
    assert test.contents == [desc]


def test_section_otherparameters():
    """Test OtherParameters.__init__."""
    desc1 = DocDescription('a', types=int, descs='Example 1.')
    desc2 = DocDescription('b', types=str, descs='Example 2.')
    test = OtherParameters([desc1, desc2])
    assert test.header == 'other parameters'
    assert test.contents == [desc1, desc2]


def test_section_raises():
    """Test Raises.__init__."""
    desc = DocDescription('TypeError', descs='If something.')
    test = Raises(desc)
    assert test.header == 'raises'
    assert test.contents == [desc]


def test_section_warns():
    """Test Warns.__init__."""
    desc = DocDescription('Warning', descs='If something.')
    test = Warns(desc)
    assert test.header == 'warns'
    assert test.contents == [desc]


def test_section_warnings():
    """Test Warnings.__init__."""
    test = Warnings('Not to be used.')
    assert test.header == 'warnings'
    assert test.contents == ['Not to be used.']


def test_section_seealso():
    """Test SeeAlso.__init__."""
    test = SeeAlso('Some other code.')
    assert test.header == 'see also'
    assert test.contents == ['Some other code.']


def test_section_notes():
    """Test Notes.__init__."""
    test = Notes('Some comment.')
    assert test.header == 'notes'
    assert test.contents == ['Some comment.']


def test_section_references():
    """Test References.__init__."""
    test = References('Some reference.')
    assert test.header == 'references'
    assert test.contents == ['Some reference.']


def test_section_examples():
    """Test Examples.__init__."""
    test = Examples('Some example.')
    assert test.header == 'examples'
    assert test.contents == ['Some example.']
