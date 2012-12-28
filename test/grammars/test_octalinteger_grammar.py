from pytest import raises
from chomsky import *


def test_octal_repr():
    assert repr(OctalInteger('0123')) == "OctalInteger('0123')"


def test_octal_type():
    assert isinstance(OctalInteger('01'), OctalInteger)


def test_octal_grammar_00():
    m = OctalInteger('00')
    assert m.parsed == '00'
    assert str(m) == '00'


def test_octal_grammar_0o0():
    m = OctalInteger('0o0')
    assert m.parsed == '0o0'
    assert str(m) == '0o0'


def test_octal_grammar_0O00():
    m = OctalInteger('0O00')
    assert m.parsed == '0O00'
    assert str(m) == '0O00'


def test_octal_grammar_01234567():
    m = OctalInteger('01234567')
    assert m.parsed == '01234567'
    assert str(m) == '01234567'


def test_octal_grammar_0o1234567():
    m = OctalInteger('0o1234567')
    assert m.parsed == '0o1234567'
    assert str(m) == '0o1234567'


def test_octal_grammar_0O1234567():
    m = OctalInteger('0O1234567')
    assert m.parsed == '0O1234567'
    assert str(m) == '0O1234567'


def test_octal_grammar_0001234567():
    m = OctalInteger('0001234567')
    assert m.parsed == '0001234567'
    assert str(m) == '0001234567'


def test_octal_grammar_neg_0001():
    m = OctalInteger('-0001')
    assert m.parsed == '-0001'
    assert str(m) == '-0001'


def test_octal_grammar_neg_0001234567():
    m = OctalInteger('-0001234567')
    assert m.parsed == '-0001234567'
    assert str(m) == '-0001234567'


def test_octal_grammar_neg_0O00100():
    m = OctalInteger('-0O00100')
    assert m.parsed == '-0O00100'
    assert str(m) == '-0O00100'


def test_octal_fail_neg_00():
    with raises(ParseException):
        print OctalInteger('-00')


def test_octal_fail_neg_00000():
    with raises(ParseException):
        print OctalInteger('-00000')


def test_octal_fail_a():
    with raises(ParseException):
        print OctalInteger('a')
