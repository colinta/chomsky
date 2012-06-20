from pytest import raises
from woodpyle import *


class TestGrammar1(Grammar):
    grammar = Regex(r'a[bc]+d(1|2|3)')


class TestGrammarShort(Grammar):
    grammar = R('a[bc]+d(1|2|3)')


class TestGrammarGroup(Grammar):
    grammar = Regex(r'([0-9])([0-9])', group=1)


class TestGrammarGroupAdvance(Grammar):
    grammar = Sequence(Regex(r'([0-9])([0-9]+)', group=2, advance=1) * 3, whitespace=None)


class TestGrammarMultipleGroups(Grammar):
    grammar = Sequence(Regex(r'([0-9])([0-9])([0-9])', group=(1, 3)) * 3)


def test_regex_grammar():
    parse = 'abd1 acd1 abcd1 abbccd2 abcbcbcd3'.split(' ')
    for TestGrammarClass in [TestGrammar1, TestGrammarShort]:
        for p in parse:
            parsed = TestGrammarClass(p)
            assert isinstance(parsed, TestGrammarClass)
            assert isinstance(parsed.parsed, ResultList)
            assert parsed[0] == p


def test_regex_grammar_options():
    parsed = TestGrammarGroup('23')
    assert isinstance(parsed, TestGrammarGroup)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == '2'


def test_regex_grammar_more_options():
    parsed = TestGrammarGroupAdvance('1234')
    assert isinstance(parsed, TestGrammarGroupAdvance)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == '234'
    assert parsed[1] == '34'
    assert parsed[2] == '4'


def test_regex_grammar_even_more_options():
    parsed = TestGrammarMultipleGroups('123 456 789')
    assert isinstance(parsed, TestGrammarMultipleGroups)
    assert isinstance(parsed.parsed, ResultList)
    assert parsed[0] == ['1', '3']
    assert parsed[1] == ['4', '6']
    assert parsed[2] == ['7', '9']


def test_regex_grammar_fail():
    parse = 'abcd abcd4'.split(' ')
    for p in parse:
        with raises(ParseException):
            TestGrammar1(p)
