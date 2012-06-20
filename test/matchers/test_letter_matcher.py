from pytest import raises
from woodpyle import *


matchers = [
    Letter('aeiou'),
    A('aeiou'),
    ]


def test_letter_matcher():
    parse = 'a e i o u'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher.parse_string(p)
            assert isinstance(parsed, Result)
            assert parsed == p


def test_letter_matcher_fail():
    parse = 'b c d'.split(' ')
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher.parse_string(p)
