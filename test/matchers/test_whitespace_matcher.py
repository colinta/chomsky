from pytest import raises
from chomsky import *


def test_whitespace_repr():
    assert repr(Whitespace()) == "Whitespace()"
    assert repr(Whitespace(suppress=False)) == "Whitespace(suppress=False)"
    assert repr(Whitespace(' \t')) == "Whitespace(' \\t')"
    assert repr(Whitespace(' \t', suppress=False)) == "Whitespace(' \\t', suppress=False)"


def test_whitespace_matcher():
    matcher = Whitespace()
    p = ' \t'
    parsed = matcher(p)
    assert parsed == p


def test_empty_whitespace_matcher():
    matcher = Whitespace()
    p = ''
    parsed = matcher(p)
    assert parsed == p


def test_whitespace_nl_matcher():
    matcher = Whitespace(suppress=False)
    p = ' \t\n'
    parsed = matcher(p)
    assert parsed == p


def test_whitespace_matcher_fail():
    matcher = Whitespace(min=1)
    with raises(ParseException):
        print matcher('abc')


def test_whitespace_nl_matcher_fail():
    matcher = Whitespace(min=1)
    with raises(ParseException):
        print matcher('abc')
