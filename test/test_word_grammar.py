from pytest import raises
from woodpyle import *


class TestGrammar(Grammar):
    grammar = Word('aeiou')


class TestGrammarShort(Grammar):
    grammar = W('aeiou')


def test_word_grammar():
    parse = 'a ae aei aeio aeiou'.split(' ')
    for TestGrammarClass in [TestGrammar, TestGrammarShort]:
        for p in parse:
            print TestGrammarClass.grammar
            parsed = TestGrammarClass(p)
            assert isinstance(parsed, TestGrammarClass)
            assert isinstance(parsed.parsed, ResultList)
            assert parsed[0] == p


def test_word_grammar_fail():
    parse = 'b bc bad'.split(' ')
    for TestGrammarClass in [TestGrammar, TestGrammarShort]:
        for p in parse:
            with raises(ParseException):
                TestGrammarClass(p)
