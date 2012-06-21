from pytest import raises
from chomsky import *


def test_regex_grammar():
    matchers = [
        Regex(r'a[bc]+d(1|2|3)'),
        R('a[bc]+d(1|2|3)'),
        ]
    parse = 'abd1 acd1 abcd1 abbccd2 abcbcbcd3'.split(' ')
    for matcher in matchers:
        for p in parse:
            parsed = matcher(p)
            assert isinstance(parsed, Result)
            assert parsed == p


def test_regex_grammar_options():
    matcher = Regex(r'([0-9])([0-9])', group=1)
    parsed = matcher('23')
    assert isinstance(parsed, Result)
    assert parsed == '2'


def test_regex_grammar_more_options():
    matcher = Sequence(Regex(r'([0-9])([0-9]+)', group=2, advance=1) * 3)
    parsed = matcher('1234')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == '234'
    assert parsed[1] == '34'
    assert parsed[2] == '4'


def test_regex_grammar_even_more_options():
    matcher = Sequence(Regex(r'([0-9])([0-9])([0-9])', group=(1, 3)) * 3, sep=Whitespace)
    parsed = matcher('123 456 789')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == ['1', '3']
    assert parsed[1] == ['4', '6']
    assert parsed[2] == ['7', '9']


def test_regex_grammar_fail():
    matcher = Regex(r'a[bc]+d(1|2|3)')
    parse = 'abcd abcd4'.split(' ')
    for p in parse:
        with raises(ParseException):
            matcher(p)
