from pytest import raises
from woodpyle import *


matchers = [
    Literal('aeiou'),
    L('aeiou'),
    ]


def test_literal_grammar():
    parse = ['aeiou']
    for matcher in matchers:
        for p in parse:
            parsed = matcher.parse_string(p)
            assert isinstance(parsed, Result)
            assert parsed == p


def test_literal_grammar_fail():
    parse = ['bad']
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher.parse_string(p)
