from pytest import raises
from chomsky import *


class GrammarInMatcherTest(Grammar):
    grammar = Any(Integer, String)


def test_grammar_in_matcher_repr():
    assert repr(GrammarInMatcherTest('0')) == "GrammarInMatcherTest('0')"


def test_grammar_in_matcher_type():
    assert isinstance(GrammarInMatcherTest('0'), GrammarInMatcherTest)
    assert isinstance(GrammarInMatcherTest('"test"'), GrammarInMatcherTest)


def test_grammar_in_matcher_grammar_0():
    m = GrammarInMatcherTest('0')
    assert m.parsed == Integer('0')
    assert str(m) == '0'


def test_grammar_in_matcher_grammar_test():
    m = GrammarInMatcherTest('"test"')
    assert m.parsed == String('"test"')
    assert str(m) == 'test'
