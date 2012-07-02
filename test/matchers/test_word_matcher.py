from pytest import raises
from chomsky import *


matchers = [
    Word('aeiou'),
    W('aeiou'),
    ]


def test_word_repr():
    assert repr(Word('aeiou')) == "Word('aeiou')"
    assert repr(Word('aeiou', min=1)) == "Word('aeiou')"
    assert repr(Word('aeiou', min=2)) == "Word('aeiou', min=2)"
    assert repr(Word('aeiou', max=2)) == "Word('aeiou', max=2)"
    assert repr(Word('aeiou', min=2, max=3)) == "Word('aeiou', min=2, max=3)"
    assert repr(Word('aeiou', suppress=False)) == "Word('aeiou')"
    assert repr(Word('aeiou', suppress=True)) == "Word('aeiou', suppress=True)"
    assert repr(W('aeiou')) == "Word('aeiou')"


def test_word_matcher():
    parse = 'a ae aei aeio aeiou'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher(p)
            assert isinstance(parsed, Result)
            assert parsed == p


def test_word_matcher_fail():
    parse = 'b bc bad'.split(' ')
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher(p)
