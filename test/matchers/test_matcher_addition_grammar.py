from pytest import raises
from woodpyle import *


class TestGrammarThree(Grammar):
    grammar = Word('aeiou') + S() + Word('abcde') + S() + Word('12345')


class TestGrammarThreeShort(Grammar):
    grammar = W('aeiou') + S() + W('abcde') + S() + W('12345')


def factory(s):
    return map(lambda s: s.replace('_', ' '), s.split(' '))


two_matchers = [
    Word('aeiou') + Whitespace() + Word('abcde'),
    W('aeiou') + S() + W('abcde'),
    ]
three_matchers = [
    Word('aeiou') + S() + Word('abcde') + S() + Word('12345'),
    W('aeiou') + S() + W('abcde') + S() + W('12345'),
    ]


def test_addition_grammar_two():
    parse = factory('a_a ae_ab aei_abc aeio_abcd aeiou_abcde uoiea_edcba')
    for matcher in two_matchers:
        for p in parse:
            parsed = matcher.parse_string(p)
            assert isinstance(parsed, ResultList)
            assert parsed[0] == p.split(' ')[0]
            assert parsed[1] == p.split(' ')[1]


def test_addition_grammar_two_fail():
    parse = factory('bcd_abc ae_xzy bcd_xyz')
    for matcher in two_matchers:
        for p in parse:
            with raises(ParseException):
                matcher.parse_string(p)


def test_addition_grammar_three():
    parse = factory('a_a_1 ae_ab_12 aei_abc_123 aeio_abcd_1234 aeiou_abcde_12345 uoiea_edcba_54321')
    for matcher in three_matchers:
        for p in parse:
            parsed = matcher.parse_string(p)
            assert isinstance(parsed, ResultList)
            assert parsed[0] == p.split(' ')[0]
            assert parsed[1] == p.split(' ')[1]
            assert parsed[2] == p.split(' ')[2]


def test_addition_grammar_three_fail():
    parse = factory('bcd_abc ae_xzy bcd_xyz')
    for matcher in three_matchers:
        for p in parse:
            with raises(ParseException):
                matcher.parse_string(p)
