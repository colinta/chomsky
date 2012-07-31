from pytest import raises
from chomsky import *


one_matcher = OneOrMore(Literal('one'))


def test_oneormore_repr():
    assert repr(OneOrMore(Literal('one'), suppress=False)) == "OneOrMore(Literal('one'))"
    assert repr(OneOrMore(Literal('one'), suppress=True)) == "OneOrMore(Literal('one'), suppress=True)"


def test_oneormore_lengths():
    assert one_matcher.minimum_length() == 3
    assert one_matcher.maximum_length() == Infinity


def test_one_oneormore():
    parsed = one_matcher('one')
    assert parsed == ['one']


def test_zero_oneormore():
    with raises(ParseException):
        print one_matcher('two')


def test_two_oneormore():
    parsed = one_matcher('oneone')
    assert parsed == ['one', 'one']


def test_two2_oneormore():
    parsed = one_matcher('onetwo')
    assert parsed == ['one']


one_with_words_matcher = Literal('pre-') + OneOrMore(Literal('uno')) + Literal('-post')


def test_one_oneormore_with_words():
    parsed = one_with_words_matcher('pre-uno-post')
    assert parsed == ['pre-', ['uno'], '-post']


def test_one2_oneormore_with_words():
    parsed = one_with_words_matcher('pre-unouno-post')
    assert parsed == ['pre-', ['uno', 'uno'], '-post']


def test_two_oneormore_with_words():
    parsed = one_with_words_matcher('pre-unounounouno-post')
    assert parsed == ['pre-', ['uno', 'uno', 'uno', 'uno'], '-post']
