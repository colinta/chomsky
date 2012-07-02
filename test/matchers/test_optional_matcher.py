from chomsky import *


optional_matcher = Optional(Literal('optional'))


def test_optional_repr():
    assert repr(Optional(Literal('optional'))) == "Optional(Literal('optional'))"
    assert repr(Optional(Literal('optional'), suppress=False)) == "Optional(Literal('optional'))"
    assert repr(Optional(Literal('optional'), suppress=True)) == "Optional(Literal('optional'), suppress=True)"


def test_one_optional():
    parsed = optional_matcher('optional')
    assert isinstance(parsed, ResultList)
    assert parsed == ['optional']


def test_empty_optional():
    parsed = optional_matcher('bahhumbug')
    assert isinstance(parsed, ResultList)
    assert parsed == []
