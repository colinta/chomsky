from chomsky import *


zero_matcher = ZeroOrMore(Literal('zero'))


def test_zeroormore_repr():
    assert repr(ZeroOrMore(Literal('zero'))) == "ZeroOrMore(Literal('zero'))"
    assert repr(ZeroOrMore(Literal('zero'), suppress=False)) == "ZeroOrMore(Literal('zero'))"
    assert repr(ZeroOrMore(Literal('zero'), suppress=True)) == "ZeroOrMore(Literal('zero'), suppress=True)"
    assert repr(ZeroOrMore(Literal(u'zero'), suppress=True)) == "ZeroOrMore(Literal(u'zero'), suppress=True)"


def test_zero_zeroormore():
    parsed = zero_matcher('')
    assert parsed == []


def test_zero2_zeroormore():
    parsed = zero_matcher('foo')
    assert parsed == []


def test_one_zeroormore():
    parsed = zero_matcher('zero')
    assert parsed == ['zero']


def test_two_zeroormore():
    parsed = zero_matcher('zerozero')
    assert parsed == ['zero', 'zero']


zero_with_words_matcher = Literal('pre-') + ZeroOrMore(Literal('nada')) + Literal('-post')


def test_zero_zeroormore_with_words():
    parsed = zero_with_words_matcher('pre--post')
    assert parsed == ['pre-', [], '-post']


def test_one_zeroormore_with_words():
    parsed = zero_with_words_matcher('pre-nada-post')
    assert parsed == ['pre-', ['nada'], '-post']


def test_two_zeroormore_with_words():
    parsed = zero_with_words_matcher('pre-nadanada-post')
    assert parsed == ['pre-', ['nada', 'nada'], '-post']
