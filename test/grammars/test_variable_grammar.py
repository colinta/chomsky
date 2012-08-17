from pytest import raises
from chomsky import *


class TestDollarVariable(Variable):
    starts_with = Chars('$')


def test_variable_repr():
    assert repr(Variable('abcd')) == "Variable('abcd')"


def test_pythonvariable_repr():
    assert repr(PythonVariable('abcd')) == "PythonVariable('abcd')"


def test_phpvariable_repr():
    assert repr(PhpVariable('$abcd')) == "PhpVariable('$abcd')"


def test_rubyvariable_repr():
    assert repr(RubyVariable('abcd')) == "RubyVariable('abcd')"


def test_variable_type():
    assert isinstance(Variable('abcd'), Variable)


def test_pythonvariable_type():
    assert isinstance(PythonVariable('abcd'), PythonVariable)


def test_phpvariable_type():
    assert isinstance(PhpVariable('$abcd'), PhpVariable)


def test_rubyvariable_type():
    assert isinstance(RubyVariable('abcd'), RubyVariable)


def test_variable_grammar_abcd():
    m = Variable('abcd')
    assert m.parsed == 'abcd'
    assert str(m) == 'abcd'


def test_pythonvariable_grammar_abcd():
    m = PythonVariable('abcd')
    assert m.parsed == 'abcd'
    assert str(m) == 'abcd'


def test_phpvariable_grammar_abcd():
    m = PhpVariable('$abcd')
    assert m.parsed == '$abcd'
    assert str(m) == '$abcd'


def test_rubyvariable_grammar_abcd():
    m = RubyVariable('abcd')
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
    m = TestDollarVariable('$abcd_123_')
    assert m.parsed == '$abcd_123_'
    assert str(m) == '$abcd_123_'


def test_variable_fail_digits():
    with raises(ParseException):
        print Variable('123')


def test_variable_fail_starts_with():
    with raises(ParseException):
        print TestDollarVariable('_abc')


def test_pythonvariable_fail_reserved():
    with raises(ParseException):
        print PythonVariable('def')


def test_phpvariable_fail_reserved():
    with raises(ParseException):
        print PhpVariable('function')


def test_phpvariable_fail_nodollar():
    with raises(ParseException):
        print PhpVariable('valid_name')


def test_rubyvariable_fail_reserved():
    with raises(ParseException):
        print RubyVariable('def')
