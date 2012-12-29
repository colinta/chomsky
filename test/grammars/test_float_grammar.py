from pytest import raises
from chomsky import *


def test_float_repr():
    assert repr(Float('123.456')) == "Float('123.456')"


def test_float_type():
    assert isinstance(Float('1.0'), Float)


def test_float_grammar_0():
    m = Float('0.0')
    assert m.parsed == '0.0'
    assert str(m) == '0.0'


def test_float_grammar_01():
    m = Float('0.1')
    assert m.parsed == '0.1'
    assert str(m) == '0.1'


def test_float_grammar_10():
    m = Float('1.0')
    assert m.parsed == '1.0'
    assert str(m) == '1.0'


def test_float_grammar_00001():
    m = Float('0.00001')
    assert m.parsed == '0.00001'
    assert str(m) == '0.00001'


def test_float_grammar_00000():
    m = Float('0.00000')
    assert m.parsed == '0.00000'
    assert str(m) == '0.00000'


def test_float_operation():
    m = Float('2.0+1')
    assert m.parsed == '2.0'
    assert str(m) == '2.0'


def test_float_grammar_neg_1():
    m = Float('-1.0')
    assert m.parsed == '-1.0'
    assert str(m) == '-1.0'


def test_float_grammar_123456():
    m = Float('123.456')
    assert m.parsed == '123.456'
    assert str(m) == '123.456'


def test_float_grammar_neg_123456():
    m = Float('-123.456')
    assert m.parsed == '-123.456'
    assert str(m) == '-123.456'


def test_float_fail_neg_0():
    with raises(ParseException):
        print Float('-0')


def test_float_fail_a():
    with raises(ParseException):
        print Float('a')
