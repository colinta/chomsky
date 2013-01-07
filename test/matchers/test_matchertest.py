from chomsky import *


def test_matchertest():
    assert Char('abcd').test('e') == False
    assert Char('abcd').test('a') == True


def test_matchertest_mark():
    buffer = Buffer('abcde')
    matcher = Char('abcd')
    assert matcher.test(buffer)
    assert buffer.position == 0
