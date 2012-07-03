from pytest import raises
from chomsky import *


nextisnot_matcher = Optional('-') + NextIsNot('0') + Word('0123546789')


def test_nextisnot_repr():
    assert repr(NextIs(Word('123456789'))) == "NextIs(Word('123456789'))"
    assert repr(NextIs(Word('123456789'), suppress=False)) == "NextIs(Word('123456789'), suppress=False)"
    assert repr(NextIs(Word('123456789'), suppress=True)) == "NextIs(Word('123456789'))"


def test_nextisnot_lengths():
    assert nextisnot_matcher.minimum_length() == 1
    assert nextisnot_matcher.maximum_length() == Infinity


def test_nextisnot_1():
    parsed = nextisnot_matcher('1')
    assert parsed == [[], '1']


def test_nextisnot_2():
    parsed = nextisnot_matcher('-2')
    assert parsed == [['-'], '2']


def test_nextisnot_11():
    parsed = nextisnot_matcher('-11')
    assert parsed == [['-'], '11']


def test_nextisnot_fail():
    with raises(ParseException):
        nextisnot_matcher('-0')
