from .buffer import Buffer
from .exceptions import ParseException
from .matchers import Matcher, AutoSequence, to_matcher


class GrammarMeta(type):
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

            grammar = cls_dict['grammar']
            if not isinstance(grammar, Matcher):
                grammar = to_matcher(grammar)
            if not isinstance(grammar, AutoSequence):
                grammar = AutoSequence(grammar)
            cls_dict['grammar'] = grammar
        return super(GrammarMeta, meta).__new__(meta, classname, bases, cls_dict)


class Grammar(object):
    __metaclass__ = GrammarMeta

    def __init__(self, parseme):
        self.buffer = Buffer(parseme)
        self.parsed = self.grammar.consume(self.buffer)

    @classmethod
    def consume(cls, buffer):
        raise NotImplementedError('Grammar.consume()')

    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= len(self.parsed):
                raise ParseException(
                    'Unexpected StringEnd at {self.position}'.format(self=self),
                    buffer)
            return self.parsed[key]

    def __repr__(self):
        return '{type.__name__}({self.parsed!r})'.format(self=self, type=type(self))
