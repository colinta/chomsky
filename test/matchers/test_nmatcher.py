from pytest import raises
from chomsky import *


nmatcher = NMatches(Literal('one'), min=1, max=2)


def test_nmatcher_repr():
    assert repr(NMatches(Literal('one'), min=1, max=2, suppress=False)) == "NMatches(Literal('one'), min=1, max=2)"
    assert repr(NMatches(Literal('one'), min=1, max=2, suppress=True)) == "NMatches(Literal('one'), min=1, max=2, suppress=True)"


def test_one_nmatcher():
    parsed = nmatcher('one')
    assert isinstance(parsed, ResultList)
    assert parsed == ['one']


def test_zero_nmatcher():
    parsed = nmatcher('one')
    assert isinstance(parsed, ResultList)
    assert parsed == ['one']


def test_two_nmatcher():
    parsed = nmatcher('oneone')
    assert isinstance(parsed, ResultList)
    assert parsed == ['one', 'one']


def test_two2_nmatcher():
    parsed = nmatcher('onetwo')
    assert isinstance(parsed, ResultList)
    assert parsed == ['one']


n_with_words_matcher = Literal('pre-') + NMatches(Literal('uno'), min=1, max=2) + Literal('-post')


def test_one_nmatcher_with_words():
    parsed = n_with_words_matcher('pre-uno-post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == ['uno']


def test_one2_nmatcher_with_words():
    parsed = n_with_words_matcher('pre-unouno-post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == ['uno', 'uno']


def test_two_nmatcher_with_words():
    with raises(ParseException):
        n_with_words_matcher('pre-unounounouno-post')
