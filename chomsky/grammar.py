import string
import re

from .buffer import Buffer
from .exceptions import ParseException
from .matchers import *


class Grammar(object, metaclass=GrammarType):
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
        bad_grammar = '-0' + Char('xX')' + Char('0')  # won't match -0x0000
    """

    bad_grammar = None
    grammar = None

    def __init__(self, parseme=None):
        '''
        In custom Grammar classes, it is "safe" to define a `consume` method.
        It will be renamed to 'consume_grammar', though, so calling
        `super(CustomGrammar, self).consume(buffer)` will fail.

        The reason is that the `GrammarType.consume` method is the method
        that must be called during parsing, but *I* *preferred* custom
        consuming in a Grammar class to be done the same way as a Matcher
        class - by defining a `consume` method.
        '''
        # short-circuit the usual parsing method
        if isinstance(parseme, Grammar) or isinstance(parseme, Matcher) or isinstance(parseme, list):
            if isinstance(parseme, list) and not isinstance(parseme, ResultList):
                parseme = ResultList(parseme)
            self.parsed = parseme
        else:
            if isinstance(parseme, Buffer):
                self.buffer = parseme
            else:
                self.buffer = Buffer(parseme)

            if not hasattr(self, 'parsed'):
                self.parsed = None

            self.parsed = self.consume_grammar(self.buffer)

    def consume_grammar(self, buffer):
        cls = type(self)
        try:
            parsed = cls.grammar.consume(buffer)
        except ParseException:
            if cls.ignore_whitespace:
                cls.whitespace.consume(buffer)
                parsed = cls.grammar.consume(buffer)
            else:
                raise

        if self.bad_grammar:
            try:
                buffer = Buffer(parsed)
                bad_matcher = StringStart() + self.bad_grammar + StringEnd()
                bad_matcher.consume(buffer)
            except ParseException:
                pass
            else:
                raise ParseException("Invalid match {buffer!r} in {self!r}".format(buffer=buffer, self=self))
        return parsed

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.parsed[key]
        return super(Grammar, self).__getitem__(key)

    def __len__(self):
        return len(self.parsed)

    def __add__(self, other):
        return [self, other]

    def __radd__(self, other):
        if isinstance(other, list):
            return [other] + [self]

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, Grammar):
            type_check = isinstance(other, type(self)) or isinstance(self, type(other))
            return type_check and self.parsed == other.parsed
        return self.parsed == other

    def __repr__(self):
        try:
            insides = self.parsed
        except AttributeError:
            insides = self.buffer

        return '{type.__name__}({insides!r})'.format(self=self, insides=str(insides), type=type(self))

    def __str__(self):
        return str(self.parsed)


class Integer(Grammar):
    grammar = Group(('0' | (Optional('-') + NextIsNot('0') + Chars(string.digits))) + NextIsNot(Char(string.digits + string.ascii_letters)))
Int = Integer


class Float(Grammar):
    grammar = Group((((Integer + '.') | '-0.') + Chars(string.digits)) + NextIsNot(Char(string.digits + string.ascii_letters)))
    bad_grammar = '-0' + Char('.') + Chars('0')


class BinaryInteger(Grammar):
    grammar = Group((Optional('-') + '0' + Char('bB') + Chars('01')) + NextIsNot(Char(string.digits + string.ascii_letters)))
    bad_grammar = '-0' + Char('bB') + Chars('0')
Binary = BinaryInteger


class OctalInteger(Grammar):
    grammar = Group((Optional('-') + '0' + Optional(Char('oO')) + Chars('01234567')) + NextIsNot(Char(string.digits + string.ascii_letters)))
    bad_grammar = '-0' + Optional(Char('oO')) + Chars('0')
Octal = OctalInteger


class HexadecimalInteger(Grammar):
    grammar = Group((Optional('-') + '0' + Char('xX') + Chars('01234567890abcdefABCDEF')) + NextIsNot(Char(string.digits + string.ascii_letters)))
    bad_grammar = '-0' + Char('xX') + Chars('0')
Hex = HexadecimalInteger


class Number(Grammar):
    grammar = Float | BinaryInteger | OctalInteger | HexadecimalInteger | Integer


class OperatorGrammarType(GrammarType):
    def __init__(cls, classname, bases, cls_dict):
        super(OperatorGrammarType, cls).__init__(classname, bases, cls_dict)
        if cls_dict.get('operators'):
            cls.grammar = Any(*cls_dict['operators'])


class Operator(Grammar, metaclass=OperatorGrammarType):
    operators = [
        '==', '!=', '<=', '>=', '<', '>',
        '&&', '||', '&', '|', '<<', '>>', '~',
        '**',  '//',  '+',  '-',  '/',  '*',  '%',
        '.',  # function call
    ]
Op = Operator


class Assignment(Grammar, metaclass=OperatorGrammarType):
    operators = [
        '**=', '//=', '+=', '-=', '/=', '*=', '%=', '=',
    ]


class UnaryOperator(Grammar, metaclass=OperatorGrammarType):
    operators = ['~', '+', '-', '!']


class ReservedWordGrammarType(GrammarType):
    def __init__(cls, classname, bases, cls_dict):
        super(ReservedWordGrammarType, cls).__init__(classname, bases, cls_dict)
        if cls_dict.get('words'):
            cls.grammar = Any(*cls_dict.pop('words'))


class ReservedWord(Grammar, metaclass=ReservedWordGrammarType):
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
    def __init__(cls, classname, bases, cls_dict):
        super(VariableGrammarType, cls).__init__(classname, bases, cls_dict)
        starts_with = cls_dict.get('starts_with', cls.starts_with)
        ends_with = cls_dict.get('ends_with', cls.ends_with)
        cls.grammar = Group(starts_with + ends_with)


class Variable(Grammar, metaclass=VariableGrammarType):
    starts_with = Char(string.ascii_letters + '_')
    ends_with = Chars(string.ascii_letters + '_' + string.digits, min=0)
Var = Variable


class PythonVariable(Variable):
    bad_grammar = PythonReservedWord


class PhpVariable(Variable):
    starts_with = Char('$') + Char(string.ascii_letters + '_')


class RubyVariable(Variable):
    bad_grammar = RubyReservedWord


class EscapeSequence(Grammar):
    grammar = Group('\\' + Any('u' + Char('0123456789abcdefABCDEF') * 4, *list("nrtabfv\n\r\'\"\\")))


class QuotedGrammarType(GrammarType):
    def __init__(cls, classname, bases, cls_dict):
        super(QuotedGrammarType, cls).__init__(classname, bases, cls_dict)
        if cls_dict.get('delimiter'):
            if 'insides' in cls_dict:
                consumer = cls_dict['insides']
            else:
                insides = cls_dict['delimiter']
                for c in "\n\r\\":
                    if c not in insides:
                        insides += c
                consumer = Chars(insides, inverse=True)

            cls.grammar = Group((cls_dict['delimiter'] + ZeroOrMore(EscapeSequence | consumer) + cls_dict['delimiter'])[1:-1])


class QuotedString(Grammar, metaclass=QuotedGrammarType):
    pass


class SingleQuotedString(QuotedString):
    delimiter = "'"


class DoubleQuotedString(QuotedString):
    delimiter = '"'


class TripleSingleQuotedString(QuotedString):
    delimiter = "'''"
    insides = Regex('.', flags=re.DOTALL)


class TripleDoubleQuotedString(QuotedString):
    delimiter = '"""'
    insides = Regex('.', flags=re.DOTALL)


class String(Grammar):
    grammar = (TripleSingleQuotedString | TripleDoubleQuotedString | SingleQuotedString | DoubleQuotedString)


class Value(Grammar):
    grammar = (
            Number
          | Variable
          | String
             )
