from chomsky import *


def test_word_rollback():
    matcher = Chars('abc') + Literal('c') + Chars('de')
    parsed = matcher('baced')
    assert parsed == ['ba', 'c', 'ed']


def test_multi_rollback():
    matcher = Whitespace() + ' ' + Whitespace() + ' ' + Whitespace()
    p = ' \n \t \n '
    parsed = matcher(p)
    assert parsed == [' ', ' ']
