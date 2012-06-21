from chomsky import *


optional_matcher = Optional(Literal('optional'))


def test_one_optional():
    parsed = optional_matcher('optional')
    assert isinstance(parsed, ResultList)
    assert parsed == ['optional']


def test_empty_optional():
    parsed = optional_matcher('bahhumbug')
    assert isinstance(parsed, ResultList)
    assert parsed == []
