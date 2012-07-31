from pytest import raises
from chomsky import *


nmatcher = NMatches(Literal('one'), min=1, max=2)


def test_nmatcher_repr():
    assert repr(NMatches(Literal('one'), min=1, max=2)) == "NMatches(Literal('one'), min=1, max=2)"
    assert repr(NMatches(Literal('one'), min=1, max=2, suppress=False)) == "NMatches(Literal('one'), min=1, max=2)"
    assert repr(NMatches(Literal('one'), min=1, max=2, suppress=True)) == "NMatches(Literal('one'), min=1, max=2, suppress=True)"


def test_nmatcher_lenghs():
    assert nmatcher.minimum_length() == 3
    assert nmatcher.maximum_length() == 6


def test_one_nmatcher():
    parsed = nmatcher('one')
    assert parsed == ['one']


def test_zero_nmatcher():
    parsed = nmatcher('one')
    assert parsed == ['one']


def test_two_nmatcher():
    parsed = nmatcher('oneone')
    assert parsed == ['one', 'one']


def test_two2_nmatcher():
    parsed = nmatcher('onetwo')
    assert parsed == ['one']


n_with_words_matcher = Literal('pre-') + NMatches(Literal('uno'), min=1, max=2) + Literal('-post')


def test_one_nmatcher_with_words():
    parsed = n_with_words_matcher('pre-uno-post')
    assert parsed == ['pre-', ['uno'], '-post']


def test_one2_nmatcher_with_words():
    parsed = n_with_words_matcher('pre-unouno-post')
    assert parsed == ['pre-', ['uno', 'uno'], '-post']


def test_two_nmatcher_with_words():
    with raises(ParseException):
        print n_with_words_matcher('pre-unounounouno-post')
