from pytest import raises
from chomsky import *


class GrammarSequenceTest(Grammar):
    grammar = Integer + Operator + Integer


def test_grammarsequence_repr():
    assert repr(GrammarSequenceTest('0 + 1')) == "GrammarSequenceTest('0 + 1')"


def test_grammarsequence_type():
    assert isinstance(GrammarSequenceTest('0 + 1'), GrammarSequenceTest)


def test_grammarsequence_grammar_0():
    m = GrammarSequenceTest('0 + 1')
    assert m.parsed == [Integer('0'), Operator('+'), Integer('1')]
    assert str(m) == '0+1'
