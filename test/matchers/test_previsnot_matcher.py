from pytest import raises
from chomsky import *


previsnot_matcher = Word('0123546789.') + PrevIsNot('.') + Word('0123546789')


def test_previsnot_repr():
    assert repr(PrevIsNot(Word('123456789'))) == "PrevIsNot(Word('123456789'))"
    assert repr(PrevIsNot(Word('123456789'), suppress=False)) == "PrevIsNot(Word('123456789'), suppress=False)"
    assert repr(PrevIsNot(Word('123456789'), suppress=True)) == "PrevIsNot(Word('123456789'))"


def test_previsnot_lengths():
    assert PrevIsNot(' ').minimum_length() == 0
    assert PrevIsNot(' ').maximum_length() == 0


def test_previsnot_0():
    parsed = previsnot_matcher('00')
    assert parsed == ['0', '0']


def test_previsnot_1():
    parsed = previsnot_matcher('1.22')
    assert parsed == ['1.2', '2']


def test_previsnot_2():
    parsed = previsnot_matcher('3.44')
    assert parsed == ['3.4', '4']


def test_previsnot_11():
    parsed = previsnot_matcher('55.66')
    assert parsed == ['55.6', '6']


def test_previsnot_fail():
    with raises(ParseException):
        print previsnot_matcher('7.7')
