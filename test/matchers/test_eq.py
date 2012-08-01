from chomsky import *


def test_letter_eq():
    assert Letter('a') == Letter('a')
    assert Letter('a') != Letter('b')
    assert Letter('ab') == Letter('ab')
    assert Letter('ab') != Letter('ba')
    assert Letter('ab', suppress=True) != Letter('ab', suppress=False)
    assert Letter('ab', suppress=True) == Letter('ab', suppress=True)


def test_literal_eq():
    assert Literal('word') == Literal('word')
    assert Literal('word') != Literal('blah')
    assert Literal('word', suppress=True) != Literal('word', suppress=False)
    assert Literal('word', suppress=True) == Literal('word', suppress=True)


def test_word_eq():
    assert Chars('word') == Chars('word')
    assert Chars('word', min=2) == Chars('word', min=2)
    assert Chars('word', min=2) != Chars('word', min=3)
    assert Chars('word', max=2) == Chars('word', max=2)
    assert Chars('word', max=2) != Chars('word', max=3)
    assert Chars('word') != Chars('blah')
    assert Chars('word', suppress=True) != Chars('word', suppress=False)
    assert Chars('word', suppress=True) == Chars('word', suppress=True)


def test_whitespace_eq():
    assert Whitespace('  ') == Whitespace('  ')
    assert Whitespace('  ') != Whitespace("\t\t")
    assert Whitespace('  ', suppress=True) != Whitespace('  ', suppress=False)
    assert Whitespace('  ', suppress=True) == Whitespace('  ', suppress=True)


def test_regex_eq():
    assert Regex('[a-z]') == Regex('[a-z]')
    assert Regex('[a-z]', group=1) == Regex('[a-z]', group=1)
    assert Regex('[a-z]', group=1) != Regex('[a-z]', group=2)
    assert Regex('[a-z]') == Regex('[a-z]')
    assert Regex('[a-z]', advance=1) == Regex('[a-z]', advance=1)
    assert Regex('[a-z]', advance=1) != Regex('[a-z]', advance=2)
    assert Regex('[a-z]') != Regex("[A-Z]")
    assert Regex('[a-z]', suppress=True) != Regex('[a-z]', suppress=False)
    assert Regex('[a-z]', suppress=True) == Regex('[a-z]', suppress=True)
