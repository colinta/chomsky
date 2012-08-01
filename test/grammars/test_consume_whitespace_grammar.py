from pytest import raises
from chomsky import *


def test_binary_grammar_0b0():
    m = BinaryInteger('  0b0  ')
    assert m.parsed == '0b0'
    assert str(m) == '0b0'
