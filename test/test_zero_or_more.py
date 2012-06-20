from woodpyle import *


class TestZeroOrMoreGrammar(Grammar):
    grammar = ZeroOrMore(Literal('zero'))


def test_zero_zeroormore():
    parsed = TestZeroOrMoreGrammar('')
    assert isinstance(parsed, TestZeroOrMoreGrammar)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == []


def test_one_zeroormore():
    parsed = TestZeroOrMoreGrammar('zero')
    assert isinstance(parsed, TestZeroOrMoreGrammar)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == ['zero']


def test_two_zeroormore():
    parsed = TestZeroOrMoreGrammar('zerozero')
    assert isinstance(parsed, TestZeroOrMoreGrammar)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == ['zero', 'zero']


class TestZeroOrMoreWithWordsGrammar(Grammar):
    grammar = Literal('pre') + ZeroOrMore(Literal('nada')) + Literal('post')


def test_zero_zeroormore_with_words():
    parsed = TestZeroOrMoreWithWordsGrammar('pre post')
    assert isinstance(parsed, TestZeroOrMoreWithWordsGrammar)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == 'pre'
    assert parsed[2] == 'post'
    assert parsed[1] == []


def test_oneo_zeroormore_with_words():
    parsed = TestZeroOrMoreWithWordsGrammar('pre nada post')
    assert isinstance(parsed, TestZeroOrMoreWithWordsGrammar)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == 'pre'
    assert parsed[2] == 'post'
    assert parsed[1] == ['nada']


def test_two_zeroormore_with_words():
    parsed = TestZeroOrMoreWithWordsGrammar('pre nada nada post')
    assert isinstance(parsed, TestZeroOrMoreWithWordsGrammar)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == 'pre'
    assert parsed[2] == 'post'
    assert parsed[1] == ['nada', 'nada']
