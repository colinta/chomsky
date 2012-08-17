# -*- encoding: utf-8 -*-
from chomsky import *


def test_two_group_repr():
    matcher = Group(Chars('aeiou') + Chars('abcde'))
    assert repr(matcher) == "Group(Chars('aeiou') + Chars('abcde'))"


def test_three_group_repr():
    matcher = Group(Sequence(Chars('aeiou'), Chars('abcde'), Chars('12345')))
    assert repr(matcher) == "Group(Sequence(Chars('aeiou'), Chars('abcde'), Chars('12345')))"


def test_two_group():
    matcher = Group(Chars('aeiou'), Chars('bcdfg'))
    parsed = matcher('aeioufgbcd')
    assert parsed == 'aeioufgbcd'


def test_two_group_unicode():
    matcher = Group(Chars(u'あいうえお'), Chars(u'べしでふじ'))
    parsed = matcher(u'いあえおうふじべしで')
    assert parsed == u'いあえおうふじべしで'


def test_two_sequence_shorthand():
    matcher = Sequence('word1', 'word1')
    parsed = matcher('word1word1')
    assert parsed == ['word1', 'word1']


def test_sequence_addition():
    matcher = Sequence(Chars('abcde')) + Sequence(Chars('aeiou'))
    test_matcher = Sequence(Chars('abcde')) + Sequence(Chars('aeiou'))
    assert matcher == test_matcher


def test_three_group():
    matcher = Group(Chars('aeiou') + Chars('pqrst') + Chars('12345'))
    assert matcher('aeioupqrst12345') == 'aeioupqrst12345'


def test_sequence_addition_left():
    matcher = Chars('aeiou') + Group(Chars('pqrst') + Chars('12345'))
    assert matcher('aeioupqrst12345') == ['aeiou', 'pqrst12345']


def test_sequence_addition_right():
    matcher = Group(Chars('aeiou') + Chars('pqrst')) + Chars('12345')
    assert matcher('aeioupqrst12345') == ['aeioupqrst', '12345']


def test_sequence_addition_nested():
    matcher = Group(Chars('aeiou') + Sequence(Chars('pqrst') + Chars('12345')))
    assert matcher('aeioupqrst12345') == 'aeioupqrst12345'
