from pytest import raises
from woodpyle import *


class TestGrammar(Grammar):
    grammar = Literal('aeiou')


class TestGrammarShort(Grammar):
    grammar = L('aeiou')


def test_literal_grammar():
    parse = 'aeiou'.split(' ')
    for TestGrammarClass in [TestGrammar, TestGrammarShort]:
        for p in parse:
            parsed = TestGrammarClass(p)
            assert isinstance(parsed, TestGrammarClass)
            assert isinstance(parsed.parsed, ResultList)
            assert parsed[0] == p


def test_literal_grammar_fail():
    parse = 'bad'.split(' ')
    for TestGrammarClass in [TestGrammar, TestGrammarShort]:
        for p in parse:
            with raises(ParseException):
                TestGrammarClass(p)
