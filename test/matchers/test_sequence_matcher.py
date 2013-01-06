from chomsky import *
from chomsky.matchers import AutoSequence


def test_two_sequences_repr():
    matcher = Sequence(Chars('aeiou'), Chars('abcde'))
    assert repr(matcher) == "Sequence(Chars('aeiou'), Chars('abcde'))"


def test_nested_sequences_repr():
    matcher = Sequence(L('b') + 'c')
    assert repr(matcher) == "Sequence(Literal('b'), Literal('c'))"


def test_two_autosequences_repr():
    matcher = Chars('aeiou') + Chars('abcde')
    assert repr(matcher) == "(Chars('aeiou') + Chars('abcde'))"


def test_three_sequences_repr():
    matcher = Sequence(Chars('aeiou'), Chars('abcde'), Chars('12345'))
    assert repr(matcher) == "Sequence(Chars('aeiou'), Chars('abcde'), Chars('12345'))"


def test_three_autosequences_repr():
    matcher = Chars('aeiou') + Chars('abcde') + Chars('12345')
    assert repr(matcher) == "(Chars('aeiou') + Chars('abcde') + Chars('12345'))"


def test_two_sequences():
    matcher = Sequence(Chars('aeiou'), Chars('bcdfg'))
    parsed = matcher('aeioufgbcd')
    assert parsed == ['aeiou', 'fgbcd']


def test_two_sequence_shorthand():
    matcher = Sequence('word1', 'word1')
    parsed = matcher('word1word1')
    assert parsed == ['word1', 'word1']


def test_sequence_addition():
    matcher = Sequence(Chars('abcde')) + Sequence(Chars('aeiou'))
    test_matcher = Sequence(Chars('abcde')) + Sequence(Chars('aeiou'))
    assert matcher == test_matcher


def test_three_sequences():
    matcher = Chars('aeiou') + Chars('pqrst') + Chars('12345')
    test_matcher = AutoSequence(Chars('aeiou'), Chars('pqrst'), Chars('12345'))
    assert matcher == test_matcher
    assert matcher('aeioupqrst12345') == ['aeiou', 'pqrst', '12345']


def test_slice_sequences():
    matcher = (Literal('[') + Chars('aeiou') + Chars('pqrst') + Chars('12345') + Literal(']'))[1:-1]
    assert matcher('[aeioupqrst12345]') == ['aeiou', 'pqrst', '12345']


def test_slice_tuple_sequences():
    matcher = (Literal('[') + Chars('aeiou') + Chars('pqrst') + Chars('12345') + Literal(']'))[1, 3]
    assert matcher('[aeioupqrst12345]') == ['aeiou', '12345']


def test_three_sequences_whitespace_sep():
    matcher = Sequence(Chars('aeiou'), Chars('pqrst'), Chars('12345'), sep=Whitespace)
    assert matcher('auieoaieo ttrrssppqq 543212345') == ['auieoaieo', 'ttrrssppqq', '543212345']


def test_sequence_addition_left():
    matcher = Chars('aeiou') + Sequence(Chars('pqrst'), Chars('12345'))
    test_matcher = AutoSequence(Chars('aeiou'), Sequence(Chars('pqrst'), Chars('12345')))
    assert matcher == test_matcher
    assert matcher('aeioupqrst12345') == ['aeiou', ['pqrst', '12345']]


def test_sequence_addition_right():
    matcher = Sequence(Chars('aeiou'), Chars('pqrst')) + Chars('12345')
    test_matcher = AutoSequence(Sequence(Chars('aeiou'), Chars('pqrst')), Chars('12345'))
    assert matcher == test_matcher
    assert matcher('aeioupqrst12345') == [['aeiou', 'pqrst'], '12345']
