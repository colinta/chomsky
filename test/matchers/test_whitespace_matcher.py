from pytest import raises
from woodpyle import *


def test_whitespace_grammar():
    matcher = Whitespace()
    p = ' \t'
    parsed = matcher(p)
    assert isinstance(parsed, Result)
    assert parsed == p


def test_whitespace_nl_grammar():
    matcher = Whitespace(' \t\n\r')
    p = ' \t\n'
    parsed = matcher(p)
    assert isinstance(parsed, Result)
    assert parsed == p


def test_whitespace_grammar_fail():
    matcher = Whitespace()
    with raises(ParseException):
        matcher('abc')


def test_whitespace_nl_grammar_fail():
    matcher = Whitespace()
    with raises(ParseException):
        matcher('abc')
