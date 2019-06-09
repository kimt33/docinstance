"""Utility functions for handling strings and attributes of an object."""
import inspect
import os
import textwrap


def wrap(text, width=100, indent_level=0, tabsize=4, **kwargs):
    """Wrap a text with the given line length and indentations.

    Parameters
    ----------
    text : str
        Text that will be wrapped into different lines such that each line is indented and is less
        than the given length.
    width : int
        Maximum number of characters allowed in each line.
    indent_level : int
        Number of indents (tabs) that are needed for the docstring.
    tabsize : int
        Number of spaces that corresponds to a tab.
    kwargs : dict
        Other options for the textwrap.fill.
        By default,
            - tabs are replaced with spaces ('expand_tabs': True),
            - whitespaces are not replaced ('replace_whitespace': False),
            - whitespaces (that are not indentations) before or after sentences are dropped
              ('drop_whitespace': True)
            - long words are not broken into smaller pieces ('break_long_words': False)
        subsequent_indent : str
            String that will be prepended to all lines save the first of wrapped output; also counts
            towards each line's width.

    Returns
    -------
    output : list of str
        Text that has been wrapped to the given length and indentation where each line is an element
        of the list.
        If there are any newline characters present in the text, the text will first be divided
        according to the newlines and will be wrapped aftewards.
        Whitespace (excluding newline) at the end of each (newline-separated) line is discarded.
        Whitespace (excluding newline) at the beginning of each (newline-separated) line is
        discarded only if the first word cannot fit into the given line width with the whitespace.

    Raises
    ------
    ValueError
        If the the amount indented is greater than the maximum width.
        If is a word plus its indentation is longer than the width.

    """
    kwargs.setdefault("expand_tabs", True)
    kwargs.setdefault("replace_whitespace", False)
    kwargs.setdefault("drop_whitespace", True)
    kwargs.setdefault("break_long_words", False)
    kwargs["tabsize"] = tabsize
    if width <= tabsize * indent_level:
        raise ValueError("Amount of indentation must be less than the maximum width.")
    kwargs["width"] = width - tabsize * indent_level

    # NOTE: uncomment to remove whitespace at the beginning and the end
    # text = text.strip()
    # Acknowledge all of the newlines (start, middle, and end)
    lines = text.split("\n")
    # wrap each line (separated by newline) separately
    wrapped_lines = [
        wrapped_line
        for unwrapped_line in lines
        for wrapped_line in (
            textwrap.wrap(unwrapped_line, **kwargs) if unwrapped_line != "" else [""]
        )
    ]
    # indent
    output = [" " * tabsize * indent_level + line for line in wrapped_lines]

    if any(len(line) > width for line in output):
        raise ValueError(
            "There cannot be any word (after indentation) that exceeds the maximum " "width"
        )
    return output


def wrap_indent_subsequent(text, width=100, indent_level=0, tabsize=4):
    """Wrap a text where first line is not indented.

    Parameters
    ----------
    text : str
        Text that will be wrapped into different lines such that each line is indented and is less
        than the given length.
    width : int
        Maximum number of characters allowed in each line.
    indent_level : int
        Number of indents (tabs) that are needed for the docstring.
    tabsize : int
        Number of spaces that corresponds to a tab.

    Returns
    -------
    output : list of str
        Text that has been wrapped to the given length and indentation where each line is an element
        of the list.
        If there are any newline characters present in the text, the text will first be divided
        according to the newlines and will be wrapped aftewards.
        Whitespace (excluding newline) at the end of each (newline-separated) line is discarded.
        Whitespace (excluding newline) at the beginning of each (newline-separated) line is
        discarded only if the first word cannot fit into the given line width with the whitespace.

    """
    output = wrap(
        text, width=width, indent_level=0, tabsize=0, subsequent_indent=" " * tabsize * indent_level
    )
    return output


def extract_members(module):
    """Extract all members of a module that are defined in the same file.

    Parameters
    ----------
    module : object
        Any python object.

    Returns
    -------
    output : dict of str to object
        Dictionary of the name of the object to the object.

    """
    # get file location
    filename = inspect.getsourcefile(module)
    # find objects that are defined in the provided module
    output = {}
    for name, member in module.__dict__.items():
        try:
            # NOTE: inspect.getsourcefile only works on a module, class, method, function,
            # traceback, frame, or code objects. Not properties.
            if os.path.samefile(inspect.getsourcefile(member), filename):
                output[name] = member
        except TypeError:
            if isinstance(member, property):
                output[name] = member
    return output
