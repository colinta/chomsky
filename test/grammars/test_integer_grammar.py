from pytest import raises
from chomsky import *


def test_integer_repr():
    assert repr(Integer('123')) == "Integer('123')"


def test_integer_type():
    assert isinstance(Integer('1'), Integer)


def test_integer_grammar_0():
    m = Integer('0')
    assert m.parsed == '0'
    assert str(m) == '0'


def test_integer_grammar_1():
    m = Integer('1')
    assert m.parsed == '1'
    assert str(m) == '1'


def test_integer_operation():
    m = Integer('1+1')
    assert m.parsed == '1'
    assert str(m) == '1'


def test_integer_grammar_neg_1():
    m = Integer('-1')
    assert m.parsed == '-1'
    assert str(m) == '-1'


def test_integer_grammar_123():
    m = Integer('123')
    assert m.parsed == '123'
    assert str(m) == '123'


def test_integer_grammar_neg_123():
    m = Integer('-123')
    assert m.parsed == '-123'
    assert str(m) == '-123'


def test_integer_fail_neg_0():
    with raises(ParseException):
        Integer('-0')


def test_integer_fail_a():
    with raises(ParseException):
        Integer('a')
