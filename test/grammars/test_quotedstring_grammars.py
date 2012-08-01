from pytest import raises
from chomsky import *


def test_single_empty_quotedstring_repr():
    assert repr(SingleQuotedString("''")) == 'SingleQuotedString("\'\'")'


def test_single_quotedstring_repr():
    assert repr(SingleQuotedString("'hi!'")) == 'SingleQuotedString("\'hi!\'")'


def test_triplesingle_empty_quotedstring_repr():
    assert repr(TripleSingleQuotedString("''''''")) == "TripleSingleQuotedString(\"''''''\")"


def test_triplesingle_quotedstring_repr():
    assert repr(TripleSingleQuotedString("'''hi!'''")) == "TripleSingleQuotedString(\"'''hi!'''\")"


def test_double_empty_quotedstring_repr():
    assert repr(DoubleQuotedString('""')) == "DoubleQuotedString('\"\"')"


def test_double_quotedstring_repr():
    assert repr(DoubleQuotedString('"hi!"')) == "DoubleQuotedString('\"hi!\"')"


def test_doublesingle_empty_quotedstring_repr():
    assert repr(TripleDoubleQuotedString('""""""')) == 'TripleDoubleQuotedString(\'""""""\')'


def test_doublesingle_quotedstring_repr():
    assert repr(TripleDoubleQuotedString('"""hi!"""')) == 'TripleDoubleQuotedString(\'"""hi!"""\')'


def test_single_quotedstring_grammar():
    matcher = SingleQuotedString("'foo'")
    assert matcher.parsed == "'foo'"
    assert str(matcher) == "'foo'"


def test_double_quotedstring_grammar():
    matcher = DoubleQuotedString('"foo"')
    assert matcher.parsed == '"foo"'
    assert str(matcher) == '"foo"'


def test_single_quotedstring_with_escape_grammar():
    matcher = SingleQuotedString(r"'foo\t\a\b\\'")
    assert matcher.parsed == r"'foo\t\a\b\\'"
    assert str(matcher) == r"'foo\t\a\b\\'"


def test_double_quotedstring_with_escape_grammar():
    matcher = DoubleQuotedString(r'"foo\t\a\b\\"')
    assert matcher.parsed == r'"foo\t\a\b\\"'
    assert str(matcher) == r'"foo\t\a\b\\"'


def test_single_quotedstring_with_newline_grammar():
    matcher = SingleQuotedString("""'foo\\
'""")
    assert matcher.parsed == """'foo\\
'"""
    assert str(matcher) == """'foo\\
'"""


def test_triplesingle_quotedstring_with_newline_grammar():
    matcher = TripleSingleQuotedString("""'''foo\\
'''""")
    assert matcher.parsed == """'''foo\\
'''"""
    assert str(matcher) == """'''foo\\
'''"""


def test_double_quotedstring_with_newline_grammar():
    matcher = DoubleQuotedString('''"foo\\
"''')
    assert matcher.parsed == '''"foo\\
"'''
    assert str(matcher) == '''"foo\\
"'''


def test_tripledouble_quotedstring_with_newline_grammar():
    matcher = TripleDoubleQuotedString('''"""foo\\
"""''')
    assert matcher.parsed == '''"""foo\\
"""'''
    assert str(matcher) == '''"""foo\\
"""'''
