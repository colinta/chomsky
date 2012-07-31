from pytest import raises
from chomsky import *


def test_escapeseq_repr():
    assert repr(EscapeSequence('\\\"')) == "EscapeSequence('\\\\\"')"


def test_escapeseq_grammar():
    for c in 'nrtabfv\'\"\n\\':
        print repr(c)
        m = EscapeSequence('\\' + c)
        assert m.parsed == '\\' + c
        assert str(m) == '\\' + c


def test_escapeseq_fail():
    with raises(ParseException):
        print EscapeSequence('\\G')
