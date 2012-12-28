from pytest import raises
from chomsky import *


def test_hexadecimal_repr():
    assert repr(HexadecimalInteger('0x123')) == "HexadecimalInteger('0x123')"


def test_hexadecimal_type():
    assert isinstance(HexadecimalInteger('0x1'), HexadecimalInteger)


def test_hexadecimal_grammar_0x0():
    m = HexadecimalInteger('0x0')
    assert m.parsed == '0x0'
    assert str(m) == '0x0'


def test_hexadecimal_grammar_0X00():
    m = HexadecimalInteger('0X00')
    assert m.parsed == '0X00'
    assert str(m) == '0X00'


def test_hexadecimal_grammar_0x123abc():
    m = HexadecimalInteger('0x123abc')
    assert m.parsed == '0x123abc'
    assert str(m) == '0x123abc'


def test_hexadecimal_grammar_0x001234567890abcdefABCDEF():
    m = HexadecimalInteger('0x001234567890abcdefABCDEF')
    assert m.parsed == '0x001234567890abcdefABCDEF'
    assert str(m) == '0x001234567890abcdefABCDEF'


def test_hexadecimal_grammar_neg_0x001():
    m = HexadecimalInteger('-0x001')
    assert m.parsed == '-0x001'
    assert str(m) == '-0x001'


def test_hexadecimal_grammar_neg_0x001234567890abcdefABCDEF():
    m = HexadecimalInteger('-0x001234567890abcdefABCDEF')
    assert m.parsed == '-0x001234567890abcdefABCDEF'
    assert str(m) == '-0x001234567890abcdefABCDEF'


def test_hexadecimal_grammar_neg_0X00100():
    m = HexadecimalInteger('-0X00100')
    assert m.parsed == '-0X00100'
    assert str(m) == '-0X00100'


def test_hexadecimal_fail_neg_0x0():
    with raises(ParseException):
        print HexadecimalInteger('-0x0')


def test_hexadecimal_fail_neg_0x0000():
    with raises(ParseException):
        print HexadecimalInteger('-0x0000')


def test_hexadecimal_fail_a():
    with raises(ParseException):
        print HexadecimalInteger('a')
