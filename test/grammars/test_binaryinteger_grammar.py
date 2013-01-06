from pytest import raises
from chomsky import *


def test_binary_repr():
    assert repr(BinaryInteger('0b001')) == "BinaryInteger('0b001')"


def test_binary_type():
    assert isinstance(BinaryInteger('0b001'), BinaryInteger)


def test_binary_grammar_0b0():
    m = BinaryInteger('0b0')
    assert m.parsed == '0b0'
    assert str(m) == '0b0'


def test_binary_grammar_0B1():
    m = BinaryInteger('0B1')
    assert m.parsed == '0B1'
    assert str(m) == '0B1'


def test_binary_grammar_0b00010():
    m = BinaryInteger('0b00010')
    assert m.parsed == '0b00010'
    assert str(m) == '0b00010'


def test_binary_grammar_neg_1():
    m = BinaryInteger('-0b1')
    assert m.parsed == '-0b1'
    assert str(m) == '-0b1'


def test_binary_grammar_neg_1110():
    m = BinaryInteger('-0b1110')
    assert m.parsed == '-0b1110'
    assert str(m) == '-0b1110'


def test_binary_grammar_neg_0B0010():
    m = BinaryInteger('-0B0010')
    assert m.parsed == '-0B0010'
    assert str(m) == '-0B0010'


def test_binary_fail_neg_0():
    with raises(ParseException):
        BinaryInteger('-0b000')


def test_binary_fail_01():
    with raises(ParseException):
        BinaryInteger('a')
