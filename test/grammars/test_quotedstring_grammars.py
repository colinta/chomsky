from pytest import raises
from chomsky import *


def test_single_quotedstring_repr():
    assert repr(SingleQuotedString("'hi!'")) == 'SingleQuotedString("\'hi!\'")'


def test_triplesingle_quotedstring_repr():
    assert repr(TripleSingleQuotedString("'''hi!'''")) == 'TripleSingleQuotedString("\'\'\'hi!\'\'\'")'


def test_double_quotedstring_repr():
    assert repr(DoubleQuotedString('"hi!"')) == "DoubleQuotedString('\"hi!\"')"


def test_singlequotedstring_grammar():
    matcher = SingleQuotedString("'foo'")
    assert matcher.parsed == "'foo'"
    assert str(matcher) == "'foo'"


def test_doublequotedstring_grammar():
    matcher = DoubleQuotedString('"foo"')
    assert matcher.parsed == '"foo"'
    assert str(matcher) == '"foo"'


def test_singlequotedstring_with_escape_grammar():
    matcher = SingleQuotedString(r"'foo\t\a\b\\'")
    assert matcher.parsed == r"'foo\t\a\b\\'"
    assert str(matcher) == r"'foo\t\a\b\\'"


def test_doublequotedstring_with_escape_grammar():
    matcher = DoubleQuotedString(r'"foo\t\a\b\\"')
    assert matcher.parsed == r'"foo\t\a\b\\"'
    assert str(matcher) == r'"foo\t\a\b\\"'


def test_singlequotedstring_with_newline_grammar():
    matcher = SingleQuotedString("""'foo\\
'""")
    assert matcher.parsed == """'foo\\
'"""
    assert str(matcher) == """'foo\\
'"""


def test_doublequotedstring_with_newline_grammar():
    matcher = DoubleQuotedString('''"foo\\
"''')
    assert matcher.parsed == '''"foo\\
"'''
    assert str(matcher) == '''"foo\\
"'''
