from pytest import raises
from chomsky import *


one_matcher = OneOrMore(Literal('one'))


def test_oneormore_repr():
    assert repr(OneOrMore(Literal('one'), suppress=False)) == "OneOrMore(Literal('one'))"
    assert repr(OneOrMore(Literal('one'), suppress=True)) == "OneOrMore(Literal('one'), suppress=True)"


def test_one_oneormore():
    parsed = one_matcher('one')
    assert isinstance(parsed, ResultList)
    assert parsed == ['one']


def test_zero_oneormore():
    with raises(ParseException):
        one_matcher('two')


def test_two_oneormore():
    parsed = one_matcher('oneone')
    assert isinstance(parsed, ResultList)
    assert parsed == ['one', 'one']


def test_two2_oneormore():
    parsed = one_matcher('onetwo')
    assert isinstance(parsed, ResultList)
    assert parsed == ['one']


one_with_words_matcher = Literal('pre-') + OneOrMore(Literal('uno')) + Literal('-post')


def test_one_oneormore_with_words():
    parsed = one_with_words_matcher('pre-uno-post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == ['uno']


def test_one2_oneormore_with_words():
    parsed = one_with_words_matcher('pre-unouno-post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == ['uno', 'uno']


def test_two_oneormore_with_words():
    parsed = one_with_words_matcher('pre-unounounouno-post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == ['uno', 'uno', 'uno', 'uno']
