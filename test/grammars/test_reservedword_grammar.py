from pytest import raises
from chomsky import *


class TestReservedWord(ReservedWord):
    words = ['def']


def test_reservedword_repr():
    assert repr(TestReservedWord('def')) == "TestReservedWord('def')"


def test_pythonreservedword_repr():
    assert repr(PythonReservedWord('def')) == "PythonReservedWord('def')"


def test_phpreservedword_repr():
    assert repr(PhpReservedWord('function')) == "PhpReservedWord('function')"


def test_rubyreservedword_repr():
    assert repr(RubyReservedWord('begin')) == "RubyReservedWord('begin')"


def test_reservedword_type():
    assert isinstance(TestReservedWord('def'), TestReservedWord)


def test_reservedword_grammar_def():
    m = TestReservedWord('def')
    assert m.parsed == 'def'
    assert str(m) == 'def'


def test_pythonreservedword_grammar():
    m = PythonReservedWord('def')
    assert m.parsed == 'def'
    assert str(m) == 'def'


def test_phpreservedword_grammar():
    m = PhpReservedWord('function')
    assert m.parsed == 'function'
    assert str(m) == 'function'


def test_rubyreservedword_grammar():
    m = RubyReservedWord('begin')
    assert m.parsed == 'begin'
    assert str(m) == 'begin'


def test_reservedword_fail():
    with raises(ParseException):
        TestReservedWord('function')
