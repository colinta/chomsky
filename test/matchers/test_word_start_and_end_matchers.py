from pytest import raises
from chomsky import *


def test_string_boundary_repr():
    assert repr(WordStart()) == 'WordStart()'
    assert repr(WordEnd()) == 'WordEnd()'
    assert repr(WordStart(suppress=False)) == 'WordStart(suppress=False)'
    assert repr(WordEnd(suppress=False)) == 'WordEnd(suppress=False)'


def test_start_of_word_and_literal_matcher():
    matcher = L('hi!') + WordStart() + L('bye!')
    parsed = matcher('hi!bye!')
    assert parsed == ['hi!', 'bye!']


def test_end_of_word_and_literal_matcher():
    matcher = L('hi') + WordEnd() + L('!bye!')
    parsed = matcher('hi!bye!')
    assert parsed == ['hi', '!bye!']


def test_start_and_end_of_word_matcher():
    matcher = L('hi!') + WordStart() + L('hello') + WordEnd() + L('!bye!')
    parsed = matcher('hi!hello!bye!')
    assert parsed == ['hi!', 'hello', '!bye!']


def test_multiple_start_and_end_of_word_matcher():
    matcher = L('hi!') + WordStart() + WordStart() + L('hello') + WordEnd() + WordEnd() + L('!bye!')
    parsed = matcher('hi!hello!bye!')
    assert parsed == ['hi!', 'hello', '!bye!']


def test_start_of_word_matcher_fail():
    matcher = L('test') + WordStart()
    with raises(ParseException):
        print matcher('test')


def test_end_of_word_matcher_fail():
    matcher = Literal('hi!') + WordEnd()
    with raises(ParseException):
        print matcher('hi!')
