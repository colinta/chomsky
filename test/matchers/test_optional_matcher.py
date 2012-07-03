from chomsky import *


optional_matcher = Optional(Literal('optional'))


def test_optional_repr():
    assert repr(Optional(Literal('optional'))) == "Optional(Literal('optional'))"
    assert repr(Optional(Literal('optional'), suppress=False)) == "Optional(Literal('optional'))"
    assert repr(Optional(Literal('optional'), suppress=True)) == "Optional(Literal('optional'), suppress=True)"


def test_optional_lengths():
    assert optional_matcher.minimum_length() == 0
    assert optional_matcher.maximum_length() == 8


def test_one_optional():
    parsed = optional_matcher('optional')
    assert parsed == ['optional']


def test_empty_optional():
    parsed = optional_matcher('bahhumbug')
    assert parsed == []
