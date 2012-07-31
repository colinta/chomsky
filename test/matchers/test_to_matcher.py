from chomsky import *
from chomsky.matchers import to_matcher


def test_to_matcher_str():
    assert to_matcher('test') == Literal('test')


def test_to_matcher_literal():
    assert to_matcher(Literal('test')) == Literal('test')


def test_to_matcher_list():
    assert to_matcher(['test']) == Sequence(Literal('test'))


def test_to_matcher_sequence():
    assert to_matcher(Sequence('test')) == Sequence(Literal('test'))
