from pytest import raises
from chomsky import *


class GrammarMatcherMixTest(Grammar):
    grammar = Integer + Literal('+') + Integer + Literal('.')


def test_grammar_matcher_mix_repr():
    assert repr(GrammarMatcherMixTest('0+1.')) == "GrammarMatcherMixTest('0+1.')"


def test_grammar_matcher_mix_type():
    assert isinstance(GrammarMatcherMixTest('0 + 1.'), GrammarMatcherMixTest)


def test_grammar_matcher_mix_raises():
    with raises(ParseException):
        assert isinstance(GrammarMatcherMixTest('0 + 1'), GrammarMatcherMixTest)


def test_grammar_matcher_mix_grammar_0plus1():
    m = GrammarMatcherMixTest('0 + 1.')
    assert m.parsed == [Integer('0'), '+', Integer('1'), '.']
    assert str(m) == '0+1.'


def test_grammar_matcher_mix_grammar_newlines():
    m = GrammarMatcherMixTest('0\n+\n1.')
    assert m.parsed == [Integer('0'), '+', Integer('1'), '.']
    assert str(m) == '0+1.'
