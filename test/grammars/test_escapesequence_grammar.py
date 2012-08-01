from pytest import raises
from chomsky import *


def test_escapesequence_repr():
    assert repr(EscapeSequence('\\\"')) == "EscapeSequence('\\\\\"')"


def test_escapesequence_grammar():
    for c in 'nrtabfv\'\"\n\r\\':
        print repr(c)
        m = EscapeSequence('\\' + c)
        assert m.parsed == '\\' + c
        assert str(m) == '\\' + c


def test_escapesequence_unicode_grammar():
    m = EscapeSequence('\\u12ab')
    assert m.parsed == '\\u12ab'
    assert str(m) == '\\u12ab'


def test_escapesequence_fail():
    with raises(ParseException):
        print EscapeSequence('\\G')
