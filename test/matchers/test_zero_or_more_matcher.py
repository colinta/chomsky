from woodpyle import *


zero_matcher = ZeroOrMore(Literal('zero'))


def test_zero_zeroormore():
    parsed = zero_matcher('')
    assert isinstance(parsed, ResultList)
    assert parsed == []


def test_zero2_zeroormore():
    parsed = zero_matcher('foo')
    assert isinstance(parsed, ResultList)
    assert parsed == []


def test_one_zeroormore():
    parsed = zero_matcher('zero')
    assert isinstance(parsed, ResultList)
    assert parsed == ['zero']


def test_two_zeroormore():
    parsed = zero_matcher('zerozero')
    assert isinstance(parsed, ResultList)
    assert parsed == ['zero', 'zero']


zero_with_words_matcher = Literal('pre-') + ZeroOrMore(Literal('nada')) + Literal('-post')


def test_zero_zeroormore_with_words():
    parsed = zero_with_words_matcher('pre--post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == []


def test_one_zeroormore_with_words():
    parsed = zero_with_words_matcher('pre-nada-post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == ['nada']


def test_two_zeroormore_with_words():
    parsed = zero_with_words_matcher('pre-nadanada-post')
    assert isinstance(parsed, ResultList)
    assert parsed[0] == 'pre-'
    assert parsed[2] == '-post'
    assert parsed[1] == ['nada', 'nada']
