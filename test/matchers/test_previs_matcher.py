from pytest import raises
from chomsky import *


previs_matcher = Chars('123456789.') + PrevIs('.') + Chars('1234567890')


def test_previs_repr():
    assert repr(PrevIs(Chars('123456789'))) == "PrevIs(Chars('123456789'))"
    assert repr(PrevIs(' ')) == "PrevIs(Literal(' '))"
    assert repr(PrevIs(Chars('123456789'), suppress=False)) == "PrevIs(Chars('123456789'), suppress=False)"
    assert repr(PrevIs(Chars('123456789'), suppress=True)) == "PrevIs(Chars('123456789'))"


def test_previs_lengths():
    assert PrevIs('.').minimum_length() == 0
    assert PrevIs('.').maximum_length() == 0


def test_previs_1():
    parsed = previs_matcher('1.2')
    assert parsed == ['1.', '2']


def test_previs_2():
    parsed = previs_matcher('3.4')
    assert parsed == ['3.', '4']


def test_previs_11():
    parsed = previs_matcher('55.66')
    assert parsed == ['55.', '66']


def test_previs_11_22():
    parsed = previs_matcher('11.22.33')
    assert parsed == ['11.22.', '33']


def test_previs_fail():
    with raises(ParseException):
        print previs_matcher('1122')
