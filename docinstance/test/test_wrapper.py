from nose.tools import assert_raises
from docinstance.wrapper import kwarg_wrapper, docstring, docstring_recursive
from docinstance.docstring import Docstring
from docinstance.section import DocSection
from docinstance.description import DocDescription


def test_kwarg_wrapper():
    """Test docinstance.wrapper.kwarg_wrapper."""
    @kwarg_wrapper
    def test(func, x=1):
        func.x = x
        return func

    def f():
        pass
    assert_raises(AttributeError, lambda: f.x)
    g = test(f)
    assert g.x == 1
    g = test(f, x=2)
    assert g.x == 2

    @test
    def f():
        pass
    assert f.x == 1

    @test(x=2)
    def f():
        pass
    assert f.x == 2


def test_wrapper_docstring_on_func():
    """Test docinstance.wrapper.docstring on a function."""
    # no _docinstance
    @docstring
    def test():
        """Test docstring.

        Parameters
        ----------
        x : int
            Something.

        """
        pass

    # NOTE: the indentation can be removed with inspect.cleandoc
    assert test.__doc__ == ('Test docstring.\n'
                            '\n'
                            '        Parameters\n'
                            '        ----------\n'
                            '        x : int\n'
                            '            Something.\n\n'
                            '        ')
    assert not hasattr(test, '_docinstance')

    # _docinstance
    docinstance = Docstring([
        'Test docstring.',
        DocSection('parameters',
                   DocDescription('x', types=int, descs='Something.'))
    ])

    def test():
        pass

    # FIXME: this is terrible because contents inside function is ignored when declaring a function
    # i.e. we cannot set the attribute of a function within a function definition. Docstrings are
    # special so they are not ignored. Using docstring that get parsed seems to be only option for
    # standalone functions
    test._docinstance = docinstance
    docstring(test)

    assert test.__doc__ == ('Test docstring.\n'
                            '\n'
                            'Parameters\n'
                            '----------\n'
                            'x : int\n'
                            '    Something.\n\n')
    assert test._docinstance == docinstance

    docstring(test, indent_level=2)
    assert test.__doc__ == ('Test docstring.\n'
                            '\n'
                            '        Parameters\n'
                            '        ----------\n'
                            '        x : int\n'
                            '            Something.\n\n'
                            '        ')
    assert test._docinstance == docinstance


def test_wrapper_docstring_on_class():
    """Test docinstance.wrapper.docstring on a class."""
    # no _docinstance
    @docstring
    class Test:
        """Test docstring.

        Attributes
        ----------
        x : int
            Something.

        """
        def f(self):
            """Test function.

            Returns
            -------
            nothing

            """
            pass

    assert Test.__doc__ == ('Test docstring.\n\n'
                            '        Attributes\n'
                            '        ----------\n'
                            '        x : int\n'
                            '            Something.\n\n'
                            '        ')
    assert not hasattr(Test, '_docinstance')

    # docinstance
    docinstance1 = Docstring([
        'Test docstring.',
        DocSection('attributes',
                   DocDescription('x', types=int, descs='Something.'))
    ])
    docinstance2 = Docstring([
        'Test function.',
        DocSection('returns', 'nothing')
    ])

    # w/o indentation
    @docstring
    class Test:
        _docinstance = docinstance1

        def f(self):
            pass
        f._docinstance = docinstance2

    assert Test.__doc__ == ('Test docstring.\n\n'
                            'Attributes\n'
                            '----------\n'
                            'x : int\n'
                            '    Something.\n\n')
    assert Test._docinstance == docinstance1
    assert Test.f.__doc__ is None
    assert Test.f._docinstance == docinstance2

    # w/ indentation
    @docstring(indent_level=1)
    class Test:
        _docinstance = docinstance1

        def f(self):
            pass
        f._docinstance = docinstance2

    assert Test.__doc__ == ('Test docstring.\n\n'
                            '    Attributes\n'
                            '    ----------\n'
                            '    x : int\n'
                            '        Something.\n\n'
                            '    ')


def test_wrapper_docstring_recursive_on_class():
    """Test docinstance.wrapper.docstring_recursive on a class."""
    # no _docinstance
    @docstring_recursive
    class Test:
        """Test docstring.

        Attributes
        ----------
        x : int
            Something.

        """
        def f(self):
            """Test function.

            Returns
            -------
            nothing

            """
            pass

    assert Test.__doc__ == ('Test docstring.\n\n'
                            '        Attributes\n'
                            '        ----------\n'
                            '        x : int\n'
                            '            Something.\n\n'
                            '        ')
    assert not hasattr(Test, '_docinstance')
    assert Test.f.__doc__ == ('Test function.\n\n'
                              '            Returns\n'
                              '            -------\n'
                              '            nothing\n\n'
                              '            ')
    assert not hasattr(Test.f, '_docinstance')

    # docinstance
    docinstance1 = Docstring([
        'Test docstring.',
        DocSection('attributes',
                   DocDescription('x', types=int, descs='Something.'))
    ])
    docinstance2 = Docstring([
        'Test function.',
        DocSection('returns', 'nothing')
    ])

    # w/o indentation
    @docstring_recursive
    class Test:
        _docinstance = docinstance1

        def f(self):
            pass
        f._docinstance = docinstance2

    assert Test.__doc__ == ('Test docstring.\n\n'
                            'Attributes\n'
                            '----------\n'
                            'x : int\n'
                            '    Something.\n\n')
    assert Test._docinstance == docinstance1
    assert Test.f.__doc__ == ('Test function.\n\n'
                              '    Returns\n'
                              '    -------\n'
                              '    nothing\n\n'
                              '    ')
    assert Test.f._docinstance == docinstance2

    # w indentation
    @docstring_recursive(indent_level=2)
    class Test:
        _docinstance = docinstance1

        def f(self):
            pass
        f._docinstance = docinstance2

    assert Test.__doc__ == ('Test docstring.\n\n'
                            '        Attributes\n'
                            '        ----------\n'
                            '        x : int\n'
                            '            Something.\n\n'
                            '        ')
    assert Test._docinstance == docinstance1
    assert Test.f.__doc__ == ('Test function.\n\n'
                              '            Returns\n'
                              '            -------\n'
                              '            nothing\n\n'
                              '            ')
    assert Test.f._docinstance == docinstance2
