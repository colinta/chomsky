# -*- encoding: utf-8 -*-
from pytest import raises
from chomsky import *


matchers = [
    Chars('aeiou'),
    W('aeiou'),
    ]


def test_chars_repr():
    assert repr(Chars('aeiou')) == "Chars('aeiou')"
    assert repr(Chars('aeiou', min=1)) == "Chars('aeiou')"
    assert repr(Chars('aeiou', min=2)) == "Chars('aeiou', min=2)"
    assert repr(Chars('aeiou', max=2)) == "Chars('aeiou', max=2)"
    assert repr(Chars('aeiou', min=2, max=3)) == "Chars('aeiou', min=2, max=3)"
    assert repr(Chars('aeiou', suppress=False)) == "Chars('aeiou')"
    assert repr(Chars('aeiou', suppress=True)) == "Chars('aeiou', suppress=True)"
    assert repr(Chars('aeiou', inverse=True)) == "Chars('aeiou', inverse=True)"
    assert repr(W('aeiou')) == "Chars('aeiou')"
    assert repr(W(u'aeiou')) == "Chars(u'aeiou')"
    assert repr(W(u'あいうえお')) == "Chars(u'\\u3042\\u3044\\u3046\\u3048\\u304a')"


def test_chars_matcher():
    parse = 'a ae aei aeio aeiou'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher(p)
            assert parsed == p


def test_chars_matcher_unicode():
    parse = u'あ あい あいう あいうえ あいうえお'.split(' ')
    for p in parse:
        parsed = Chars(u'あいうえお')(p)
        assert parsed == p


def test_inverse_word_matcher():
    parse = 'b bc bc! bc!: bc!:-'.split(' ')
    matcher = Chars('aeiou', inverse=True)
    for p in parse:
        parsed = matcher(p)
        assert parsed == p
    parsed = matcher('bc!a')
    assert parsed == 'bc!'


def test_chars_matcher_fail():
    parse = 'b bc bad'.split(' ')
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher(p)
