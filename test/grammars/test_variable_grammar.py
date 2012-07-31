from pytest import raises
from chomsky import *


def test_variable_repr():
    assert repr(Variable('abcd')) == "Variable('abcd')"


def test_variable_type():
    assert isinstance(Variable('abcd'), Variable)


def test_variable_grammar_abcd():
    m = Variable('abcd')
    assert m.parsed == 'abcd'
    assert str(m) == 'abcd'


def test_variable_grammar_underscore():
    m = Variable('_abcd')
    assert m.parsed == '_abcd'
    assert str(m) == '_abcd'


def test_variable_grammar_alphanumeric():
    m = Variable('abcd123')
    assert m.parsed == 'abcd123'
    assert str(m) == 'abcd123'


def test_variable_grammar_all():
    m = Variable('_abcd_123_')
    assert m.parsed == '_abcd_123_'
    assert str(m) == '_abcd_123_'


def test_variable_starts_with():
    m = Variable('$abcd_123_', starts_with=Word('$'))
    assert m.parsed == '$abcd_123_'
    assert str(m) == '$abcd_123_'


def test_variable_fail_digits():
    with raises(ParseException):
        print Variable('123')


def test_variable_fail_starts_with():
    with raises(ParseException):
        print Variable('_abc', starts_with=Word('abcdefg'))
