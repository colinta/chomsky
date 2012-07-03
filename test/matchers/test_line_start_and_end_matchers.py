from pytest import raises
from chomsky import *


def test_string_boundary_repr():
    assert repr(LineStart()) == 'LineStart()'
    assert repr(LineEnd()) == 'LineEnd()'
    assert repr(LineStart(suppress=False)) == 'LineStart(suppress=False)'
    assert repr(LineEnd(suppress=False)) == 'LineEnd(suppress=False)'


def test_start_of_line_matcher():
    matcher = LineStart()
    parsed = matcher('')
    assert parsed == None


def test_start_of_line_and_literal_matcher():
    matcher = S() + LineStart() + L('test')
    parsed = matcher('test')
    assert parsed == ['test']
    parsed = matcher('\ntest')
    assert parsed == ['test']


def test_complicated_line_stuff_matcher():
    matcher = L("start") + S() + LineStart() + S() + L('hi!')
    parsed = matcher("start  \n  hi!")
    assert parsed == ['start', 'hi!']


def test_start_of_line_matcher_fail():
    matcher = L('\ntest') + LineStart()
    with raises(ParseException):
        matcher('test')


def test_end_of_line_matcher():
    matcher = LineEnd()
    parsed = matcher('')
    assert parsed == None


def test_literal_and_end_of_line_matcher():
    matcher = L('test') + LineEnd()
    parsed = matcher('test')
    assert parsed == ['test']
    parsed = matcher('test\n')
    assert parsed == ['test']


def test_end_of_line_and_literal_matcher():
    matcher = L('hi!') + LineEnd()
    parsed = matcher('hi!')
    assert parsed == ['hi!']


def test_end_of_line_matcher_fail():
    matcher = L('test') + LineEnd()
    with raises(ParseException):
        matcher('testtest')
