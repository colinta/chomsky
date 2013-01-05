# from pytest import raises
from chomsky import *


class ExclamationGrammar(Grammar):
    '''
    Consumes any number of exclamation marks
    '''
    def consume(self, buffer):
        self.parsed = ''
        while buffer and buffer[0] == '!':
            self.parsed += '!'
            buffer.advance(1)


class CustomGrammar(Grammar):
    grammar = Integer + ExclamationGrammar


def test_custom_grammar():
    m = CustomGrammar('12345!!!!!b')
    assert m.parsed == [Integer('12345'), ExclamationGrammar('!!!!!')]
    assert str(m) == '12345!!!!!'
