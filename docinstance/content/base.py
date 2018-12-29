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
