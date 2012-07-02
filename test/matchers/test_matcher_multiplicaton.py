from pytest import raises
from chomsky import *
from chomsky.matchers import AutoSequence
import string


def test_two_products():
    matcher = Literal('aeiou') * 2
    test_matcher = AutoSequence(Literal('aeiou'), Literal('aeiou'))
    assert matcher == test_matcher
    assert matcher('aeiouaeiou') == ['aeiou', 'aeiou']


def test_sequence_product():
    matcher = Sequence(Literal('abcde')) * 2
    test_matcher = Sequence(Literal('abcde')) + Sequence(Literal('abcde'))
    assert matcher == test_matcher
    assert matcher('abcdeabcde') == [['abcde'], ['abcde']]


def test_three_products():
    matcher = Literal('aeiou') * 3
    test_matcher = AutoSequence(Literal('aeiou'), Literal('aeiou'), Literal('aeiou'))
    assert matcher == test_matcher
    assert matcher('aeiouaeiouaeiou') == ['aeiou', 'aeiou', 'aeiou']


def test_three_sequence_products():
    matcher = (Word(string.letters) + Literal(' ')) * 3
    assert matcher('why hello there ') == [['why', ' '], ['hello', ' '], ['there', ' ']]
    with raises(ParseException):
        matcher('not enough spaces')
