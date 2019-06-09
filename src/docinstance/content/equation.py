"""Class for representing math equations."""
from docinstance.utils import wrap
from docinstance.content.base import DocContent


class DocEquation(DocContent):
    """Multiple lines (block) of equations.

    Attributes
    ----------
    equations : list of str
        Multi-line string that consists of multiple equations.

    Methods
    -------
    __init__(self, equations)
        Initialize.
    make_numpy_docstring(self, style, width, indent_level, tabsize)
        Return docstring in correponding style.

    """

    def __init__(self, equations):
        """Initialize.

        Parameters
        ----------
        equations : str
           Multi-line string that consists of multiple equations.

        Raises
        ------
        TypeError
            If given equations are not string.

        """
        if not isinstance(equations, str):
            raise TypeError("Equations must be given as one string.")
        self.equations = equations.split("\n")
        if self.equations[-1] == "":
            self.equations = self.equations[:-1]

    def make_numpy_docstring(self, width, indent_level, tabsize):
        """Return the docstring in numpy style.

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
        equation_docstring : str
            Docstring of the given equations in numpy style.

        Raises
        ------
        ValueError
            If the width is too small to fit the equation for the given indent and tabsize.

        """
        output = ""
        if len(self.equations) == 1:
            first_line = wrap(
                ".. math:: " + self.equations[0],
                width=width,
                indent_level=indent_level,
                tabsize=tabsize,
            )
            if len(first_line) == 1:
                output += first_line[0]
                output += "\n\n"
                return output
        first_line = wrap(".. math:: ", width=width, indent_level=indent_level, tabsize=tabsize)
        if len(first_line) != 1:
            raise ValueError(
                "Given line width is too small to fit the equation for the given "
                "indent and tab size"
            )
        output += first_line[0]
        output += "\n\n"
        output += "\n".join(
            "\n".join(wrap(equation, width=width, indent_level=indent_level + 1, tabsize=tabsize))
            for equation in self.equations
        )
        output += "\n\n"
        return output
