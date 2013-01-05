# from pytest import raises
from chomsky import *


def test_separatedby_repr():
    matcher = SeparatedBy(',', Chars('aeiou'))
    assert repr(matcher) == "SeparatedBy(Literal(',', suppress=True), Chars('aeiou'))"


def test_two_separatedby():
    matcher = SeparatedBy(',', Chars('aeiou'))
    parsed = matcher('aeiou,uoiea')
    assert parsed == ['aeiou', 'uoiea']


def test_four_separatedby():
    matcher = SeparatedBy(',', Chars('aeiou'))
    parsed = matcher('aeiou,uoiea,aaiieeouu,eeeee')
    assert parsed == ['aeiou', 'uoiea', 'aaiieeouu', 'eeeee']
