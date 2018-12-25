import textwrap


def wrap(text, width=100, indent_level=0, tabsize=4, **kwargs):
    """Wrap a text with the given line length and indentations.

    Parameters
    ----------
    text : str
        Text that will be wrapped.
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

    Returns
    -------
    output : list of str
        Text that has been wrapped to the given length and indentation where each line is an element
        of the list.

    Raises
    ------
    ValueError
        If the the amount indented is greater than the maximum width.
        If is a word plus its indentation is longer than the width.

    """
    kwargs.setdefault('expand_tabs', True)
    kwargs.setdefault('replace_whitespace', False)
    kwargs.setdefault('drop_whitespace', True)
    kwargs.setdefault('break_long_words', False)
    kwargs['tabsize'] = tabsize
    if width <= tabsize * indent_level:
        raise ValueError('Amount of indentation must be less than the maximum width.')
    kwargs['width'] = width - tabsize * indent_level

    lines = textwrap.wrap(text, **kwargs)
    output = [' ' * tabsize * indent_level + line for line in lines]
    if any(len(line) > width for line in output):
        raise ValueError('There cannot be any word (after indentation) that exceeds the maximum '
                         'width')
    return output
