from chomsky import *


class RecurTest(Grammar):
    grammar = '(' + Recur('RecurTest') + ')' | 'foo'


def test_recur_repr0():
    assert repr(RecurTest('foo')) == "RecurTest('foo')"


def test_recur_repr1():
    assert repr(RecurTest('(foo)')) == "RecurTest('(foo)')"


def test_recur_repr2():
    assert repr(RecurTest('((foo))')) == "RecurTest('((foo))')"
