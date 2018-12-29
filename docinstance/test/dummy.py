"""This will be replaced."""
from docinstance.docstring import Docstring
from docinstance.content.section import DocSection
from docinstance.content.description import DocDescription


_docinstance = Docstring([
    'Dummy module for testing docinstance.wrapper.docstring_modify_import.'
])


class DummyClass:
    """This too will be replaced."""
    _docinstance = Docstring([
        'Class for testing.',
        DocSection('attributes', DocDescription('x', types=str, descs='Example.'))
    ])
