from chomsky import *


class LaterTest(Grammar):
    grammar = '(' + Later('LaterTest') + ')' | 'foo'


def test_recur_repr0():
    assert repr(LaterTest('foo')) == "LaterTest('foo')"


def test_recur_repr1():
    assert repr(LaterTest('(foo)')) == "LaterTest('(foo)')"


def test_recur_repr2():
    assert repr(LaterTest('((foo))')) == "LaterTest('((foo))')"
