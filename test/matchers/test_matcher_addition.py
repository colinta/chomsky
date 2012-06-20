from woodpyle import *
from woodpyle.matchers import AutoSequence


def test_two_additions():
    grammar = Word('aeiou') + Word('abcde')
    test_grammar = AutoSequence(Word('aeiou'), Word('abcde'))
    assert grammar == test_grammar


def test_sequence_addition():
    grammar = Sequence(Word('abcde')) + Sequence(Word('aeiou'))
    test_grammar = Sequence(Word('abcde')) + Sequence(Word('aeiou'))
    assert grammar == test_grammar


def test_three_additions():
    grammar = Word('aeiou') + Word('abcde') + Word('12345')
    test_grammar = AutoSequence(Word('aeiou'), Word('abcde'), Word('12345'))
    assert grammar == test_grammar


def test_sequence_addition_left():
    grammar = Word('aeiou') + Sequence(Word('abcde'), Word('12345'))
    test_grammar = AutoSequence(Word('aeiou'), Sequence(Word('abcde'), Word('12345')))
    assert grammar == test_grammar


def test_sequence_addition_right():
    grammar = Sequence(Word('aeiou'), Word('abcde')) + Word('12345')
    test_grammar = AutoSequence(Sequence(Word('aeiou'), Word('abcde')), Word('12345'))
    assert grammar == test_grammar
