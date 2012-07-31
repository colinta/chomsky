import string
from .buffer import Buffer
from .exceptions import ParseException
from .matchers import *


class GrammarType(type):
    """
    Ensures that Grammar classes are well-formed:

    - have a `grammar` property, and
    - that `grammar` property is a Matcher.  If it is not a Matcher, use
      `to_matcher` to make it one
    """
    def __new__(meta, classname, bases, cls_dict):
        if classname != 'Grammar':
            if 'grammar' not in cls_dict:
                raise TypeError('grammar is required in {classname}'.format(**locals()))

            cls_dict['grammar'] = to_matcher(cls_dict['grammar'])
        return super(GrammarType, meta).__new__(meta, classname, bases, cls_dict)

    def __repr__(cls):
        return cls.__name__

    def consume(cls, buffer):
        raise NotImplementedError('GrammarType.consume()')


class Grammar(object):
    __metaclass__ = GrammarType

    def __init__(self, parseme=None):
        self.buffer = Buffer(parseme)
        self.parsed = self.grammar.consume(self.buffer)

    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= len(self.parsed):
                raise ParseException(
                    'Unexpected StringEnd at {self.position}'.format(self=self),
                    buffer)
            return self.parsed[key]

    def __repr__(self):
        return '{type.__name__}({buffer!r})'.format(self=self, buffer=str(self.buffer), type=type(self))

    def __str__(self):
        return str(self.parsed)


class Integer(Grammar):
    grammar = ('0' | (Optional('-') + NextIsNot('0') + Word(string.digits)))
