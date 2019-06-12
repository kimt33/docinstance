"""Base class for docstring contents."""


class DocContent:
    """Base class for all content of a docstring.

    Any special construct that goes inside a docstring (i.e. not a string) should be a child of this
    class.

    Methods
    -------
    __init__(self)
        Initialize.
    __eq__(self, other)
        Return True if other is DocContent instance with the same contents. False otherwise.
    __ne__(self, other)
        Return False if other is DocContent instance with the same contents. True otherwise.
    make_docstring(self, width, indent_level, tabsize, style)
        Return the docstring of the content in the given style.

    """

    def __eq__(self, other):
        """Return True if other is DocContent instance with the same contents. False otherwise.

        Parameters
        ----------
        other : DocContent

        Returns
        -------
        bool

        """
        return isinstance(other, DocContent) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return False if other is DocContent instance with the same contents. True otherwise.

        Parameters
        ----------
        other : DocContent

        Returns
        -------
        bool

        Notes
        -----
        The behaviour of __ne__ changed form Python 2 to Python 3. In Python 3, there is a default
        behaviour of __ne__ when __eq__ returns NotImplemented, which is the default behaviour for
        __eq__. Special care needs to be taken when only __ne__ is defined. However, since we define
        the __eq__ here, we don't need to be too careful. See
        https://stackoverflow.com/questions/4352244/python-should-i-implement-ne-operator-based-on-eq/50661674#50661674
        for more details.

        """
        return not self == other

    def make_docstring(self, width, indent_level, tabsize, style, **kwargs):
        """Return the docstring as a string in the given style.

        Parameters
        ----------
        width : int
            Maximum number of characters allowed in a line.
        indent_level : int
            Number of indents (tabs) that are needed for the docstring.
        tabsize : int
            Number of spaces that corresponds to a tab.
        style : str
            Name of the docstring style.
        kwargs : dict
            Other keyword arguments that will be passed onto the docstring maker of the given style.

        Returns
        -------
        content_docstring : str
            Docstring of the given content in the given style.

        Raises
        ------
        TypeError
            If `style` is not given as a non-empty string.
        NotImplementedError
            If the corresponding method for the given `style` is not defined.

        """
        if not (isinstance(style, str) and style != ""):
            raise TypeError("The `style` of the docstring must be given as a non-empty string.")
        method_name = "make_docstring_{}".format(style)
        if hasattr(self, method_name):
            return getattr(self, method_name)(width, indent_level, tabsize, **kwargs)
        raise NotImplementedError(
            "To make a docstring of style, {}, the given instance of {} must have a method called "
            "{} with arguments (width, indent_level, tabsize).".format(
                style, self.__class__, method_name
            )
        )
