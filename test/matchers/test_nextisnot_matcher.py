from pytest import raises
from chomsky import *


nextisnot_matcher = Optional('-') + NextIsNot('0') + Chars('0123546789')


def test_nextisnot_repr():
    assert repr(NextIsNot(Chars('123456789'))) == "NextIsNot(Chars('123456789'))"
    assert repr(NextIsNot(Chars('123456789'), suppress=False)) == "NextIsNot(Chars('123456789'), suppress=False)"
    assert repr(NextIsNot(Chars('123456789'), suppress=True)) == "NextIsNot(Chars('123456789'))"


def test_nextisnot_lengths():
    assert NextIsNot(' ').minimum_length() == 0
    assert NextIsNot(' ').maximum_length() == 0


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
