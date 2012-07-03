from pytest import raises
from chomsky import *


matchers = [
    Letter('aeiou'),
    A('aeiou'),
    ]


def test_letter_matcher_repr():
    assert repr(Letter('aeiou')) == "Letter('aeiou')"
    assert repr(A('aeiou')) == "Letter('aeiou')"
    assert repr(Letter('aeiou', suppress=False)) == "Letter('aeiou')"
    assert repr(Letter('aeiou', suppress=True)) == "Letter('aeiou', suppress=True)"


def test_letter_matcher_lengths():
    assert matchers[0].minimum_length() == 1
    assert matchers[0].maximum_length() == 1


def test_letter_matcher():
    parse = 'a e i o u'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher.parse_string(p)
            assert parsed == p


def test_letter_matcher_fail():
    parse = 'b c d'.split(' ')
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher.parse_string(p)
