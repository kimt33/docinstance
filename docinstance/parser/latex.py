"""Parser for Latex equations."""
import re
import inspect
from docinstance.content.equation import DocEquation


def is_math(text):
    """Check if the given text is a math equation in rst format.

    Parameters
    ----------
    text : str
        Text to check.

    Returns
    -------
    is_math :bool
        True if text is a math equation.
        False otherwise.

    """
    re_math = re.compile(r'^\s*\.\.\s*math::\n*(?:\n\s+.+)+\n*$')
    return bool(re_math.search(text))


def parse_equation(text):
    """Parse multiline math equation from the text.

    Parameters
    ----------
    text : str
        Text from which the math equation is extracted.

    Returns
    -------
    split_text : list of {str, DocEquation}
        Text where the math equations have been separated from the rest of the string.
        Equations are stored as instances of DocEquation.

    """
    re_math = re.compile(r'\s*(\.\.\s*math::\n*(?: +.+\n?)+)\n*')
    # split equations
    split_text = []
    for block in re_math.split(text):
        # remove empty blocks
        if block == '':
            continue
        # remove trailing newline
        if is_math(block):
            block = re.sub(r'\n*$', '', block)
            block = re.sub(r'^\s*\.\.\s*math::\n*', '', block)
            block = inspect.cleandoc(block)
            block = DocEquation(block)
        split_text.append(block)
    return split_text
