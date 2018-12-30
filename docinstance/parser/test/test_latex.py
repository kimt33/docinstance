"""Tests for docinstance.parser.latex."""
from docinstance.parser.latex import is_math, parse_equation
from docinstance.content.equation import DocEquation


def test_is_math():
    """Test docinstance.parser.numpy.is_math."""
    assert is_math('.. math::\n\n    x&=2\\\\\n    &=3')
    assert is_math('.. math::\n\n    x&=2\\\\\n    &=3\n')
    assert is_math('\n.. math::\n\n    x&=2\\\\\n    &=3\n\n\n')
    assert not is_math('x\n.. math::\n\n    x&=2\\\\\n    &=3\n\n\n')
    assert is_math('.. math::\n\n    x=2')
    assert is_math('  .. math::\n\n    x=2')
    assert is_math('\n       .. math::\n\n    x=2')


def test_parse_equation():
    """Test docinstance.parser.numpy.parse_equation."""
    test = parse_equation('.. math::\n\n    x &= 2\\\\\n    &= 3\n')
    assert len(test) == 1
    assert isinstance(test[0], DocEquation)
    assert test[0].equations == ['x &= 2\\\\', '&= 3']

    test = parse_equation('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n')
    assert len(test) == 2
    assert test[0] == 'x'
    assert isinstance(test[1], DocEquation)
    assert test[1].equations == ['x &= 2\\\\', '&= 3']

    test = parse_equation('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n\n\n')
    assert len(test) == 2
    assert test[0] == 'x'
    assert isinstance(test[1], DocEquation)
    assert test[1].equations == ['x &= 2\\\\', '&= 3']

    test = parse_equation('x\n.. math::\n\n    x &= 2\\\\\n    &= 3\n\ny')
    assert len(test) == 3
    assert test[0] == 'x'
    assert isinstance(test[1], DocEquation)
    assert test[1].equations == ['x &= 2\\\\', '&= 3']
    assert test[2] == 'y'
