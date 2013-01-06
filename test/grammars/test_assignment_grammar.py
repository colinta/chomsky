# -*- encoding: utf-8 -*-
from pytest import raises
from chomsky import *


def test_operator_repr():
    assert repr(Assignment('=')) == "Assignment('=')"


def test_operator_type():
    assert isinstance(Assignment('='), Assignment)


def test_operator_grammar_assign():
    m = Assignment('=')
    assert m.parsed == '='
    assert str(m) == '='


def test_operator_grammar_plus_assign():
    m = Assignment('+=')
    assert m.parsed == '+='
    assert str(m) == '+='


def test_operator_fail():
    with raises(ParseException):
        print Assignment('+')
