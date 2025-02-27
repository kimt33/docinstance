"""Class for representing a section in the docstring."""
from docinstance.utils import wrap, wrap_indent_subsequent
from docinstance.content.base import DocContent
from docinstance.content.description import DocDescription


class DocSection(DocContent):
    """Section within a docstring.

    Attributes
    ----------
    header : str
        Name of the section to be used within the docstring.
    contents : {list of str, list of DocDescription}
        Contents within the section.

    Methods
    -------
    __init__(self, header, contents)
        Initialize.
    make_numpy_docstring(self, width, indent_level, tabsize, include_signature=False)
        Return the docstring in numpy style.
    make_numpy_docstring_signature(self, width, indent_level, tabsize)
        Return the docstring in numpy style modified to include signature.

    """

    def __init__(self, header, contents):
        """Initialize.

        Parameters
        ----------
        header : str
            Name of the section.
        contents : {str, list/tuple of str, list/tuple of DocDescription}
            Contents of the section.
            If a string is provided, then this string will be treated as a paragraph in the section.
            If multiple strings is provided via a list/tuple, then each string will be treated as a
            paragraph in the section and will be separate from one another by two newlines.
            If multiple DocDescription's are provided, then each DocDescription will be separate
            from one another by a newline.

        Raises
        ------
        TypeError
            If `header` is not a string.
            If `contents` is not a string, a list/tuple of DocDescription, or a list/tuple of
            string/DocContent where none of the DocContent instances are also instances of
            DocDescription.

        """
        if not isinstance(header, str):
            raise TypeError("The parameter `header` must be a string.")
        self.header = header

        if isinstance(contents, (str, DocContent)):
            contents = [contents]
        # NOTE: is it really necessary to prevent contents of a section from mixing
        # strings/DocContent and DocDescription?
        elif not (isinstance(contents, (tuple, list)) and
                  (all(isinstance(content, (str, DocContent)) and
                       not isinstance(content, DocDescription) for content in contents) or
                   all(isinstance(content, DocDescription) for content in contents))):
            raise TypeError("The parameter `contents` must be a string, a list/tuple of "
                            "DocDescription, or a list/tuple of strings/DocContent (not "
                            "DocDescription).")
        self.contents = list(contents)

    # pylint: disable=W0221
    # the extra argument is used in the make_numpy_docstring_signature
    def make_numpy_docstring(self, width, indent_level, tabsize, include_signature=False):
        """Return the docstring in numpy style.

        Parameters
        ----------
        width : int
            Maximum number of characters allowed in a line.
        indent_level : int
            Number of indents (tabs) that are needed for the docstring.
        tabsize : int
            Number of spaces that corresponds to a tab.
        include_signature : {bool, False}
            Flag for modifying the numpy docstring format to include the signature of a function.
            Default is False.

        Returns
        -------
        section_docstring : str
            Docstring of the given section in numpy style.

        Raises
        ------
        ValueError
            If the title is too long for the given width and indentation.

        """
        output = ''
        # title
        if self.header != '':
            title = wrap(self.header.title(), width=width, indent_level=indent_level,
                         tabsize=tabsize)
            divider = wrap('-' * len(self.header), width=width, indent_level=indent_level,
                           tabsize=tabsize)
            # NOTE: error will be raised if the line width is not wide enough to fit the title and
            # the divider in one line because the divider is one word and wrap will complain if the
            # line width is not big enough to fit the first word
            output += '{0}\n{1}\n'.format(title[0], divider[0])
        # contents
        for paragraph in self.contents:
            # NOTE: since the contents are checked in the initialization, we will assume that the
            # paragraph can only be string or DocDescription
            if isinstance(paragraph, str):
                output += '\n'.join(wrap(paragraph, width=width, indent_level=indent_level,
                                         tabsize=tabsize))
                output += '\n\n'
            # if isinstance(paragraph, DocContent)
            elif include_signature and hasattr(paragraph, 'make_numpy_docstring_signature'):
                output += paragraph.make_numpy_docstring_signature(width, indent_level, tabsize)
            else:
                output += paragraph.make_numpy_docstring(width, indent_level, tabsize)
        # pylint: disable=W0120
        # following block clause should always be executed
        else:
            # end a section with two newlines (note that the section already ends with a newline if
            # it ends with a paragraph)
            output += '\n' * isinstance(paragraph, DocDescription)

        return output

    def make_numpy_docstring_signature(self, width, indent_level, tabsize):
        """Return the docstring in numpy style modified to include signature.

        Parameters
        ----------
        width : int
            Maximum number of characters allowed in a line.
        indent_level : int
            Number of indents (tabs) that are needed for the docstring.
        tabsize : int
            Number of spaces that corresponds to a tab.

        Returns
        -------
        section_docstring : str
            Docstring of the given section in numpy style that includes the signature.

        Raises
        ------
        ValueError
            If the title is too long for the given width and indentation.
            If any of the paragraph is neither a string nor a DocDescription instance.

        """
        return self.make_numpy_docstring(width, indent_level, tabsize, include_signature=True)

    def make_google_docstring(self, width, indent_level, tabsize):
        """Return the docstring of the section in google style.

        Parameters
        ----------
        width : int
            Maximum number of characters allowed in a line.
        indent_level : int
            Number of indents (tabs) that are needed for the docstring.
        tabsize : int
            Number of spaces that corresponds to a tab.

        Returns
        -------
        content_docstring : str
            Docstring of the given content in google style.

        Raises
        ------
        ValueError
            If the title is too long for the given width and indentation.

        """
        output = ''
        # title
        if self.header != '':
            title = wrap('{0}:'.format(self.header.title()),
                         width=width, indent_level=indent_level, tabsize=tabsize)
            if len(title) > 1:
                raise ValueError('The header must fit into the given width with the indentation')
            output += title[0]
            output += '\n'
        else:
            # don't indent the contents if there is no header
            indent_level -= 1
        # contents
        for paragraph in self.contents:
            # NOTE: since the contents are checked in the initialization, we will assume that the
            # paragraph can only be string or DocDescription
            if isinstance(paragraph, str):
                output += '\n'.join(wrap(paragraph, width=width, indent_level=indent_level+1,
                                         tabsize=tabsize))
                output += '\n\n'
            # if isinstance(paragraph, DocContent)
            else:
                output += paragraph.make_google_docstring(width, indent_level+1, tabsize)
        # pylint: disable=W0120
        # following block clause should always be executed
        else:
            # end a section with two newlines (note that the section already ends with a newline if
            # it ends with a paragraph)
            output += '\n' * isinstance(paragraph, DocDescription)

        return output

    def make_rst_docstring(self, width, indent_level, tabsize):
        """Return the docstring in sphinx's rst format.

        Parameters
        ----------
        width : int
            Maximum number of characters allowed in a line.
        indent_level : int
            Number of indents (tabs) that are needed for the docstring.
        tabsize : int
            Number of spaces that corresponds to a tab.

        Returns
        -------
        content_docstring : str
            Docstring of the given content in sphinx's rst style.

        """
        output = ''
        header = ''
        special_headers = {'see also': 'seealso', 'warnings': 'warning', 'warning': 'warning',
                           'notes': 'note', 'note': 'note', 'to do': 'todo', 'todo': 'todo'}

        if self.header.lower() in special_headers:
            header = '.. {0}::'.format(special_headers[self.header.lower()])
        elif self.header != '':
            output += ':{0}:\n\n'.format(self.header.title())

        for i, paragraph in enumerate(self.contents):
            # first content must be treated with care for special headers
            if i == 0 and self.header.lower() in special_headers:
                # str
                if isinstance(paragraph, str):
                    text = '{0} {1}'.format(header, paragraph)
                    # FIXME: following can probably be replaced with a better wrapping function
                    first_content = [' ' * indent_level * tabsize + line for line in
                                     wrap_indent_subsequent(text,
                                                            width=width - indent_level*tabsize,
                                                            indent_level=indent_level+1,
                                                            tabsize=tabsize)]
                    output += '\n'.join(first_content)
                    output += '\n'
                # DocContent
                else:
                    output += header
                    output += '\n'
                    output += paragraph.make_rst_docstring(width=width,
                                                           indent_level=indent_level+1,
                                                           tabsize=tabsize)
                # indent all susequent content
                indent_level += 1
            elif isinstance(paragraph, str):
                output += '\n'.join(wrap(paragraph, width=width, indent_level=indent_level,
                                         tabsize=tabsize))
                # NOTE: the second newline may cause problems (because the field might not
                # recognize text that is more than one newline away)
                output += '\n\n'
            else:
                output += paragraph.make_rst_docstring(width, indent_level, tabsize)
        # pylint: disable=W0120
        # following block clause should always be executed
        else:
            # end a section with two newlines (note that the section already ends with a newline
            # if it ends with a paragraph)
            output += '\n' * isinstance(paragraph, DocDescription)

        return output


# FIXME: make a special class for summary
class Summary(DocSection):
    """First line of the docstring.

    Attributes
    ----------
    header : ''
        Name of the section to be used within the docstring.
    contents : list of str
        Contents within the section.

    Methods
    -------
    __init__(self, header, contents)
        Initialize.
    make_numpy_docstring(self, width, indent_level, tabsize, include_signature=False)
        Return the docstring in numpy style.
    make_numpy_docstring_signature(self, width, indent_level, tabsize)
        Return the docstring in numpy style modified to include signature.

    """

    def __init__(self, contents):
        """Initialize.

        Parameters
        ----------
        contents : str
            First line of docstring.

        Raises
        ------
        TypeError
            If the given content is not a string.

        """
        self.header = ''
        if not isinstance(contents, str):
            raise TypeError("The parameter `contents` must be a string.")
        self.contents = [contents]

    def make_docstring(self, width, indent_level, tabsize, summary_only=False, special=False):
        """Return the docstring for the summary.

        Parameters
        ----------
        width : int
            Maximum number of characters allowed in a line.
        indent_level : int
            Number of indents (tabs) that are needed for the docstring.
        tabsize : int
            Number of spaces that corresponds to a tab.
        summary_only : {bool, False}
            Flag for indicating that there is only summary in the docstring.
            If True, then newlines are not added to the output if the summary can fit both triple
            quotations on either side. Otherwise, newlines are added.
            By default, False.
        special : {bool, False}
            Flag for indicating that the docstring is raw or is unicode.
            By default, False.

        Returns
        -------
        summary : str
            First line of the docstring.

        Raises
        ------
        ValueError
            If the title is too long for the given width and indentation.

        """
        output = ''
        summary = self.contents[0]
        # if summary cannot fit into first line with one triple quotation
        # if len(summary) + ' ' * indent_level * tabsize > width - 3:
        if len(wrap(summary, width - 3 - int(special), indent_level, tabsize)) > 1:
            output += '\n'
            # if summary cannot fit into the second line (without tripple quotation)
            # if len(summary) + ' ' * indent_level * tabsize > width:
            if len(wrap(summary, width, indent_level, tabsize)) > 1:
                raise ValueError('First section of the docstring (summary) must fit completely into'
                                 ' the first line of the docstring (including the triple quotation)'
                                 ' or the second line.')
        output += summary
        # if summary only and summary can fit into the first line with two triple quotations
        if not (summary_only and
                len(wrap(summary, width - 6 - int(special), indent_level, tabsize)) == 1):
            output += '\n\n'
        return output


# pylint: disable=C0103
dict_classname_headers = {'ExtendedSummary': '', 'Parameters': None, 'Attributes': None,
                          'Methods': None, 'Returns': None, 'Yields': None,
                          'OtherParameters': 'other parameters', 'Raises': None, 'Warns': None,
                          'Warnings': None, 'SeeAlso': 'see also', 'Notes': None,
                          'References': None, 'Examples': None}


# factory for init
def make_init(header):
    """Return init function.

    Parameters
    ----------
    header : str
        Name of the section.

    Returns
    -------
    __init__(self, contents)
        Init function where the header is fixed and is removed as a parameter.

    Notes
    -----
    Factory is used to ensure that the function is bound early rather than late. The __init__ can be
    declared within the for loop where value of the header is received from the local scope within
    the for loop. However, the function will be late binding, meaning that the value of the header
    will be looked up when the function is called. We can force early binding with a factory.

    See https://stackoverflow.com/questions/3431676/creating-functions-in-a-loop for more details.

    """
    def __init__(self, contents):
        """Initialize.

        Parameters
        ----------
        contents : {str, list/tuple of str, list/tuple of DocDescription}
            Contents of the section.
            If a string is provided, then this string will be treated as a paragraph in the section.
            If multiple strings is provided via a list/tuple, then each string will be treated as a
            paragraph in the section and will be separate from one another by two newlines.
            If multiple DocDescription's are provided, then each DocDescription will be separate
            from one another by a newline.

        Raises
        ------
        TypeError
            If `header` is not a string.
            If `contents` is not a string or a list/tuple of strings.

        """
        super(self.__class__, self).__init__(header, contents)

    return __init__


# declare classes from string
for class_name, section_header in dict_classname_headers.items():
    # if header is None, then it is assumed to be the same as the clas sname
    if section_header is None:
        section_header = class_name.lower()

    # globals is the dictionary of the current module for the symbols
    # types is used to instantiate a class (because all classes are instances of type)
    globals()[class_name] = type(class_name, (DocSection,), {'__init__': make_init(section_header)})
