"""Class for representing a description of objects/errors in the docstring."""
from docinstance.utils import wrap, wrap_indent_subsequent
from docinstance.content.base import DocContent
from docinstance.content.equation import DocEquation


class DocDescription(DocContent):
    """Description of objects or errors raised in a docstring.

    If a function is being described, then all of `name`, `signature`, and `descs` can be given. The
    `types` can also be given to show the types of the returned value. However, note that NumPy
    docstring format does not support this documentation format.
    If a variable is being described, then `name`, `type` and `descs` can be given. The `types`
    would correspond to the allowed types of the parameter.
    If an error is being described, then `name` and `descs` can be given.

    Attributes
    ----------
    name : str
        Name of the described object/error.
    signature : str
        Signature of the described object.
        Used to describe inputs to functions.
    types : list of classes/str
        Allowed types of the given object.
        If multiple classes are given, then the last one is assumed to be the default value.
        Used to describe types of a parameter and of the value returned by a method.
    descs : list of {str, DocEquation}
        Descriptions of the given object.
        If multiple descriptions are given, then each string in the list/tuple provides a
        paragraph.

    Methods
    -------
    __init__(self, name, signature='', types='', descs='')
        Initialize.
    make_docstring(self, style, width, indent_level, tabsize)
        Return docstring in correponding style.
    make_numpy_docstring(self, width, indent_level, tabsize)
        Return the docstring in numpy style.
    make_numpy_docstring_signature(self, width, indent_level, tabsize)
        Return the docstring in numpy style modified to include signature.

    """
    def __init__(self, name, signature='', types=None, descs=None):
        """Initialize the object.

        Parameters
        ----------
        name : str
            Name of the described object/error.
        signture : {str, ''}
            Signature of the described object.
            Default is no signature (i.e. empty string).
        types : {class, list/tuple of classes, str, list/tuple of str, None}
            Allowed types of the given object.
            If multiple classes are given, then the last one is assumed to be the default value.
            Default is no types.
        descs : {str, list/tuple of str/DocEquation, None}
            Descriptions of the given object.
            If multiple descriptions are given, then each string in the list/tuple provides a
            paragraph.
            Default is no descriptions.

        Raises
        ------
        TypeError
            If the name of the described object/error is not a string.
            If the signature of the described object/error is not a string.
            If the allowed types of the described object/error is not a class or a list/tuple of
            classes/strings.
            If the descriptions of the described object/error is not a string or a list/tuple of
            strings.

        """
        if not isinstance(name, str):
            raise TypeError("Name of the described object/error must be a string.")
        self.name = name

        if not isinstance(signature, str):
            raise TypeError("Signature of the given object must be a string.")
        self.signature = signature

        if types is None:
            types = []
        elif isinstance(types, (type, str)):
            types = [types]
        elif not (isinstance(types, (list, tuple)) and
                  all(isinstance(i, (type, str)) for i in types)):
            raise TypeError("Types of allowed objects must be given as a class or list/tuple of "
                            "classes/strings.")
        self.types = list(types)

        if descs is None:
            descs = []
        elif isinstance(descs, (str, DocEquation)):
            descs = [descs]
        elif not (isinstance(descs, (list, tuple)) and
                  all(isinstance(i, (str, DocEquation)) for i in descs)):
            raise TypeError("Descriptions of the object/error must be given as a string or "
                            "list/tuple of strings")
        self.descs = list(descs)

    @property
    def types_str(self):
        """Return types as strings.

        Returns
        -------
        types_str : list of str
            Types where the classes are converted to its __name__ attribute.

        """
        return [i.__name__ if isinstance(i, type) else i for i in self.types]

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
        descripton_docstring : str
            Docstring of the given descriptions of the object/error in numpy style.

        Raises
        ------
        ValueError
            If the name and the type of variable cannot fit into the given width and indentation.
            If the name and the first type of the variable cannot fit into the given width and
            indentation.

        Notes
        -----
        The signature of a function is not included in the numpy docstring.

        """
        if self.signature != '':
            print('Warning: In NumPy docstring format, the signature of a function is not '
                  'included.')

        output = ''
        # var_name
        # OR
        # error_name
        if not self.types:
            # NOTE: error is raised by wrap if the name is too long to fit in the given width and
            #       indentation
            output += wrap(self.name, width=width, indent_level=indent_level, tabsize=tabsize)[0]
        # var_name : var_type
        elif len(self.types) == 1:
            name_type = wrap('{0} : {1}'.format(self.name, self.types_str[0]),
                             width=width, indent_level=indent_level, tabsize=tabsize)
            # check that the both the name and the type can fit in the given width and indentation
            if len(name_type) > 1:
                # FIXME: need a better message
                raise ValueError('The name and the type of the variable are too long to fit into '
                                 'given width and indentation.')
            output += name_type[0]
        # var_name : {var_type1, var_type2, default_type}
        else:
            name_types = wrap('{0} : {{{1}}}'.format(self.name, ', '.join(self.types_str)),
                              width=width, indent_level=indent_level, tabsize=tabsize)
            # if there are too many types to fit into one line, the remaining lines should be
            # indented to line up after "var_name : {"
            wrap_point = len('{0} : {{'.format(self.name))
            # check that the name and first type can fit into the first line
            if not name_types[0].startswith('{0}{1} : {{{2}'.format(' ' * indent_level * tabsize,
                                                                    self.name, self.types_str[0])):
                # FIXME: need a better message
                raise ValueError('The name and the first type of the variable are too long to fit '
                                 'into the given width and indentation.')
            # wrap the remaining lines
            name_types_lines = [name_types[0]]
            for line in name_types[1:]:
                name_types_lines += wrap(line, width=width, indent_level=1, tabsize=wrap_point)
            output += '\n'.join(name_types_lines)
        output += '\n'

        # descriptions
        for paragraph in self.descs:
            output += '\n'.join(wrap(paragraph,
                                     width=width, indent_level=indent_level+1, tabsize=tabsize))
            output += '\n'

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
        descripton_docstring : str
            Docstring of the given descriptions of the object/error in numpy style that includes the
            signature.

        """
        new_name = '{0}{1}'.format(self.name, self.signature)
        new_description = self.__class__(new_name, '', self.types, self.descs)
        return new_description.make_numpy_docstring(width, indent_level, tabsize)

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

        Notes
        -----
        The signature of a function is not included in the google docstring.

        """
        output = ''
        first_block = []
        # var_name:
        if not self.types:
            first_block = wrap('{0}:'.format(self.name),
                               width=width, indent_level=indent_level, tabsize=tabsize)
        # var_name (type1, type2):
        else:
            # FIXME: optional parameters need to be specified within google doc
            types_str = [i if isinstance(i, str) else ':obj:`{0}`'.format(j)
                         for i, j in zip(self.types, self.types_str)]
            text = '{0} ({1}):'.format(self.name, ', '.join(types_str))
            # if there are too many types to fit into one line, the remaining lines should be
            # indented to line up after "var_name ("
            # FIXME: following can probably be replaced with a better wrapping function
            first_block = [' ' * indent_level * tabsize + line for line in
                           wrap_indent_subsequent(text, width=width - indent_level*tabsize,
                                                  indent_level=1,
                                                  tabsize=len('{0} ('.format(self.name)))]
        # add descriptions
        if self.descs:
            output += '\n'.join(first_block[:-1])
            if len(first_block) != 1:
                output += '\n'
            # FIXME: following can probably be replaced with a better wrapping function
            first_desc = wrap_indent_subsequent(first_block[-1] + ' ' + self.descs[0], width=width,
                                                indent_level=indent_level+1, tabsize=tabsize)
            output += '\n'.join(first_desc)
            output += '\n'
            for desc in self.descs[1:]:
                output += '\n'.join(wrap(desc, width=width, indent_level=indent_level+1,
                                         tabsize=tabsize))
                output += '\n'
        else:
            output += '\n'.join(first_block)
            output += '\n'
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

        Raises
        ------
        ValueError
            If the parameter name is too long to fit within the given width and indent.

        """
        output = ''
        if self.descs:
            text = ':param {0}: {1}'.format(self.name, self.descs[0])
            # FIXME: following can probably be replaced with a better wrapping function
            block = [' ' * indent_level * tabsize + line for line in
                     wrap_indent_subsequent(text, width=width - indent_level*tabsize,
                                            indent_level=1, tabsize=tabsize)]
            output += '\n'.join(block)
            output += '\n'
            if len(self.descs) > 1:
                for desc in self.descs[1:]:
                    output += '\n'.join(wrap(desc, width=width, indent_level=indent_level+1,
                                             tabsize=tabsize))
                    output += '\n'
        else:
            block = wrap(':param {0}:'.format(self.name), width=width, indent_level=indent_level,
                         tabsize=tabsize)
            if len(block) > 1:
                raise ValueError('Parameter name is too long to fit within the given line width and'
                                 ' indent level.')
            output += block[0]
            output += '\n'

        types_str = [i if isinstance(i, str) else ':obj:`{0}`'.format(j)
                     for i, j in zip(self.types, self.types_str)]
        if self.types:
            text = ':type {0}: {1}'.format(self.name, ', '.join(types_str))
            block = [' ' * indent_level * tabsize + line for line in
                     wrap_indent_subsequent(text, width=width - indent_level*tabsize,
                                            indent_level=1, tabsize=tabsize)]
            output += '\n'.join(block)
            output += '\n'
        return output
