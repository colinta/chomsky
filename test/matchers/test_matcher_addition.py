from chomsky import *
from chomsky.matchers import AutoSequence


def test_two_additions_repr():
    matcher = Chars('aeiou') + Chars('abcde')
    assert repr(matcher) == "Sequence(Chars('aeiou') + Chars('abcde'))"


def test_two_literal_additions_lengths():
    matcher = Literal('word1') + Literal('other words')
    assert matcher.minimum_length() == 16
    assert matcher.maximum_length() == 16


def test_two_additions_lengths():
    matcher = Chars('abcd') + Literal('other words')
    assert matcher.minimum_length() == 12
    assert matcher.maximum_length() == Infinity


def test_three_additions_repr():
    matcher = Chars('aeiou') + Chars('abcde') + Chars('12345')
    assert repr(matcher) == "Sequence(Chars('aeiou') + Chars('abcde') + Chars('12345'))"


def test_three_additions_lengths():
    matcher = Chars('aeiou') + Chars('abcde') + Chars('12345')
    assert matcher.minimum_length() == 3
    assert matcher.maximum_length() == Infinity


def test_two_additions():
    matcher = Chars('aeiou') + Chars('bcdef')
    test_matcher = AutoSequence(Chars('aeiou'), Chars('bcdef'))
    assert matcher == test_matcher
    assert matcher('uoiaeaiuiobcdef') == ['uoiaeaiuio', 'bcdef']


def test_two_additions_shorthand():
    matcher = Chars('aeiou') + 'bcdef'
    test_matcher = AutoSequence(Chars('aeiou'), Literal('bcdef'))
    assert matcher == test_matcher
    assert matcher('aeioubcdef') == ['aeiou', 'bcdef']


def test_two_additions_reverse_shorthand():
    matcher = 'aeiou' + Chars('bcdef')
    test_matcher = AutoSequence(Literal('aeiou'), Chars('bcdef'))
    assert matcher == test_matcher
    assert matcher('aeioubcdef') == ['aeiou', 'bcdef']


def test_sequence_addition():
    matcher = Sequence(Chars('abcde')) + Sequence(Chars('fghij'))
    test_matcher = Sequence(Chars('abcde')) + Sequence(Chars('fghij'))
    assert matcher == test_matcher
    assert matcher('abcdejhifg') == [['abcde'], ['jhifg']]


def test_three_additions():
    matcher = Chars('aeiou') + Chars('abcde') + Chars('12345')
    test_matcher = AutoSequence(Chars('aeiou'), Chars('abcde'), Chars('12345'))
    assert matcher == test_matcher


def test_sequence_addition_left():
    matcher = Chars('aeiou') + Sequence(Chars('abcde'), Chars('12345'))
    test_matcher = AutoSequence(Chars('aeiou'), Sequence(Chars('abcde'), Chars('12345')))
    assert matcher == test_matcher


def test_sequence_addition_right():
    matcher = Sequence(Chars('aeiou'), Chars('abcde')) + Chars('12345')
    test_matcher = AutoSequence(Sequence(Chars('aeiou'), Chars('abcde')), Chars('12345'))
    assert matcher == test_matcher


def test_literal_shorthands():
    matcher = ' ' + Chars('abcde') + ' '
    assert matcher == Sequence(L(' '), Chars('abcde'), L(' '))
