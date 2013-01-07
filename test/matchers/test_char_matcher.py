# -*- encoding: utf-8 -*-
from pytest import raises
from chomsky import *


matchers = [
    Char('aeiou'),
    A('aeiou'),
    ]


def test_char_matcher_repr():
    assert repr(Char('aeiou')) == "Char('aeiou')"
    assert repr(A('aeiou')) == "Char('aeiou')"
    assert repr(Char('aeiou', suppress=False)) == "Char('aeiou')"
    assert repr(Char('aeiou', suppress=True)) == "Char('aeiou', suppress=True)"
    assert repr(Char('aeiou', inverse=True)) == "Char('aeiou', inverse=True)"
    assert repr(Char(u'aeiou', inverse=True)) == "Char(u'aeiou', inverse=True)"


def test_char_matcher_lengths():
    assert matchers[0].minimum_length() == 1
    assert matchers[0].maximum_length() == 1


def test_char_matcher():
    parse = 'a e i o u'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher(p)
            assert parsed == p


def test_char_matcher_unicode():
    parse = u'あ い う え お'.split(' ')
    for p in parse:
        parsed = Char(u'あいうえお')(p)
        assert parsed == p


def test_any_char_matcher():
    parse = 'a e i o u'.split(' ')
    for p in parse:
        assert Char()(p) == p


def test_inverse_char_matcher():
    parse = 'b c d f g h ! @ # $ % ^ & * ( )'.split(' ')
    matcher = Char('aeiou', inverse=True)
    for p in parse:
        parsed = matcher(p)
        assert parsed == p


def test_char_matcher_fail():
    parse = 'b c d'.split(' ')
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher(p)
