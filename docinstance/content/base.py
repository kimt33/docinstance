"""Base class for docstring contents."""


class DocContent:
    def __init__(self):
        """Initialize.

        Raises
        ------
        NotImplementedError
            Always.

        """
        raise NotImplementedError

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

    def make_numpy_docstring(self, width, indent_level, tabsize):
        """Return the docstring of the content in numpy style.

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
            Docstring of the given content in numpy style.

        Raises
        ------
        NotImplementedError
            Always.

        """
        raise NotImplementedError

    def make_google_docstring(self, width, indent_level, tabsize):
        """Return the docstring of the content in google style.

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
        NotImplementedError
            Always.

        """
        raise NotImplementedError

    def make_rst_docstring(self, width, indent_level, tabsize):
        """Return the docstring of the content in rst style.

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
            Docstring of the given content in rst style.

        Raises
        ------
        NotImplementedError
            Always.

        """
        raise NotImplementedError
