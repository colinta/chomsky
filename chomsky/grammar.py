import string
from .buffer import Buffer
from .exceptions import ParseException
from .matchers import *


class Grammar(object):
    """
    Note: There is a common need to have invalid versions of an otherwise simple
    grammar.  Take HexadecimalInteger:

        grammar = Group(Optional('-') + ('0x' | '0X') + Word('01234567890abcdefABCDEF'))

    Easy enough, but now we get the bogus match "-0x0000".  Instead of writing a
    complicated matcher, we can just use the `bad_grammar` feature.  Any matches
    that match the bad_grammar are ParseExceptions.  The bad_grammar must match
    the entire result (StringStart() and StringEnd() tokens are added to the
    matcher automatically)

        grammar = Group(Optional('-') + ('0x' | '0X') + Word('01234567890abcdefABCDEF'))
        bad_grammar = '-0' + Letter('xX')' + Letter('0')  # won't match -0x0000
    """
    bad_grammar = None
    # grammar = None

    def __init__(self, parseme=None):
        self.buffer = Buffer(parseme)
        self.parsed = self.consume(self.buffer)

    def consume(self, buffer):
        ret = self.grammar.consume(buffer)
        if self.bad_grammar:
            try:
                buffer = Buffer(ret)
                (StringStart() + self.bad_grammar + StringEnd()).consume(buffer)
            except ParseException:
                pass
            else:
                raise ParseException("Invalid match {ret!r} in {self!r}".format(ret=ret, self=self), buffer)
        return ret

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.parsed[key]

    def __repr__(self):
        return '{type.__name__}({buffer!r})'.format(self=self, buffer=str(self.buffer), type=type(self))

    def __str__(self):
        return str(self.parsed)


class Integer(Grammar):
    grammar = Group('0' | (Optional('-') + NextIsNot('0') + Word(string.digits)))


class BinaryInteger(Grammar):
    grammar = Group(Optional('-') + '0' + Letter('bB') + Word('01'))
    bad_grammar = '-0' + Letter('bB') + Word('0')


class OctalInteger(Grammar):
    grammar = Group(Optional('-') + '0' + Optional(Letter('oO')) + Word('01234567'))
    bad_grammar = '-0' + Optional(Letter('oO')) + Word('0')


class HexadecimalInteger(Grammar):
    grammar = Group(Optional('-') + '0' + Letter('xX') + Word('01234567890abcdefABCDEF'))
    bad_grammar = '-0' + Letter('xX') + Word('0')


class Operator(Grammar):
    operators = list('+-/*%<>') + ['==', '!=', '&&', '||'] + list('&|')

    def __init__(self, *args, **kwargs):
        self.operators = kwargs.pop('operators', type(self).operators)
        if not hasattr(self, 'grammar'):
            self.grammar = Any(*self.operators)
        super(Operator, self).__init__(*args, **kwargs)


class Variable(Grammar):
    starts_with = Letter(string.ascii_letters + '_')
    ends_with = Word(string.ascii_letters + '_' + string.digits, min=0)

    def __init__(self, *args, **kwargs):
        self.starts_with = kwargs.pop('starts_with', type(self).starts_with)
        self.ends_with = kwargs.pop('ends_with', type(self).ends_with)
        if not hasattr(self, 'grammar'):
            self.grammar = Group(self.starts_with + self.ends_with)
        super(Variable, self).__init__(*args, **kwargs)
