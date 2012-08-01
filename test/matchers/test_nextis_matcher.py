from pytest import raises
from chomsky import *


nextis_matcher = NextIs(Chars('123456789')) + Chars('1234567890')


def test_nextis_repr():
    assert repr(NextIs(Chars('123456789'))) == "NextIs(Chars('123456789'))"
    assert repr(NextIs(Chars('123456789'), suppress=False)) == "NextIs(Chars('123456789'), suppress=False)"
    assert repr(NextIs(Chars('123456789'), suppress=True)) == "NextIs(Chars('123456789'))"


def test_nextis_lengths():
    assert NextIs(' ').minimum_length() == 0
    assert NextIs(' ').maximum_length() == 0


def test_nextis_1():
    parsed = nextis_matcher('1')
    assert parsed == ['1']


def test_nextis_2():
    parsed = nextis_matcher('2')
    assert parsed == ['2']


def test_nextis_11():
    parsed = nextis_matcher('11')
    assert parsed == ['11']


def test_nextis_fail():
    with raises(ParseException):
        print nextis_matcher('02')
