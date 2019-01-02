"""Class for representing the docstring."""
from docinstance.content.base import DocContent
from docinstance.content.section import DocSection, Summary


class Docstring:
    """Class that contains the information in a docstring.

    Attributes
    ----------
    sections : list of DocSection
        Sections of the docstring.
    default_style : str
        Default style of the docstring.

    Methods
    -------
    __init__(self, sections, default_style)
        Initialize.
    make_docstring(self, style='numpy', width=100, indent_level=0, tabsize=4)
        Return the docstring in the given style.

    """

    def __init__(self, sections, default_style='numpy'):
        """Initialize.

        Parameters
        ----------
        sections : {str, list/tuple of str, list/tuple of DocSection}
            Sections of the docstring.
        default_style : {'numpy with signature', 'google', 'rst', 'numpy'}
            Style of the docstring.

        Raises
        ------
        TypeError
            If sections is not a string, list/tuple of strings, or list/tuple of DocSection
            instances.
        ValueError
            If there are no sections.
            If style is not one of 'numpy', 'numpy with signature', 'google', 'rst'.

        """
        if isinstance(sections, (str, DocContent)):
            sections = [sections]
        elif not (isinstance(sections, (list, tuple)) and
                  all(isinstance(i, (str, DocContent)) for i in sections)):
            raise TypeError('Sections of the docstring must be provided as a string, list/tuple of '
                            'strings, or list/tuple of DocContent instances.')
        # NOTE: should the empty sections be allowed?
        elif not sections:
            raise ValueError('At least one section must be provided.')
        self.sections = [section if isinstance(section, DocSection) else DocSection('', section)
                         for section in sections]

        if default_style not in ['numpy', 'numpy with signature', 'google', 'rst']:
            raise ValueError("Default style must be one of 'numpy', 'numpy with signature', "
                             "'google', 'rst'.")
        self.default_style = default_style

    # pylint: disable=R0912
    def make_docstring(self, width=100, indent_level=0, tabsize=4, style=None):
        """Return the docstring in the given style.

        Parameters
        ----------
        width : {int, 100}
            Maximum number of characters allowed in a line.
            Default is 100 characters.
        indent_level : {int, 0}
            Number of indents (tabs) that are needed for the docstring.
            Default is 0.
        tabsize : {int, 4}
            Number of spaces that corresponds to a tab.
            Default is 4.
        style : {'numpy', 'google', 'rst', 'numpy with signature', None}
            Style of the docstring.
            Default is the `default_style`.

        Returns
        -------
        section_docstring : str
            Docstring that correspond to the given section.

        Raises
        ------
        TypeError
            If width is not an integer.
            If indent_level is not an integer.
            If tabsize is not an integer.
        ValueError
            If width is less than or equal to zero.
            If indent_level is less than zero.
            If tabsize is less than or equal to zero.
            If the given style is not 'numpy', 'numpy with signature', google', or 'rst'.
            If the sections are not ordered correctly according to the given style.
            If the first section of the docstring (summary) does not have an empty header.
            If the first section of the docstring (summary) does not consist of one string.
            If the first section of the docstring (summary) does not fit completely into the first
            line of the docstring (including the triple quotation) or the second line.

        """
        if style is None:
            style = self.default_style
        # check input
        if not isinstance(width, int):
            raise TypeError('Maximum width of the line must be given as an integer.')
        elif width <= 0:
            raise ValueError('Maximum width of the line must be greater than zero.')

        if not isinstance(indent_level, int):
            raise TypeError('Level of indentation must be given as an integer.')
        elif indent_level < 0:
            raise ValueError('Level of indentation must be greater than or equal to zero.')

        if not isinstance(tabsize, int):
            raise TypeError('Number of spaces in a tab must be given as an integer.')
        elif tabsize <= 0:
            raise ValueError('Number of spaces in a tab must be greater than zero.')

        if style == 'numpy':
            docstring_func = 'make_numpy_docstring'
        elif style == 'numpy with signature':
            docstring_func = 'make_numpy_docstring_signature'
        elif style == 'google':
            docstring_func = 'make_google_docstring'
        elif style == 'rst':
            docstring_func = 'make_rst_docstring'
        else:
            raise ValueError("Given docstring style must be one of 'numpy', 'numpy with signature',"
                             " 'google', 'rst'.")

        # FIXME: this may not be necessary and can be removed
        if not self.check_section_order(style):
            raise ValueError('Sections must be ordered according to the guideline set by the given '
                             'docstring style.')

        output = ''
        # check that first section does not have a header
        if self.sections[0].header != '':
            raise ValueError('First section of the docstring (summary) must have an empty header.')
        # add summary
        summary = Summary(self.sections[0].contents[0])
        output += summary.make_docstring(width, indent_level, tabsize,
                                         summary_only=(len(self.sections) ==
                                                       len(self.sections[0].contents) == 1))
        # add remaining summary
        if len(self.sections[0].contents) > 1:
            summary = DocSection('', self.sections[0].contents[1:])
            output += getattr(summary, docstring_func)(width, indent_level, tabsize)
        # add other sections
        if len(self.sections) > 1:
            for section in self.sections[1:]:
                output += getattr(section, docstring_func)(width, indent_level, tabsize)
        # add whitespace to indent the triple quotation
        output += ' ' * indent_level * tabsize
        return output

    # TODO: add ordering of the other styles. It seems that only numpy cares about the ordering of
    # the sections.
    # FIXME: this may not be necessary and can be removed
    def check_section_order(self, style):
        """Check that the sections are correctly ordered for the given style.

        Parameters
        ----------
        style : {'numpy', 'google', 'rst', 'numpy with signature'}
            Style of the docstring.

        Returns
        -------
        bool
            True if the sections are ordered correctly.
            False otherwise.

        Raises
        ------
        ValueError
            If an unidentified section is used and the style does not permit the use of unidentified
            sections.

        """
        allow_other_sections = True
        # FIXME: default value should be arbitrarily large (in case for whatever reason, there are
        # sections with values over 99)
        default_value = 99
        # only numpy seems to care about the ordering
        if style == 'numpy':
            ordering = {'': 0, 'parameters': 1, 'attributes': 2, 'methods': 3, 'returns': 4,
                        'yields': 4, 'other parameters': 5, 'raises': 6, 'warns': 7, 'warnings': 8,
                        'see also': 9, 'notes': 10, 'references': 11, 'examples': 12}
            allow_other_sections = False
        else:
            ordering = {}
        order_values = [ordering.get(section.header.lower(), default_value)
                        for section in self.sections]
        if not allow_other_sections and any(i == default_value for i in order_values):
            raise ValueError('For the docstring style, {0}, the headings of the sections must be '
                             'one of {1}'.format(style, list(ordering.keys())))
        return all(i <= j for i, j in zip(order_values, order_values[1:]))
