from pytest import raises
from woodpyle import *


class TestGrammarTwo(Grammar):
    grammar = Word('aeiou') + Word('abcde')


class TestGrammarTwoShort(Grammar):
    grammar = W('aeiou') + W('abcde')


class TestGrammarThree(Grammar):
    grammar = Word('aeiou') + Word('abcde') + Word('12345')


class TestGrammarThreeShort(Grammar):
    grammar = W('aeiou') + W('abcde') + W('12345')


def factory(s):
    return map(lambda s: s.replace('_', ' '), s.split(' '))


def test_grammar_two():
    parse = factory('a_a ae_ab aei_abc aeio_abcd aeiou_abcde uoiea_edcba')
    for TestGrammarClass in [TestGrammarTwo, TestGrammarTwoShort]:
        for p in parse:
            parsed = TestGrammarClass(p)
            print repr(p)
            print repr(parsed)
            assert isinstance(parsed, TestGrammarClass)
            assert isinstance(parsed.parsed, ResultList)
            assert parsed[0] == p.split(' ')[0]
            assert parsed[1] == ' '
            assert parsed[2] == p.split(' ')[1]


def test_grammar_two_fail():
    parse = factory('bcd_abc ae_xzy bcd_xyz')
    for TestGrammarClass in [TestGrammarTwo, TestGrammarTwoShort]:
        for p in parse:
            with raises(ParseException):
                TestGrammarClass(p)


def test_grammar_three():
    parse = factory('a_a_1 ae_ab_12 aei_abc_123 aeio_abcd_1234 aeiou_abcde_12345 uoiea_edcba_54321')
    for TestGrammarClass in [TestGrammarThree, TestGrammarThreeShort]:
        for p in parse:
            parsed = TestGrammarClass(p)
            print repr(p)
            print repr(parsed)
            assert isinstance(parsed, TestGrammarClass)
            assert isinstance(parsed.parsed, ResultList)
            assert parsed[0] == p.split(' ')[0]
            assert parsed[1] == ' '
            assert parsed[2] == p.split(' ')[1]
            assert parsed[3] == ' '
            assert parsed[4] == p.split(' ')[2]


def test_grammar_three_fail():
    parse = factory('bcd_abc ae_xzy bcd_xyz')
    for TestGrammarClass in [TestGrammarThree, TestGrammarThreeShort]:
        for p in parse:
            with raises(ParseException):
                TestGrammarClass(p)
