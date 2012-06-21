from chomsky import *
from chomsky.matchers import AutoSequence


def test_two_products():
    grammar = Word('aeiou') * 2
    test_grammar = AutoSequence(Word('aeiou'), Word('aeiou'))
    assert grammar == test_grammar


def test_sequence_product():
    grammar = Sequence(Word('abcde')) * 2
    test_grammar = Sequence(Word('abcde')) + Sequence(Word('abcde'))
    assert grammar == test_grammar


def test_three_products():
    grammar = Word('aeiou') * 3
    test_grammar = AutoSequence(Word('aeiou'), Word('aeiou'), Word('aeiou'))
    assert grammar == test_grammar
