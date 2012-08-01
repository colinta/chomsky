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


def test_escapeseq_fail():
    with raises(ParseException):
        print EscapeSequence('\\G')
