from pytest import raises
from chomsky import *


def test_whitespace_repr():
    assert repr(Whitespace()) == "Whitespace()"
    assert repr(Whitespace(suppress=False)) == "Whitespace(suppress=False)"
    assert repr(Whitespace(' \t\n\r')) == "Whitespace(' \\t\\n\\r')"
    assert repr(Whitespace(' \t\n\r', suppress=False)) == "Whitespace(' \\t\\n\\r', suppress=False)"


def test_whitespace_matcher():
    matcher = Whitespace()
    p = ' \t'
    parsed = matcher(p)
    assert isinstance(parsed, Result)
    assert parsed == p


def test_whitespace_nl_matcher():
    matcher = Whitespace(' \t\n\r')
    p = ' \t\n'
    parsed = matcher(p)
    assert isinstance(parsed, Result)
    assert parsed == p


def test_whitespace_matcher_fail():
    matcher = Whitespace()
    with raises(ParseException):
        matcher('abc')


def test_whitespace_nl_matcher_fail():
    matcher = Whitespace()
    with raises(ParseException):
        matcher('abc')
