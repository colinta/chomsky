from pytest import raises
from chomsky import *


any_matcher = Any(Literal('Joey'), Literal('Bob'), Literal('Billy'))
autoany_matcher = Literal('Joey') | Literal('Bob') | Literal('Billy')


def test_any_repr():
    assert repr(Any(Literal('Joey'), Literal('Bob'), Literal('Billy'))) == "Any(Literal('Joey'), Literal('Bob'), Literal('Billy'))"
    assert repr(Any(Literal('Joey'), Literal('Bob'), Literal('Billy'), suppress=False)) == "Any(Literal('Joey'), Literal('Bob'), Literal('Billy'))"
    assert repr(Any(Literal('Joey'), Literal('Bob'), Literal('Billy'), suppress=True)) == "Any(Literal('Joey'), Literal('Bob'), Literal('Billy'), suppress=True)"


def test_autoany_repr():
    assert repr(Literal('Joey') | Literal('Bob') | Literal('Billy')) == "Any(Literal('Joey') | Literal('Bob') | Literal('Billy'))"
    assert repr('Joey' | Literal('Bob') | Literal('Billy')) == "Any(Literal('Joey') | Literal('Bob') | Literal('Billy'))"
    assert repr(Literal('Joey') | Literal('Bob') | 'Billy') == "Any(Literal('Joey') | Literal('Bob') | Literal('Billy'))"
    assert repr(Literal('Joey') | 'Bob' | Literal('Billy')) == "Any(Literal('Joey') | Literal('Bob') | Literal('Billy'))"
    assert repr('Joey' | Literal('Bob') | 'Billy') == "Any(Literal('Joey') | Literal('Bob') | Literal('Billy'))"


def test_any_lengths():
    assert any_matcher.minimum_length() == 3
    assert any_matcher.maximum_length() == 5


def test_any():
    for name in ['Joey', 'Bob', 'Billy']:
        parsed = any_matcher(name)
        assert parsed == name


def test_any_same_char():
    for char in ['***', '**', '*']:
        parsed = Any(Literal('***'), Literal('**'), Literal('*'))(char)
        assert parsed == char


def test_autoany():
    for name in ['Joey', 'Bob', 'Billy']:
        parsed = autoany_matcher(name)
        assert parsed == name


def test_any_fail():
    with raises(ParseException):
        print any_matcher('bahhumbug')
