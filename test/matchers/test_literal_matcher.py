# -*- encoding: utf-8 -*-
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


def test_literal_lengths():
    assert matchers[0].minimum_length() == 5
    assert matchers[0].maximum_length() == 5


def test_literal_matcher():
    parse = ['aeiou']
    for matcher in matchers:
        for p in parse:
            parsed = matcher(p)
            assert parsed == p


def test_literal_matcher_unicode():
    parse = u'あえうえお'
    parsed = Literal(u'あえうえお')(parse)
    assert parsed == parse


def test_literal_matcher_fail():
    parse = ['bad']
    for matcher in matchers:
        for p in parse:
            with raises(ParseException):
                matcher(p)
