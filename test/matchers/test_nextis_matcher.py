from pytest import raises
from chomsky import *


nextis_matcher = Optional('-') + NextIs(Word('123456789')) + Word('1234567890')


def test_nextis_repr():
    assert repr(NextIs(Word('123456789'))) == "NextIs(Word('123456789'))"
    assert repr(NextIs(Word('123456789'), suppress=False)) == "NextIs(Word('123456789'), suppress=False)"
    assert repr(NextIs(Word('123456789'), suppress=True)) == "NextIs(Word('123456789'))"


def test_nextis_lengths():
    assert nextis_matcher.minimum_length() == 1
    assert nextis_matcher.maximum_length() == Infinity


def test_nextis_1():
    parsed = nextis_matcher('1')
    assert parsed == [[], '1']


def test_nextis_2():
    parsed = nextis_matcher('-2')
    assert parsed == [['-'], '2']


def test_nextis_11():
    parsed = nextis_matcher('-11')
    assert parsed == [['-'], '11']


def test_nextis_fail():
    with raises(ParseException):
        nextis_matcher('-0')
