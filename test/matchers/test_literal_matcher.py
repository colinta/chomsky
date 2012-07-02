from pytest import raises
from chomsky import *


matchers = [
    Literal('aeiou'),
    L('aeiou'),
    ]


def test_literal_repr():
    assert repr(Literal('aeiou')) == "Literal('aeiou')"
    assert repr(Literal('aeiou', suppress=False)) == "Literal('aeiou')"
    assert repr(Literal('aeiou', suppress=True)) == "Literal('aeiou', suppress=True)"
    assert repr(L('aeiou')) == "Literal('aeiou')"


def test_literal_matcher():
    parse = ['aeiou']
    for matcher in matchers:
        for p in parse:
            parsed = matcher.parse_string(p)
            assert isinstance(parsed, Result)
            assert parsed == p


def test_literal_matcher_fail():
    parse = ['bad']
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher.parse_string(p)
