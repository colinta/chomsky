from pytest import raises
from chomsky import *


matchers = [
    Word('aeiou'),
    W('aeiou'),
    ]


def test_word_grammar():
    parse = 'a ae aei aeio aeiou'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher(p)
            assert isinstance(parsed, Result)
            assert parsed == p


def test_word_grammar_fail():
    parse = 'b bc bad'.split(' ')
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher(p)
