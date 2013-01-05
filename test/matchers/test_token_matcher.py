# from pytest import raises
from chomsky import *


def test_token_repr():
    matcher = Token(Chars('aeiou'))
    assert repr(matcher) == "Token(Chars('aeiou'))"


def test_token():
    matcher = Token(Chars('aeiou'))
    parsed = matcher('   aeiou   ')
    assert parsed == 'aeiou'


def test_two_tokens():
    matcher = Token(Chars('aeiou')) + Token(Chars('vwxyz'))
    parsed = matcher('aeiou  zyxwv')
    assert parsed == ['aeiou', 'zyxwv']


def test_two_tokens_nospace_fail():
    matcher = Token(Chars('aeiou')) + Token(Chars('vwxyz'))
    parsed = matcher('aeiouzyxwv')
    assert parsed == ['aeiou', 'zyxwv']
