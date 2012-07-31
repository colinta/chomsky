from chomsky import *


def test_two_group_repr():
    matcher = Group(Word('aeiou') + Word('abcde'))
    assert repr(matcher) == "Group(Sequence(Word('aeiou') + Word('abcde')))"


def test_three_group_repr():
    matcher = Group(Sequence(Word('aeiou'), Word('abcde'), Word('12345')))
    assert repr(matcher) == "Group(Sequence(Word('aeiou'), Word('abcde'), Word('12345')))"


def test_two_group():
    matcher = Group(Word('aeiou'), Word('bcdfg'))
    parsed = matcher('aeioufgbcd')
    assert parsed == 'aeioufgbcd'


def test_two_sequence_shorthand():
    matcher = Sequence('word1', 'word1')
    parsed = matcher('word1word1')
    assert parsed == ['word1', 'word1']


def test_sequence_addition():
    matcher = Sequence(Word('abcde')) + Sequence(Word('aeiou'))
    test_matcher = Sequence(Word('abcde')) + Sequence(Word('aeiou'))
    assert matcher == test_matcher


def test_three_group():
    matcher = Group(Word('aeiou') + Word('pqrst') + Word('12345'))
    assert matcher('aeioupqrst12345') == 'aeioupqrst12345'


def test_sequence_addition_left():
    matcher = Word('aeiou') + Group(Word('pqrst') + Word('12345'))
    assert matcher('aeioupqrst12345') == ['aeiou', 'pqrst12345']


def test_sequence_addition_right():
    matcher = Group(Word('aeiou') + Word('pqrst')) + Word('12345')
    assert matcher('aeioupqrst12345') == ['aeioupqrst', '12345']


def test_sequence_addition_nested():
    matcher = Group(Word('aeiou') + Sequence(Word('pqrst') + Word('12345')))
    assert matcher('aeioupqrst12345') == 'aeioupqrst12345'
