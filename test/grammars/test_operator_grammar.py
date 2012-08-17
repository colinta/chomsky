# -*- encoding: utf-8 -*-
from pytest import raises
from chomsky import *


class UnicodeOperator(Grammar):
    __metaclass__ = OperatorGrammarType
    operators = list(u'÷')


def test_operator_repr():
    assert repr(Operator('-')) == "Operator('-')"


def test_unicodeoperator_repr():
    assert repr(UnicodeOperator(u'÷')) == u"UnicodeOperator(u'\\xf7')"


def test_operator_type():
    assert isinstance(Operator('-'), Operator)


def test_operator_grammar_minus():
    m = Operator('-')
    assert m.parsed == '-'
    assert str(m) == '-'


def test_operator_grammar_unicode():
    m = UnicodeOperator(u'÷')
    assert m.parsed == u'÷'
    assert unicode(m) == u'÷'


def test_operator_grammar_plus():
    m = Operator('+')
    assert m.parsed == '+'
    assert str(m) == '+'


def test_operator_grammar_equal():
    m = Operator('==')
    assert m.parsed == '=='
    assert str(m) == '=='


def test_operator_grammar_and():
    m = Operator('&&')
    assert m.parsed == '&&'
    assert str(m) == '&&'


def test_operator_grammar_binary_or():
    m = Operator('|')
    assert m.parsed == '|'
    assert str(m) == '|'


def test_operator_fail():
    with raises(ParseException):
        print Operator('a')
