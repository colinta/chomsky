from pytest import raises
from chomsky import *
from chomsky.matchers import AutoSequence
import string


def test_two_products():
    matcher = Literal('aeiou') * 2
    test_matcher = Exactly(Literal('aeiou'), 2)
    assert matcher == test_matcher
    assert matcher('aeiouaeiou') == ['aeiou', 'aeiou']


def test_two_products_lengths():
    matcher = Literal('aeiou') * 2
    assert matcher.minimum_length() == 10
    assert matcher.maximum_length() == 10


def test_sequence_product():
    matcher = Sequence(Literal('abcde')) * 2
    test_matcher = Exactly(Sequence(Literal('abcde')), 2)
    assert matcher == test_matcher
    assert matcher('abcdeabcde') == [['abcde'], ['abcde']]


def test_three_products():
    matcher = Literal('aeiou') * 3
    test_matcher = Exactly(Literal('aeiou'), 3)
    assert matcher == test_matcher
    assert matcher('aeiouaeiouaeiou') == ['aeiou', 'aeiou', 'aeiou']


def test_three_sequence_products():
    matcher = (Chars(string.letters) + Literal(' ')) * 3
    assert matcher('why hello there ') == [['why', ' '], ['hello', ' '], ['there', ' ']]
    with raises(ParseException):
        print matcher('not enough spaces')
