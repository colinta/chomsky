from pytest import raises
from chomsky import *


def test_start_of_string_matcher():
    matcher = StringStart()
    parsed = matcher('')
    assert parsed == None


def test_start_of_string_and_literal_matcher():
    matcher = StringStart() + L('hi!')
    parsed = matcher('hi!')
    assert parsed == ['hi!']


def test_start_of_string_matcher_fail():
    matcher = L('test') + StringStart()
    with raises(ParseException):
        matcher('test')


def test_end_of_string_matcher():
    matcher = StringEnd()
    parsed = matcher('')
    assert parsed == None


def test_end_of_string_and_literal_matcher():
    matcher = L('hi!') + StringEnd()
    parsed = matcher('hi!')
    assert parsed == ['hi!']


def test_end_of_string_matcher_fail():
    matcher = StringEnd()
    with raises(ParseException):
        matcher('test')
