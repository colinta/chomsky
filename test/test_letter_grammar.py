from pytest import raises
from woodpyle import *


class TestGrammar(Grammar):
    grammar = Letter('aeiou')


class TestGrammarShort(Grammar):
    grammar = A('aeiou')


def test_letter_grammar():
    parse = 'a e i o u'.split(' ')
    for TestGrammarClass in [TestGrammar, TestGrammarShort]:
        for p in parse:
            parsed = TestGrammarClass(p)
            assert isinstance(parsed, TestGrammarClass)
            assert isinstance(parsed.parsed, ResultList)
            assert parsed[0] == p


def test_letter_grammar_fail():
    parse = 'b c d'.split(' ')
    for TestGrammarClass in [TestGrammar, TestGrammarShort]:
        for p in parse:
            with raises(ParseException):
                TestGrammarClass(p)
