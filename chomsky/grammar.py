import string
from .buffer import Buffer
from .exceptions import ParseException
from .matchers import *


class GrammarType(type):
    def __new__(meta, classname, bases, cls_dict):
        cls = super(GrammarType, meta).__new__(meta, classname, bases, cls_dict)
        cls.suppress = False
        return cls

    def rollback(cls, *args, **kwargs):
        return cls.grammar.rollback(*args, **kwargs)

    def minimum_length(cls, *args, **kwargs):
        return cls.grammar.minimum_length(*args, **kwargs)

    def maximum_length(cls, *args, **kwargs):
        return cls.grammar.maximum_length(*args, **kwargs)

    def consume(cls, buffer):
        return cls.grammar.consume(buffer)

    def __repr__(cls):
        return cls.__name__


class Grammar(object):
    """
    Note: There is a common need to have invalid versions of an otherwise simple
    grammar.  Take HexadecimalInteger:

        grammar = Group(Optional('-') + ('0x' | '0X') + Chars('01234567890abcdefABCDEF'))

    Easy enough, but now we get the bogus match "-0x0000".  Instead of writing a
    complicated matcher, we can just use the `bad_grammar` feature.  Any matches
    that match the bad_grammar are ParseExceptions.  The bad_grammar must match
    the entire result (StringStart() and StringEnd() tokens are added to the
    matcher automatically)

        grammar = Group(Optional('-') + ('0x' | '0X') + Chars('01234567890abcdefABCDEF'))
        bad_grammar = '-0' + Letter('xX')' + Letter('0')  # won't match -0x0000
    """
    __metaclass__ = GrammarType

    bad_grammar = None
    grammar = None

    def __init__(self, parseme=None):
        self.buffer = Buffer(parseme)
        self.parsed = self.grammar.consume(Buffer(parseme))
        if self.bad_grammar:
            try:
                buffer = Buffer(str(self.parsed))
                (StringStart() + self.bad_grammar + StringEnd()).consume(buffer)
            except ParseException:
                pass
            else:
                raise ParseException("Invalid match {parseme!r} in {self!r}".format(parseme=parseme, self=self), buffer)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.parsed[key]

    def __repr__(self):
        return '{type.__name__}({buffer!r})'.format(self=self, buffer=str(self.buffer), type=type(self))

    def __str__(self):
        return str(self.parsed)


class Integer(Grammar):
    grammar = Group('0' | (Optional('-') + NextIsNot('0') + Chars(string.digits)))
Int = Integer


class BinaryInteger(Grammar):
    grammar = Group(Optional('-') + '0' + Letter('bB') + Chars('01'))
    bad_grammar = '-0' + Letter('bB') + Chars('0')
Binary = BinaryInteger


class OctalInteger(Grammar):
    grammar = Group(Optional('-') + '0' + Optional(Letter('oO')) + Chars('01234567'))
    bad_grammar = '-0' + Optional(Letter('oO')) + Chars('0')
Octal = OctalInteger


class HexadecimalInteger(Grammar):
    grammar = Group(Optional('-') + '0' + Letter('xX') + Chars('01234567890abcdefABCDEF'))
    bad_grammar = '-0' + Letter('xX') + Chars('0')
Hex = HexadecimalInteger


class OperatorGrammarType(GrammarType):
    def __new__(meta, classname, bases, cls_dict):
        cls = super(OperatorGrammarType, meta).__new__(meta, classname, bases, cls_dict)
        if not cls.grammar:
            cls.grammar = Any(*cls_dict['operators'])
        return cls


class Operator(Grammar):
    __metaclass__ = OperatorGrammarType
    operators = list('+-/*%<>') + ['==', '!=', '&&', '||'] + list('&|')
Op = Operator


class ReservedWordGrammarType(GrammarType):
    def __new__(meta, classname, bases, cls_dict):
        cls = super(ReservedWordGrammarType, meta).__new__(meta, classname, bases, cls_dict)
        if cls_dict['words']:
            cls.grammar = Any(*cls_dict.pop('words'))
        return cls


class ReservedWord(Grammar):
    __metaclass__ = ReservedWordGrammarType
    words = None

    def __repr__(self):
        args = ""
        if self.words != type(self).words:
            args = ", words={self.words!r}".format(self=self)
        return '{type.__name__}({buffer!r}{args})'.format(self=self, buffer=str(self.buffer), type=type(self), args=args)


class PythonReservedWord(ReservedWord):
    words = [
        'and',       'del',       'from',      'not',       'while',
        'as',        'elif',      'global',    'or',        'with',
        'assert',    'else',      'if',        'pass',      'yield',
        'break',     'except',    'import',    'print',
        'class',     'exec',      'in',        'raise',
        'continue',  'finally',   'is',        'return',
        'def',       'for',       'lambda',    'try',
        ]


class PhpReservedWord(ReservedWord):
    words = [
    '__halt_compiler', 'abstract',   'and',        'array',        'as',
    'break',           'callable',   'case',       'catch',        'class',
    'clone',           'const',      'continue',   'declare',      'default',
    'die',             'do',         'echo',       'else',         'elseif',
    'empty',           'enddeclare', 'endfor',     'endforeach',   'endif',
    'endswitch',       'endwhile',   'eval',       'exit',         'extends',
    'final',           'for',        'foreach',    'function',     'global',
    'goto',            'if',         'implements', 'include',      'include_once',
    'instanceof',      'insteadof',  'interface',  'isset',        'list',
    'namespace',       'new',        'or',         'print',        'private',
    'protected',       'public',     'require',    'require_once', 'return',
    'static',          'switch',     'throw',      'trait',        'try',
    'unset',           'use',        'var',        'while',        'xor',
    ]


class RubyReservedWord(ReservedWord):
    words = [
    'alias',  'and',    'BEGIN', 'begin', 'break', 'case',   'class',  'def',    'defined?',
    'do',     'else',   'elsif', 'END',   'end',   'ensure', 'false',  'for',    'if',
    'in',     'module', 'next',  'nil',   'not',   'or',     'redo',   'rescue', 'retry',
    'return', 'self',   'super', 'then',  'true',  'undef',  'unless', 'until',  'when',
    'while',  'yield',
    ]


class VariableGrammarType(GrammarType):
    def __new__(meta, classname, bases, cls_dict):
        cls = super(VariableGrammarType, meta).__new__(meta, classname, bases, cls_dict)
        starts_with = cls_dict.get('starts_with', cls.starts_with)
        ends_with = cls_dict.get('ends_with', cls.ends_with)
        cls.grammar = Group(starts_with + ends_with)
        return cls


class Variable(Grammar):
    __metaclass__ = VariableGrammarType
    starts_with = Letter(string.ascii_letters + '_')
    ends_with = Chars(string.ascii_letters + '_' + string.digits, min=0)
Var = Variable


class PythonVariable(Variable):
    bad_grammar = PythonReservedWord


class PhpVariable(Variable):
    bad_grammar = PhpReservedWord


class RubyVariable(Variable):
    bad_grammar = RubyReservedWord
