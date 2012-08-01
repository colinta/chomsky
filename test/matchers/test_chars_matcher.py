from pytest import raises
from chomsky import *


matchers = [
    Chars('aeiou'),
    W('aeiou'),
    ]


def test_word_repr():
    assert repr(Chars('aeiou')) == "Chars('aeiou')"
    assert repr(Chars('aeiou', min=1)) == "Chars('aeiou')"
    assert repr(Chars('aeiou', min=2)) == "Chars('aeiou', min=2)"
    assert repr(Chars('aeiou', max=2)) == "Chars('aeiou', max=2)"
    assert repr(Chars('aeiou', min=2, max=3)) == "Chars('aeiou', min=2, max=3)"
    assert repr(Chars('aeiou', suppress=False)) == "Chars('aeiou')"
    assert repr(Chars('aeiou', suppress=True)) == "Chars('aeiou', suppress=True)"
    assert repr(Chars('aeiou', inverse=True)) == "Chars('aeiou', inverse=True)"
    assert repr(W('aeiou')) == "Chars('aeiou')"


def test_word_matcher():
    parse = 'a ae aei aeio aeiou'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher(p)
            assert parsed == p


def test_inverse_word_matcher():
    parse = 'b bc bc! bc!: bc!:-'.split(' ')
    matcher = Chars('aeiou', inverse=True)
    for p in parse:
        parsed = matcher(p)
        assert parsed == p


def test_word_matcher_fail():
    parse = 'b bc bad'.split(' ')
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher(p)
