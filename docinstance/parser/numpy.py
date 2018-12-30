"""Parser for numpy docstring."""
import re
import inspect
from docinstance.parser.latex import parse_equation
from docinstance.docstring import Docstring
from docinstance.content.description import DocDescription
from docinstance.content.section import (DocSection, Summary, ExtendedSummary, Parameters,
                                         Attributes, Methods, Returns, Yields, OtherParameters,
                                         Raises, Warns, Warnings, SeeAlso, Notes, References,
                                         Examples)
from docinstance.content.equation import DocEquation


def parse_numpy(docstring, contains_quotes=False):
    """Parse a docstring in numpy format into a Docstring instance.

    Multiple descriptions of the indented information (e.g. parameters, attributes, methods,
    returns, yields, raises, see also) are distinguished from one another with a period.
    If the period is not present, then the description is assumed to be a multiline description.

    Parameters
    ----------
    docstring : str
        Numpy docstring.
    contains_quotes : bool
        True if docstring contains \"\"\" or \'\'\'.

    Returns
    -------
    docstring : Docstring
       Instance of Docstring that contains the necessary information.

    Raises
    ------
    ValueError
        If summary is not in the first or second line.
        If summary is now followed with a blank line.
        If number of '-' does not match the number of characters in the header.
        If given entry of the tabbed information (parameters, attributes, methods, returns, yields,
        raises, see also) had an unexpected pattern.
    NotImplementedError
        If quotes corresponds to a raw string, i.e. r\"\"\".

    Notes
    -----
    Copied from https://github.com/kimt33/pydocstring.

    """
    docstring = inspect.cleandoc('\n' * contains_quotes + docstring)

    # remove quotes from docstring
    if contains_quotes:
        quotes = r'[\'\"]{3}'
        if re.search(r'^r{0}'.format(quotes), docstring):
            raise NotImplementedError('A raw string quotation, i.e. r""" cannot be given as a '
                                      'string, i.e. from reading a python file as a string, '
                                      'because the backslashes belonging to escape sequences '
                                      'cannot be distinguished from those of normal backslash.'
                                      'You either need to change existing raw string to normal '
                                      'i.e. convert all occurences of \\ to \\\\, or import the '
                                      'docstring from the instance through `__doc__` attribute.')
    else:
        quotes = r''
    docstring = re.sub(r'^{0}'.format(quotes), '', docstring)
    docstring = re.sub(r'{0}$'.format(quotes), '', docstring)

    sections = []
    # summary
    for regex in [r'^\n?(.+?)\n\n+', r'^\n?(.*?)\n*$']:
        re_summary = re.compile(regex)
        try:
            sections.append(Summary(re_summary.search(docstring).group(1)))
            break
        except AttributeError:
            pass
    else:
        raise ValueError('The summary must be in the first or the second line with a blank line '
                         'afterwards.')
    # remove summary from docstring
    docstring = re_summary.sub('', docstring)
    if docstring == '':
        return Docstring(sections)

    # if headers do not exist
    re_header = re.compile(r'\n*(.+)\n(-+)\n+')
    if re_header.search(docstring) is None:
        # split into blocks by math equations and multiple newlines
        extended = [[lines] if isinstance(lines, DocEquation) else re.split(r'\n\n+', lines)
                    for lines in parse_equation(docstring)]
        extended = [line for lines in extended for line in lines]
        extended_contents = []
        for block in extended:
            # NOTE: all newlines at the end of the docstring will be removed by inspect.cleandoc. So
            # there is no empty blocks
            # if block == '':
            #     continue
            if not isinstance(block, DocEquation):
                # remove quotes
                block = re.sub(r'\n*{0}$'.format(quotes), '', block)
                # remove trailing newlines
                block = re.sub(r'\n+$', '', block)
                # replace newlines
                block = block.replace('\n', ' ')
            extended_contents.append(block)
        sections.append(ExtendedSummary(extended_contents))
        return Docstring(sections)

    # split docstring by the headers
    split_docstring = re_header.split(docstring)
    # 0th element is always the extended summary, 1st element is the header, 2nd element is the
    # ----- divider
    extended, *split_docstring = split_docstring
    # FIXME: repeated code
    # extract math and split blocks
    extended = [[lines] if isinstance(lines, DocEquation) else re.split(r'\n\n+', lines)
                for lines in parse_equation(extended)]
    extended = [line for lines in extended for line in lines]
    # process blocks
    processed_extended = []
    for block in extended:
        # NOTE: all newlines at the end of the docstring will be removed by inspect.cleandoc. So
        # there is no empty blocks
        # if block == '':
        #     continue
        if not isinstance(block, DocEquation):
            # remove quotes
            block = re.sub(r'\n*{0}$'.format(quotes), '', block)
            # remove trailing newlines
            block = re.sub(r'\n+$', '', block)
            # replace newlines
            block = block.replace('\n', ' ')
        processed_extended.append(block)

    if processed_extended != []:
        sections.append(ExtendedSummary(processed_extended))

    headers_sections = {'parameters': Parameters, 'other parameters': OtherParameters,
                        'attributes': Attributes, 'methods': Methods, 'returns': Returns,
                        'yields': Yields, 'raises': Raises, 'see also': SeeAlso, 'warns': Warns,
                        'warnings': Warnings, 'examples': Examples, 'references': References,
                        'notes': Notes, 'properties': None, 'abstract properties': None,
                        'abstract methods': None}
    for header, lines, contents in zip(split_docstring[0::3],
                                       split_docstring[1::3],
                                       split_docstring[2::3]):
        contents = re.sub(r'\n+$', r'\n', contents)

        if len(header) != len(lines):
            raise ValueError('Need {0} of `-` underneath the header title, {1}'
                             ''.format(len(header), header))

        header = header.lower()
        header_contents = []
        # special headers (special format for each entry)
        if header in headers_sections:
            entries = (entry for entry in re.split(r'\n(?!\s+)', contents) if entry != '')
            # FIXME: following regular expression would work only if docstring has spaces adjacent
            #        to ':'
            re_entry = re.compile(r'^(.+?)(\(.+?\))?(?: *: *(.+))?(?:\n|$)')
            for entry in entries:
                # keep only necessary pieces
                _, name, signature, types, descs = re_entry.split(entry)

                # process signature
                if signature is None:
                    signature = ''
                else:
                    signature = ', '.join(i.strip() for i in signature.split(','))

                # process types
                if types is None:
                    types = []
                elif re.search(r'\{.+\}', types):
                    types = re.search(r'^\{((?:(.+?),\s*)*(.+?))\}$', types).group(1)
                    types = re.split(r',\s*', types)
                else:
                    types = re.search(r'^((?:(.+?),\s*)*(.+?))$', types).group(1)
                    types = re.split(r',\s*', types)
                types = [i for i in types if i is not None]

                # process documentation
                descs = inspect.cleandoc('\n' + descs)
                # NOTE: period is used to terminate a description. i.e. one description is
                #       distinguished from another with a period and a newline.
                descs = re.split(r'\.\n+', descs)
                # add period (only the last line is not missing the period)
                descs = [line + '.' for line in descs[:-1]] + descs[-1:]
                # extract equations
                descs = [line for lines in descs for line in parse_equation(lines)]
                # non math blocks will replace newlines with spaces.
                # math blocks will add newline at the end
                descs = [line if isinstance(line, DocEquation) else line.replace('\n', ' ')
                         for line in descs]

                # store
                header_contents.append(DocDescription(name, signature=signature, types=types,
                                                      descs=descs))
        else:
            header_contents = [i for i in re.split(r'\n\n+', contents) if i != '']
        try:
            sections.append(headers_sections[header](header_contents))
        except KeyError:
            sections.append(DocSection(header, header_contents))
    return Docstring(sections)
