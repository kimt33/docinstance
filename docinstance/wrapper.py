"""Functions for wrapping a python object to utilize the docinstance object."""
import inspect
import os
from functools import wraps
import importlib
from docinstance.utils import extract_members


def kwarg_wrapper(wrapper):
    """Wrap the keyword arguments into the wrapper.

    The wrapper behaves differently when used as a decorator if the arguments are given. i.e.
    @decorator vs @decorator(). Therefore, the default keyword values of the wrapper must be changed
    (with another wrapper).

    """
    @wraps(wrapper)
    def new_wrapper(obj=None, **kwargs):
        """Reconstruction of the provided wrapper so that keyword arguments are rewritten.

        When a wrapper is used as a decorator and is not called (i.e. no parenthesis), then the
        wrapee (wrapped object) is automatically passed into the decorator. This function changes
        the "default" keyword arguments so that the decorator is not called (so that the wrapped
        object is automatically passed in). If the decorator is called, e.g. `x = decorator(x)`,
        then it simply needs to return the wrapped value.

        """
        if obj is None and kwargs:
            # Since no object is provided, we need to turn the wrapper back into a form so that it
            # will automatically pass in the object (i.e. turn it into a function) after overwriting
            # the keyword arguments
            return lambda orig_obj: wrapper(orig_obj, **kwargs)
        # Here, the object is provided OR keyword argument is not provided.
        # If the object is provided, then the wrapper can be executed.
        # If the object is not provided and keyword argument is not provided, then an error will
        # be raised.
        return wrapper(obj, **kwargs)

    return new_wrapper


# FIXME: change name
# FIXME: doesn't work on standalone functions because we cannot assign attributes of a function
# within the definition of a function
@kwarg_wrapper
def docstring(obj, width=100, indent_level=0, tabsize=4):
    """Wrap given object such that _docinstance is used to overwrite __docstring__.

    Parameters
    ----------
    obj : function, module, class
        Object that contains a docstring.
    width : {int, 100}
        Maximum number of characters allowed in each line.
        Default is 100.
    indent_level : {int, 0}
        Number of indents (tabs) that the docstring uses.
        Default is 0.
    tabsize : {int, 4}
        Number of spaces that corresponds to one tab.
        Default is 4.

    Raises
    ------
    TypeError
        If the obj's __doc__ is neither str nor Docstring instance.

    """
    # TODO: if there is a parser, parse the docstring into docinstance
    if not hasattr(obj, '_docinstance'):
        return obj
    # generate new docstring from docinstance
    # pylint: disable=W0212
    docinst = obj._docinstance
    new_doc = docinst.make_docstring(width=width, indent_level=indent_level, tabsize=tabsize)
    # TODO: following can be used to check that the parsed docstring matches with the original
    # # compare to original if original exists
    # if obj.__doc__ is not None:
    #     diff = list(difflib.context_diff(obj.__doc__.strip().split('\n'),
    #                                      new_doc.strip().split('\n'),
    #                                      fromfile='original-docstring',
    #                                      tofile='generated-docstring'))
    #     if len(diff) != 0:
    #         print('WARNING: docstring generated from _docinstance is different from the
    #               original.')
    #         print('\n'.join(diff))
    # overwrite docstring
    obj.__doc__ = new_doc

    return obj


@kwarg_wrapper
def docstring_recursive(obj, width=100, indent_level=0, tabsize=4):
    """Wrap given object and its attributes such that __docstring__ is overwritten.

    This wrapper recursively converts every member of the object (and their members) if their
    source code is located in the same file.

    Parameters
    ----------
    obj : function, module, class, property
        Object that contains a docstring.
    width : {int, 100}
        Maximum number of characters allowed in each width.
    indent_level : {int, 0}
        Number of indents (tabs) that are needed for the docstring.
    tabsize : {int, 4}
        Number of spaces that corresponds to a tab.

    Returns
    -------
    obj
        Wrapped object where the docstring is in the selected format and the corresponding Docstring
        instance is stored in `_docstring`.

    Notes
    -----
    A package and its contents can be wrapped using this decorator, but the contents of the package
    must be accessible through the __init__.py of the package. This would mean that the __init__.py
    would need to explicitly import the desired modules. In fact, all of the __init__.py (for each
    directory in the package) will need to import the modules that contains contents to be wrapped.

    """
    # wrap self
    obj = docstring(obj, width=width, indent_level=indent_level, tabsize=tabsize)
    # wrap members
    for member in extract_members(obj).values():
        # recurse for all members of member
        docstring_recursive(member, width=width, indent_level=indent_level+1, tabsize=tabsize)

    return obj


def docstring_current_module(width=100, tabsize=4):
    """Wrap the docstrings of all objects defined within the current module.

    Call this function within the module whose objects will be wrapped.

    Parameters
    ----------
    width : {int, 100}
        Maximum number of characters allowed in each line.
        Default is 100.
    tabsize : {int, 4}
        Number of spaces that corresponds to one tab.
        Default is 4.

    Notes
    -----
    Must be called within the module that is to be wrapped. Otherwise, the objects in the wrong
    module/frame will be wrapped.

    """
    # get the module that called this function
    module = next(inspect.getmodule(i[0]) for i in inspect.stack()[1:]  # pragma: no branch
                  if inspect.getmodule(i[0]) is not None)
    # recursively convert
    # NOTE: docstring for the module will always not be indented
    docstring_recursive(module, width=width, indent_level=0, tabsize=tabsize)


# TODO: make this function work for built in packages as well?
# FIXME: doesn't work if the module has already been imported. If so, then the module needs to be
# reloaded (importlib.reload(module))
def docstring_modify_import(width=100, tabsize=4):
    """Modify import behaviour to wrap the docstrings of related objects after the import.

    This function should be placed in the __init__.py of the package to ensure that the import
    behaviour is different only for the given package. It is assumed that the package is organized
    by directories where the __init__.py of the package is the parent directory in which all of the
    modules are located. For example, it is assumed that there are no soft-links to directories
    outside of this package.

    Parameters
    ----------
    width : {int, 100}
        Maximum number of characters allowed in each line.
        Default is 100.
    tabsize : {int, 4}
        Number of spaces that corresponds to one tab.
        Default is 4.

    Notes
    -----
    This function modifies some pretty low level code, so it should be used with caution.

    Since the modified loader is the SourceFileLoader, this function does not affect the import of
    built-in packages.

    """
    # find the location from which this function is called
    parentfile = next(inspect.getsourcefile(i[0]) for i in inspect.stack()[1:]  # pragma: no branch
                      if inspect.getmodule(i[0]) is not None)
    parentdir = os.path.dirname(parentfile)

    def pandora_box(old_import):
        """Change the import behaviour.

        Parameters
        ----------
        old_import : importlib._bootstrap_external.SourceFileLoader.exec_module
            Function that is executed when a module is imported.
            This decorator is intended for the SourceFileLoader.exec_module and using it on other
            functions may result in weird behaviour.

        Returns
        -------
        new_import : function
            Function that has been modified to wrap the docstrings of the objects of the module by
            recursively scanning the __dict__.

        """
        if not hasattr(old_import, 'special_cases'):
            old_import.special_cases = set()
        old_import.special_cases.add(parentdir)

        def new_import(*args, **kwargs):
            """Import and then overwrite __doc__ using _docinstance."""
            old_import(*args, **kwargs)

            # NOTE: the arguments to the function
            # importlib._bootstrap_external.SourceFileLoader.exec_module is the SourceFileLoader
            # instance (i.e. self) and the module that is executed. We are assuming here that this
            # decorator will be applied only to `exc_module`.
            module = args[1]
            sourcefile = inspect.getsourcefile(module)
            if any(os.path.commonpath([sourcefile, parent]) == parent
                   for parent in old_import.special_cases):
                docstring_recursive(module, width=width, indent_level=0, tabsize=tabsize)

        new_import.special_cases = old_import.special_cases

        return new_import

    # open the box
    # pylint: disable=W0212
    importlib._bootstrap_external.SourceFileLoader.exec_module = pandora_box(
        # pylint: disable=W0212
        importlib._bootstrap_external.SourceFileLoader.exec_module
    )
