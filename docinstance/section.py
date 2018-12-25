"""Class for representing a section in the docstring."""
from docinstance.utils import wrap
from docinstance.description import DocDescription


class DocSection:
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
    make_docstring(self, style, width, indent_level, tabsize)
        Return docstring in correponding style.
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
            If `contents` is not a string or a list/tuple of strings.

        """
        if not isinstance(header, str):
            raise TypeError("The parameter `header` must be a string.")
        self.header = header

        if isinstance(contents, (str, DocDescription)):
            contents = [contents]
        elif not (isinstance(contents, (tuple, list)) and
                  (all(isinstance(content, str) for content in contents) or
                   all(isinstance(content, DocDescription) for content in contents))):
            raise TypeError("The parameter `contents` must be a string, a list/tuple of strings, or"
                            " a list/tuple of DocDescription.")
        self.contents = list(contents)

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
            # FIXME: following is redundant because the wrap of the divider raises an error when it
            # is does not fit into the given width
            if len(title) > 1 or len(divider) > 1:
                raise ValueError('Title is too long for the given width and indentation.')
            output += '{0}\n{1}\n'.format(title[0], divider[0])
        # contents
        for paragraph in self.contents:
            # NOTE: since the contents are checked in the initialization, we will assume that the
            # paragraph can only be string or DocDescription
            if isinstance(paragraph, str):
                output += '\n'.join(wrap(paragraph, width=width, indent_level=indent_level,
                                         tabsize=tabsize))
                output += '\n\n'
            # if isinstance(paragraph, DocDescription)
            else:
                # FIXME: it would be nice if this part can be separated out into the
                # make_numpy_docstring_signature
                if include_signature:
                    output += paragraph.make_numpy_docstring_signature(width, indent_level, tabsize)
                else:
                    output += paragraph.make_numpy_docstring(width, indent_level, tabsize)
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
        """Return the docstring in google style.

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
            Docstring of the given section in google style.

        Raises
        ------
        NotImplementedError

        """
        raise NotImplementedError

    def make_rst_docstring(self, width, indent_level, tabsize):
        """Return the docstring in rst style.

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
            Docstring of the given section in rst style.

        Raises
        ------
        NotImplementedError

        """
        raise NotImplementedError
