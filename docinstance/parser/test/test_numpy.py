"""Tests for docinstance.parser.numpy."""
from nose.tools import assert_raises
from docinstance.docstring import Docstring
from docinstance.section import (DocSection, Summary, ExtendedSummary, Parameters)
from docinstance.description import DocDescription
from docinstance.parser.numpy import parse_numpy, is_math, extract_math


def test_is_math():
    """Test docinstance.parser.numpy.is_math."""
    assert is_math('.. math::\n\n    x&=2\\\\\n    &=3')
    assert is_math('.. math::\n\n    x&=2\\\\\n    &=3\n')
    assert is_math('\n.. math::\n\n    x&=2\\\\\n    &=3\n\n\n')
    assert not is_math('x\n.. math::\n\n    x&=2\\\\\n    &=3\n\n\n')
    assert is_math('.. math::\n\n    x=2')


def test_extract_math():
    """Test docinstance.parser.numpy.extract_math."""
    assert (extract_math('.. math::\n\n    x &= 2\\\\\n    &= 3\n') ==
            ['.. math::\n\n    x &= 2\\\\\n    &= 3'])
    assert (extract_math('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n') ==
            ['x', '.. math::\n\n    x &= 2\\\\\n    &= 3'])
    assert (extract_math('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n\n\n') ==
            ['x', '.. math::\n\n    x &= 2\\\\\n    &= 3'])
    assert (extract_math('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n\ny') ==
            ['x', '.. math::\n\n    x &= 2\\\\\n    &= 3', 'y'])


# TODO: move into __eq__ of appropriate classes?
def equal_docstrings(doc1, doc2):
    """Return True if doc1 and doc2 have the same content, otherwise False.

    Parameters
    ----------
    doc1 : Docstring
    doc2 : Docstring

    Returns
    -------
    bool

    """
    if not (isinstance(doc1, Docstring) and isinstance(doc2, Docstring)):
        return False
    elif len(doc1.sections) != len(doc2.sections):
        return False
    for section1, section2 in zip(doc1.sections, doc2.sections):
        # this part repeats
        if section1.header != section2.header:
            return False
        elif len(section1.contents) != len(section2.contents):
            return False
        for content1, content2 in zip(section1.contents, section2.contents):
            if isinstance(content1, str) and isinstance(content2, str):
                if content1 != content2:
                    return False
            # elif isinstance(content1, DocDescription) and isinstance(content2, DocDescription):
            elif (content1.name != content2.name or content1.signature != content2.signature or
                  content1.types != content2.types or content1.descs != content2.descs):
                return False
    return True


def test_compare_docinstances():
    """Test docinstance.parser.test.test_numpy."""
    doc1 = Docstring(['summary',
                      DocSection('section1', ['content1', 'content2']),
                      DocSection('section2', [DocDescription('name1', '(a, b)', str,
                                                             ['desc1', 'desc2']),
                                              DocDescription('name2', '(c, d)', int,
                                                             ['desc3', 'desc4'])])])
    doc2 = Docstring(['summary',
                      DocSection('section1', ['content1', 'content2']),
                      DocSection('section2', [DocDescription('name1', '(a, b)', str,
                                                             ['desc1', 'desc2']),
                                              DocDescription('name2', '(c, d)', int,
                                                             ['desc3', 'desc4'])])])
    assert not equal_docstrings(doc1, 1)
    assert not equal_docstrings(1, doc2)
    assert not equal_docstrings(Docstring(['a', 'b']),
                                Docstring(['a', 'b', 'c']))
    assert not equal_docstrings(Docstring(['a', 'b']),
                                Docstring(['a', DocSection('x', 'b')]))
    assert not equal_docstrings(Docstring(DocSection('a', 'b')),
                                Docstring(DocSection('a', ['b', 'c'])))
    assert not equal_docstrings(Docstring(DocSection('a', 'b')),
                                Docstring(DocSection('a', 'c')))
    assert not equal_docstrings(Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))),
                                Docstring(DocSection('a', DocDescription('1', 'y', 'z', 'k'))))
    assert not equal_docstrings(Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))),
                                Docstring(DocSection('a', DocDescription('x', '1', 'z', 'k'))))
    assert not equal_docstrings(Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))),
                                Docstring(DocSection('a', DocDescription('x', 'y', '1', 'k'))))
    assert not equal_docstrings(Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))),
                                Docstring(DocSection('a', DocDescription('x', 'y', 'z', '1'))))
    assert equal_docstrings(doc1, doc2)


def test_parse_numpy():
    """Tests docinstance.numpy.parse_numpy."""
    # summary
    docstring = 'summary'
    assert equal_docstrings(parse_numpy(docstring), Docstring(Summary('summary')))
    docstring = 'summary\n'
    assert equal_docstrings(parse_numpy(docstring), Docstring(Summary('summary')))
    docstring = '\nsummary\n'
    assert equal_docstrings(parse_numpy(docstring), Docstring(Summary('summary')))
    docstring = '    """summary\n    """'
    assert equal_docstrings(parse_numpy(docstring, contains_quotes=True),
                            Docstring(Summary('summary')))
    # FIXME: this should raise an error
    docstring = '\n\nsummary\n'
    assert equal_docstrings(parse_numpy(docstring), Docstring([Summary('summary')]))
    docstring = '"""\n\nsummary\n"""'
    assert_raises(ValueError, parse_numpy, docstring, contains_quotes=True)
    docstring = '    """\n\n    summary\n    """'
    assert_raises(ValueError, parse_numpy, docstring, contains_quotes=True)
    docstring = 'summary\na'
    assert_raises(ValueError, parse_numpy, docstring)

    # extended
    docstring = 'summary\n\nblock1\n\nblock2'
    assert equal_docstrings(parse_numpy(docstring),
                            Docstring([Summary('summary'), ExtendedSummary(['block1', 'block2'])]))
    docstring = '\nsummary\n\nblock1\n\nblock2'
    assert equal_docstrings(parse_numpy(docstring),
                            Docstring([Summary('summary'), ExtendedSummary(['block1', 'block2'])]))
    docstring = '\nsummary\n\n\n\nblock2\n\n'
    assert equal_docstrings(parse_numpy(docstring),
                            Docstring([Summary('summary'), ExtendedSummary(['block2'])]))
    # FIXME: is this a bug?
    docstring = '\n\nsummary\n\nblock1\n\nblock2'
    assert equal_docstrings(parse_numpy(docstring),
                            Docstring([Summary('summary'),
                                       ExtendedSummary(['block1', 'block2'])]))
    # extended + headers
    docstring = 'summary\n\nblock1\n\nblock2\n\nheader\n------\nstuff'
    assert equal_docstrings(parse_numpy(docstring),
                            Docstring([Summary('summary'), ExtendedSummary(['block1', 'block2']),
                                       DocSection('header', 'stuff')]))

    # header with bad divider (-----)
    docstring = 'summary\n\nblock1\n\nblock2\n\nheader1\n--\nstuff\n\n'
    assert_raises(ValueError, parse_numpy, docstring)

    for header in ['parameters', 'attributes', 'methods', 'returns', 'yields', 'raises',
                   'other parameters', 'see also']:
        # name + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert equal_docstrings(parse_numpy(docstring),
                                Docstring([Summary('summary'),
                                           ExtendedSummary(['block1', 'block2']),
                                           DocSection(header,
                                                      DocDescription('abc',
                                                                     descs=['description1.',
                                                                            'description2.']))]))
        # name + types + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert equal_docstrings(parse_numpy(docstring),
                                Docstring([Summary('summary'),
                                           ExtendedSummary(['block1', 'block2']),
                                           DocSection(header,
                                                      DocDescription('abc',
                                                                     types='str',
                                                                     descs=['description1.',
                                                                            'description2.']))]))
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : {{str, int}}\n'
                     '    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert equal_docstrings(parse_numpy(docstring),
                                Docstring([Summary('summary'),
                                           ExtendedSummary(['block1', 'block2']),
                                           DocSection(header,
                                                      DocDescription('abc',
                                                                     types=['str', 'int'],
                                                                     descs=['description1.',
                                                                            'description2.']))]))
        # name + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y)\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert equal_docstrings(parse_numpy(docstring),
                                Docstring([Summary('summary'),
                                           ExtendedSummary(['block1', 'block2']),
                                           DocSection(header,
                                                      DocDescription('abc',
                                                                     signature='(x, y)',
                                                                     descs=['description1.',
                                                                            'description2.']))]))
        # name + types + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert equal_docstrings(parse_numpy(docstring),
                                Docstring([Summary('summary'),
                                           ExtendedSummary(['block1', 'block2']),
                                           DocSection(header,
                                                      DocDescription('abc',
                                                                     types='str',
                                                                     signature='(x, y)',
                                                                     descs=['description1.',
                                                                            'description2.']))]))
        # name + types + signature + multiple descriptions - extended summary
        docstring = ('summary\n\n{0}\n{1}\nabc(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert equal_docstrings(parse_numpy(docstring),
                                Docstring([Summary('summary'),
                                           DocSection(header,
                                                      DocDescription('abc',
                                                                     types='str',
                                                                     signature='(x, y)',
                                                                     descs=['description1.',
                                                                            'description2.']))]))
        # name + types
        docstring = ('summary\n\n{0}\n{1}\nabc: str\ndef: int'.format(header.title(),
                                                                      '-'*len(header)))
        assert equal_docstrings(parse_numpy(docstring),
                                Docstring([Summary('summary'),
                                           DocSection(header,
                                                      [DocDescription('abc', types='str'),
                                                       DocDescription('def', types='int')])]))


def test_parse_numpy_raw():
    """Test pydocstring.numpy_docstring.parse_numpy with raw strings."""
    docstring = '"""summary\n\nextended"""'
    assert equal_docstrings(parse_numpy(docstring, contains_quotes=True),
                            Docstring([Summary('summary'),
                                       ExtendedSummary('extended')]))
    docstring = 'r"""summary\n\nextended"""'
    assert_raises(NotImplementedError, parse_numpy, docstring, contains_quotes=True)


def test_parse_numpy_self():
    """Test pydocstring.numpy_docstring.parse_numpy using itself as an example."""
    docstring = parse_numpy.__doc__
    # summary
    assert (parse_numpy(docstring, contains_quotes=False).sections[0].contents[0] ==
            'Parse a docstring in numpy format into a Docstring instance.')
    # extended
    assert (parse_numpy(docstring, contains_quotes=False).sections[1].contents ==
            ['Multiple descriptions of the indented information (e.g. parameters, '
             'attributes, methods, returns, yields, raises, see also) are '
             'distinguished from one another with a period. If the period is not '
             'present, then the description is assumed to be a multiline '
             'description.'])
    # parameters
    assert (parse_numpy(docstring, contains_quotes=False).sections[2].header ==
            'parameters')
    assert (parse_numpy(docstring, contains_quotes=False).sections[2].contents[0].name ==
            'docstring')
    assert (parse_numpy(docstring, contains_quotes=False).sections[2].contents[0].types ==
            ['str'])
    assert (parse_numpy(docstring, contains_quotes=False).sections[2].contents[0].descs ==
            ['Numpy docstring.'])
    assert (parse_numpy(docstring, contains_quotes=False).sections[2].contents[1].name ==
            'contains_quotes')
    assert (parse_numpy(docstring, contains_quotes=False).sections[2].contents[1].types ==
            ['bool'])
    assert (parse_numpy(docstring, contains_quotes=False).sections[2].contents[1].descs ==
            ['True if docstring contains """ or \'\'\'.'])
    # returns
    assert (parse_numpy(docstring, contains_quotes=False).sections[3].header ==
            'returns')
    assert (parse_numpy(docstring, contains_quotes=False).sections[3].contents[0].name ==
            'docstring')
    assert (parse_numpy(docstring, contains_quotes=False).sections[3].contents[0].types ==
            ['Docstring'])
    assert (parse_numpy(docstring, contains_quotes=False).sections[3].contents[0].descs ==
            ['Instance of Docstring that contains the necessary information.'])
    # raises
    assert (parse_numpy(docstring, contains_quotes=False).sections[4].header ==
            'raises')
    assert (parse_numpy(docstring, contains_quotes=False).sections[4].contents[0].name ==
            'ValueError')
    assert (parse_numpy(docstring, contains_quotes=False).sections[4].contents[0].descs ==
            ['If summary is not in the first or second line.',
             'If summary is now followed with a blank line.',
             'If number of \'-\' does not match the number of characters in the header.',
             'If given entry of the tabbed information (parameters, attributes, methods, returns, '
             'yields, raises, see also) had an unexpected pattern.'])
    assert (parse_numpy(docstring, contains_quotes=False).sections[4].contents[1].name ==
            'NotImplementedError')
    assert (parse_numpy(docstring, contains_quotes=False).sections[4].contents[1].descs ==
            ['If quotes corresponds to a raw string, i.e. r""".'])


def test_parse_numpy_equations():
    """Test pydocstring.numpy_docstring.parse_numpy with equations."""
    # equation in extended
    docstring = ('summary\n\n.. math::\n\n    \\frac{1}{2}')
    assert equal_docstrings(parse_numpy(docstring),
                            Docstring([Summary('summary'),
                                       ExtendedSummary('.. math::\n\n    \\frac{1}{2}')]))
    docstring = ('summary\n\n'
                 '.. math::\n\n'
                 '    x &= 2\\\\\n'
                 '    &= y\\\\\n')
    assert equal_docstrings(
        parse_numpy(docstring),
        Docstring([Summary('summary'),
                   ExtendedSummary('.. math::\n\n    x &= 2\\\\\n    &= y\\\\')])
    )
    docstring = ('summary\n\n'
                 '.. math::\n\n'
                 '    x &= 2\\\\\n'
                 '    &= y\\\\\n'
                 'Parameters\n'
                 '----------\n'
                 'a')
    assert equal_docstrings(
        parse_numpy(docstring),
        Docstring([Summary('summary'),
                   ExtendedSummary('.. math::\n\n    x &= 2\\\\\n    &= y\\\\'),
                   Parameters(DocDescription('a'))]))

    # equation in parameter
    # single line equation
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n    '
                 '    \\frac{1}{2}')
    assert equal_docstrings(
        parse_numpy(docstring),
        Docstring([Summary('summary'),
                   Parameters(DocDescription('a', types='float',
                                             descs='.. math::\n\n    \\frac{1}{2}\n'))])
    )
    # multi line equation
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n'
                 '        \\frac{1}{2}\\\\\n        \\frac{1}{3}')
    assert equal_docstrings(
        parse_numpy(docstring),
        Docstring([Summary('summary'),
                   Parameters(DocDescription('a', types='float',
                                             descs=['.. math::\n\n    \\frac{1}{2}\\\\\n'
                                                    '    \\frac{1}{3}\n']))])
    )
    # multiple equations
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n'
                 '        \\frac{1}{2}\n    ..math::\n        \\frac{1}{3}')
    assert equal_docstrings(
        parse_numpy(docstring),
        Docstring([Summary('summary'),
                   Parameters(DocDescription('a', types='float',
                                             descs=['.. math::\n\n    \\frac{1}{2}\n',
                                                    '..math::\n    \\frac{1}{3}\n']))])
    )
    # multiple equations and other descriptions
    docstring = ('summary\n\nParameters\n----------\na : float\n    Some float.\n    .. math::\n\n'
                 '        \\frac{1}{2}\n\n    Yes.\n    ..math::\n        \\frac{1}{3}\n'
                 '    This is the float.')
    assert equal_docstrings(
        parse_numpy(docstring),
        Docstring([Summary('summary'),
                   Parameters(DocDescription('a', types='float',
                                             descs=['Some float.',
                                                    '.. math::\n\n    \\frac{1}{2}\n',
                                                    'Yes.',
                                                    '..math::\n    \\frac{1}{3}\n',
                                                    'This is the float.']))])
    )
