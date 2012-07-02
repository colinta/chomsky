from chomsky import *
from chomsky.matchers import AutoSequence


def test_two_sequences_repr():
    matcher = Sequence(Word('aeiou'), Word('abcde'))
    assert repr(matcher) == "Sequence(Word('aeiou'), Word('abcde'))"


def test_three_sequences_repr():
    matcher = Sequence(Word('aeiou'), Word('abcde'), Word('12345'))
    assert repr(matcher) == "Sequence(Word('aeiou'), Word('abcde'), Word('12345'))"


def test_two_sequences():
    matcher = Sequence(Word('aeiou'), Word('bcdfg'))
    parsed = matcher('aeioufgbcd')
    assert parsed == ['aeiou', 'fgbcd']


def test_two_sequence_shorthand():
    matcher = Sequence('word1', 'word1')
    parsed = matcher('word1word1')
    assert parsed == ['word1', 'word1']


def test_sequence_addition():
    matcher = Sequence(Word('abcde')) + Sequence(Word('aeiou'))
    test_matcher = Sequence(Word('abcde')) + Sequence(Word('aeiou'))
    assert matcher == test_matcher


def test_three_sequences():
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
