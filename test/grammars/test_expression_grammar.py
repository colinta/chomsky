from pytest import raises
from chomsky import *


def test_expression_repr():
    assert repr(Expression('0+1')) == "Expression('0+1')"


def test_expression_grammar():
    assert Expression('0+1').parsed == [Integer('0'), Operator('+'), Integer('1')]
