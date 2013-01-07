from chomsky import *


def test_integer_number_grammar():
    assert Number('1').parsed == Integer('1')
    assert Number('11323').parsed == Integer('11323')


def test_float_number_grammar():
    assert Number('1.321').parsed == Float('1.321')
    assert Number('11323.321').parsed == Float('11323.321')
    assert Number('-1.321').parsed == Float('-1.321')
    assert Number('-0.321').parsed == Float('-0.321')


def test_binary_number_grammar():
    assert Number('0b1').parsed == BinaryInteger('0b1')
    assert Number('0B1').parsed == BinaryInteger('0B1')


def test_octal_number_grammar():
    assert Number('01').parsed == OctalInteger('01')
    assert Number('07314').parsed == OctalInteger('07314')


def test_hexadecimal_number_grammar():
    assert Number('0x1').parsed == HexadecimalInteger('0x1')
    assert Number('0Xabf7314').parsed == HexadecimalInteger('0Xabf7314')
