from pytest import raises
from chomsky import *


class OneLineGrammarTest(Grammar):
    grammar = OneLine(Integer + Operator + Integer)


def test_oneline_repr():
    assert repr(OneLineGrammarTest('0 + 1')) == "OneLineGrammarTest('0+1')"


def test_oneline_type():
    assert isinstance(OneLineGrammarTest('0 + 1'), OneLineGrammarTest)


def test_oneline_grammar_0plus1():
    m = OneLineGrammarTest('0 + 1')
    assert m.parsed == [Integer('0'), Operator('+'), Integer('1')]
    assert str(m) == '0+1'


def test_oneline_grammar_newlines_fail():
    with raises(ParseException):
        OneLineGrammarTest('0\n+\n1')
    with raises(ParseException):
        OneLineGrammarTest('0+\n1')

def test_oneline_grammar_newlines_pass():
    # but this is fine
    m = OneLineGrammarTest('0+1\n')
    assert m.parsed == [Integer('0'), Operator('+'), Integer('1')]
    assert str(m) == '0+1'
