import string
from chomsky import *


class Variable(Grammar):
    grammar = Letter(string.letters + '_') + Word(string.letters + string.digits + '_')


class Expression(Grammar):
    grammar = String | Integer | Variable
    suppress = True


class KeywordArgument(Grammar):
    grammar = Variable + '=' + Expression


class Arguments(Grammar):
    grammar = '(' + Separated(',', Expression | KeywordArgument) + ')'


class Function(Grammar):
    grammar = Variable + Arguments


Function('foo("bar", 1, bar, pip=pop)')
    # => [Variable('foo'), [String("bar", quote='"'), Integer(1), Variable("baz"), KeywordArgument(Variable('pip'), Variable('pop')))]]
