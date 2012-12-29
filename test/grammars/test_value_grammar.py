from pytest import raises
from chomsky import *


def test_integer_value_grammar():
    assert Value('1').parsed == Integer('1')
    assert Value('11323').parsed == Integer('11323')


def test_binary_value_grammar():
    assert Value('0b1').parsed == BinaryInteger('0b1')
    assert Value('0B1').parsed == BinaryInteger('0B1')


def test_octal_value_grammar():
    assert Value('01').parsed == OctalInteger('01')
    assert Value('07314').parsed == OctalInteger('07314')


def test_hexadecimal_value_grammar():
    assert Value('0x1').parsed == HexadecimalInteger('0x1')
    assert Value('0Xabf7314').parsed == HexadecimalInteger('0Xabf7314')


def test_variable_value_grammar():
    assert Value('abcd').parsed == Variable('abcd')
    assert Value('_123').parsed == Variable('_123')


def test_string_value_grammar():
    assert Value('"double"').parsed == DoubleQuotedString('"double"')
    assert Value("'single'").parsed == SingleQuotedString("'single'")
    assert Value(r'"double-escaped\n\""').parsed == DoubleQuotedString(r'"double-escaped\n\""')
    assert Value(r"'single-escaped\n\''").parsed == SingleQuotedString(r"'single-escaped\n\''")
    assert Value(r'"""double-triple"""').parsed == TripleDoubleQuotedString('"""double-triple"""')
    assert Value(r"'''single-triple'''").parsed == TripleSingleQuotedString("'''single-triple'''")
