from pytest import raises
from woodpyle import *


class TestGrammar(Grammar):
    grammar = Whitespace()


class TestGrammarNl(Grammar):
    grammar = Whitespace(' \t\n\r')


def test_whitespace_grammar():
    p = ' \t'
    parsed = TestGrammar(p)
    assert isinstance(parsed, TestGrammar)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == p


def test_whitespace_nl_grammar():
    p = ' \t\n'
    parsed = TestGrammarNl(p)
    assert isinstance(parsed, TestGrammarNl)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == p


def test_whitespace_grammar_fail():
    with raises(ParseException):
        TestGrammar('abc')


def test_whitespace_nl_grammar_fail():
    with raises(ParseException):
        TestGrammarNl('abc')
