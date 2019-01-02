"""Tests for docinstance.parser.numpy."""
import pytest
from docinstance.docstring import Docstring
from docinstance.content.section import (DocSection, Summary, ExtendedSummary, Parameters)
from docinstance.content.description import DocDescription
from docinstance.content.equation import DocEquation
from docinstance.parser.numpy import parse_numpy


def test_compare_docinstances():
    """Test docinstance.parser.test.test_numpy."""
    doc1 = Docstring(['summary',
                      DocSection('section1', ['content1', 'content2']),
                      DocSection('section2', [DocDescription('name1', '(a, b)', str,
                                                             ['desc1', 'desc2']),
                                              DocDescription('name2', '(c, d)', int,
                                                             ['desc3', DocEquation('desc4')])])])
    doc2 = Docstring(['summary',
                      DocSection('section1', ['content1', 'content2']),
                      DocSection('section2', [DocDescription('name1', '(a, b)', str,
                                                             ['desc1', 'desc2']),
                                              DocDescription('name2', '(c, d)', int,
                                                             ['desc3', DocEquation('desc4')])])])
    assert doc1 != 1
    assert Docstring(['a', 'b']) != Docstring(['a', 'b', 'c'])
    assert Docstring(['a', 'b']) != Docstring(['a', DocSection('x', 'b')])
    assert Docstring(DocSection('a', 'b')) != Docstring(DocSection('a', ['b', 'c']))
    assert Docstring(DocSection('a', 'b')) != Docstring(DocSection('a', 'c'))
    assert (Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))) !=
            Docstring(DocSection('a', DocDescription('1', 'y', 'z', 'k'))))
    assert (Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))) !=
            Docstring(DocSection('a', DocDescription('x', '1', 'z', 'k'))))
    assert (Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))) !=
            Docstring(DocSection('a', DocDescription('x', 'y', '1', 'k'))))
    assert (Docstring(DocSection('a', DocDescription('x', 'y', 'z', 'k'))) !=
            Docstring(DocSection('a', DocDescription('x', 'y', 'z', '1'))))
    assert (Docstring(DocSection('a', DocDescription('x', 'y', 'z', DocEquation('k')))) !=
            Docstring(DocSection('a', DocDescription('x', 'y', 'z', DocEquation('1')))))
    assert doc1.__dict__ == doc2.__dict__


def test_parse_numpy():
    """Tests docinstance.numpy.parse_numpy."""
    # monkeypatch equality for Docstring
    Docstring.__eq__ = lambda self, other: self.__dict__ == other.__dict__
    # summary
    docstring = 'summary'
    assert parse_numpy(docstring) == Docstring(Summary('summary'))
    docstring = 'summary\n'
    assert parse_numpy(docstring) == Docstring(Summary('summary'))
    docstring = '\nsummary\n'
    assert parse_numpy(docstring) == Docstring(Summary('summary'))
    docstring = '    """summary\n    """'
    assert parse_numpy(docstring, contains_quotes=True) == Docstring(Summary('summary'))
    # FIXME: this should raise an error
    docstring = '\n\nsummary\n'
    assert parse_numpy(docstring), Docstring([Summary('summary')])
    docstring = '"""\n\nsummary\n"""'
    with pytest.raises(ValueError):
        parse_numpy(docstring, contains_quotes=True)
    docstring = '    """\n\n    summary\n    """'
    with pytest.raises(ValueError):
        parse_numpy(docstring, contains_quotes=True)
    docstring = 'summary\na'
    with pytest.raises(ValueError):
        parse_numpy(docstring)

    # extended
    docstring = 'summary\n\nblock1\n\nblock2'
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'), ExtendedSummary(['block1', 'block2'])]))
    docstring = '\nsummary\n\nblock1\n\nblock2'
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'), ExtendedSummary(['block1', 'block2'])]))
    docstring = '\nsummary\n\n\n\nblock2\n\n'
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'), ExtendedSummary(['block2'])]))
    # FIXME: is this a bug?
    docstring = '\n\nsummary\n\nblock1\n\nblock2'
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'), ExtendedSummary(['block1', 'block2'])]))
    # extended + headers
    docstring = 'summary\n\nblock1\n\nblock2\n\nheader\n------\nstuff'
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'), ExtendedSummary(['block1', 'block2']),
                       DocSection('header', 'stuff')]))

    # header with bad divider (-----)
    docstring = 'summary\n\nblock1\n\nblock2\n\nheader1\n--\nstuff\n\n'
    with pytest.raises(ValueError):
        parse_numpy(docstring)

    for header in ['parameters', 'attributes', 'methods', 'returns', 'yields', 'raises',
                   'other parameters', 'see also']:
        # name + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert (parse_numpy(docstring) ==
                Docstring([Summary('summary'),
                           ExtendedSummary(['block1', 'block2']),
                           DocSection(header,
                                      DocDescription('abc',
                                                     descs=['description1.', 'description2.']))]))
        # name + types + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert (parse_numpy(docstring) ==
                Docstring([Summary('summary'),
                           ExtendedSummary(['block1', 'block2']),
                           DocSection(header,
                                      DocDescription('abc', types='str',
                                                     descs=['description1.', 'description2.']))]))
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc : {{str, int}}\n'
                     '    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert (parse_numpy(docstring) ==
                Docstring([Summary('summary'),
                           ExtendedSummary(['block1', 'block2']),
                           DocSection(header,
                                      DocDescription('abc', types=['str', 'int'],
                                                     descs=['description1.', 'description2.']))]))
        # name + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y)\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert (parse_numpy(docstring) ==
                Docstring([Summary('summary'),
                           ExtendedSummary(['block1', 'block2']),
                           DocSection(header,
                                      DocDescription('abc', signature='(x, y)',
                                                     descs=['description1.', 'description2.']))]))
        # name + types + signature + multiple descriptions
        docstring = ('summary\n\nblock1\n\nblock2\n\n{0}\n{1}\nabc(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert (parse_numpy(docstring) ==
                Docstring([Summary('summary'),
                           ExtendedSummary(['block1', 'block2']),
                           DocSection(header,
                                      DocDescription('abc', types='str', signature='(x, y)',
                                                     descs=['description1.', 'description2.']))]))
        # name + types + signature + multiple descriptions - extended summary
        docstring = ('summary\n\n{0}\n{1}\nabc(x, y): str\n    description1.\n'
                     '    description2.'.format(header.title(), '-'*len(header)))
        assert (parse_numpy(docstring) ==
                Docstring([Summary('summary'),
                           DocSection(header,
                                      DocDescription('abc', types='str', signature='(x, y)',
                                                     descs=['description1.', 'description2.']))]))
        # name + types
        docstring = ('summary\n\n{0}\n{1}\nabc: str\ndef: int'.format(header.title(),
                                                                      '-'*len(header)))
        assert (parse_numpy(docstring) ==
                Docstring([Summary('summary'), DocSection(header,
                                                          [DocDescription('abc', types='str'),
                                                           DocDescription('def', types='int')])]))


def test_parse_numpy_raw():
    """Test pydocstring.numpy_docstring.parse_numpy with raw strings."""
    docstring = '"""summary\n\nextended"""'
    assert (parse_numpy(docstring, contains_quotes=True) ==
            Docstring([Summary('summary'), ExtendedSummary('extended')]))
    docstring = 'r"""summary\n\nextended"""'
    with pytest.raises(NotImplementedError):
        parse_numpy(docstring, contains_quotes=True)


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
            [r'True if docstring contains \"\"\" or \'\'\'.'])
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
            [r'If quotes corresponds to a raw string, i.e. r\"\"\".'])


def test_parse_numpy_equations():
    """Test pydocstring.numpy_docstring.parse_numpy with equations."""
    # monkeypatch equality for Docstring
    Docstring.__eq__ = lambda self, other: self.__dict__ == other.__dict__
    # equation in extended
    docstring = ('summary\n\n.. math::\n\n    \\frac{1}{2}')
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'), ExtendedSummary(DocEquation('\\frac{1}{2}'))]))
    docstring = ('summary\n\n'
                 '.. math::\n\n'
                 '    x &= 2\\\\\n'
                 '    &= y\\\\\n')
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'),
                       ExtendedSummary(DocEquation('x &= 2\\\\\n&= y\\\\'))]))
    docstring = ('summary\n\n'
                 '.. math::\n\n'
                 '    x &= 2\\\\\n'
                 '    &= y\\\\\n'
                 'Parameters\n'
                 '----------\n'
                 'a')
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'),
                       ExtendedSummary(DocEquation('x &= 2\\\\\n&= y\\\\')),
                       Parameters(DocDescription('a'))]))

    # equation in parameter
    # single line equation
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n    '
                 '    \\frac{1}{2}')
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'),
                       Parameters(DocDescription('a', types='float',
                                                 descs=DocEquation('\\frac{1}{2}')))]))
    # multi line equation
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n'
                 '        \\frac{1}{2}\\\\\n        \\frac{1}{3}')
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'),
                       Parameters(DocDescription('a', types='float',
                                                 descs=DocEquation('\\frac{1}{2}\\\\\n'
                                                                   '\\frac{1}{3}\n')))]))
    # multiple equations
    docstring = ('summary\n\nParameters\n----------\na : float\n    .. math::\n\n'
                 '        \\frac{1}{2}\n    ..math::\n        \\frac{1}{3}')
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'),
                       Parameters(DocDescription('a', types='float',
                                                 descs=[DocEquation('\\frac{1}{2}'),
                                                        DocEquation('\\frac{1}{3}')]))]))
    # multiple equations and other descriptions
    docstring = ('summary\n\nParameters\n----------\na : float\n    Some float.\n    .. math::\n\n'
                 '        \\frac{1}{2}\n\n    Yes.\n    ..math::\n        \\frac{1}{3}\n'
                 '    This is the float.')
    assert (parse_numpy(docstring) ==
            Docstring([Summary('summary'),
                       Parameters(DocDescription('a', types='float',
                                                 descs=['Some float.',
                                                        DocEquation('\\frac{1}{2}'),
                                                        'Yes.',
                                                        DocEquation('\\frac{1}{3}'),
                                                        'This is the float.']))]))
