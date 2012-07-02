from chomsky import *
from chomsky.matchers import AutoSequence


def test_two_additions_repr():
    matcher = Word('aeiou') + Word('abcde')
    assert repr(matcher) == "Sequence(Word('aeiou'), Word('abcde'))"


def test_three_additions_repr():
    matcher = Word('aeiou') + Word('abcde') + Word('12345')
    assert repr(matcher) == "Sequence(Word('aeiou'), Word('abcde'), Word('12345'))"


def test_two_additions():
    matcher = Word('aeiou') + Word('bcdef')
    test_matcher = AutoSequence(Word('aeiou'), Word('bcdef'))
    assert matcher == test_matcher
    assert matcher('uoiaeaiuiobcdef') == ['uoiaeaiuio', 'bcdef']


def test_two_additions_shorthand():
    matcher = Word('aeiou') + 'bcdef'
    test_matcher = AutoSequence(Word('aeiou'), Literal('bcdef'))
    assert matcher == test_matcher
    assert matcher('aeioubcdef') == ['aeiou', 'bcdef']


def test_two_additions_reverse_shorthand():
    matcher = 'aeiou' + Word('bcdef')
    test_matcher = AutoSequence(Literal('aeiou'), Word('bcdef'))
    assert matcher == test_matcher
    assert matcher('aeioubcdef') == ['aeiou', 'bcdef']


def test_sequence_addition():
    matcher = Sequence(Word('abcde')) + Sequence(Word('fghij'))
    test_matcher = Sequence(Word('abcde')) + Sequence(Word('fghij'))
    assert matcher == test_matcher
    assert matcher('abcdejhifg') == [['abcde'], ['jhifg']]


def test_three_additions():
    matcher = Word('aeiou') + Word('abcde') + Word('12345')
    test_matcher = AutoSequence(Word('aeiou'), Word('abcde'), Word('12345'))
    assert matcher == test_matcher


def test_sequence_addition_left():
    matcher = Word('aeiou') + Sequence(Word('abcde'), Word('12345'))
    test_matcher = AutoSequence(Word('aeiou'), Sequence(Word('abcde'), Word('12345')))
    assert matcher == test_matcher


def test_sequence_addition_right():
    matcher = Sequence(Word('aeiou'), Word('abcde')) + Word('12345')
    test_matcher = AutoSequence(Sequence(Word('aeiou'), Word('abcde')), Word('12345'))
    assert matcher == test_matcher
