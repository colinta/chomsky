from chomsky import *


def test_matchertest():
    assert Char('abcd').test('e') == False
    assert Char('abcd').test('a') == True
