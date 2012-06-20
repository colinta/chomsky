import re

from .exceptions import ParseException
from .result import Result, ResultList


def to_matcher(obj):
    if isinstance(obj, str):
        return Literal(obj)

    if isinstance(obj, list) or isinstance(obj, tuple):
        return Sequence(obj)

    raise TypeError('Unknown type {obj!r}'.format(obj=obj))


class Matcher(object):
    """
    Base class for Matcher objects, mostly to distinguish them from `Grammar`
    classes.
    """
    def __init__(self, *args, **kwargs):
        self.is_boundary = kwargs.pop('is_boundary', False)
        if kwargs:
            raise TypeError('Unknown options: {type.__name__}({keys!r})'.format(
                type=type(self),
                keys=kwargs.keys()
                ))

    def __repr__(self):
        raise TypeError()

    def __add__(self, other):
        if isinstance(other, str):
            return self + Literal(str)
        elif not isinstance(other, Matcher):
            raise TypeError
        return AutoSequence(self, other)

    def __mul__(self, other):
        if isinstance(other, int):
            return AutoSequence(*([self] * other))
        else:
            raise TypeError

    def __radd__(self, other):
        return to_matcher(other) + self

    def rollback(self, buffer, consumed, rollbacks, result):
        raise


class Letter(Matcher):
    """
    Consumes one characters from a list of acceptable characters.
    """
    def __init__(self, consumable, **kwargs):
        self.consumable = consumable
        super(Letter, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Letter) and self.consumable == other.consumable

    def __repr__(self):
        return '{type.__name__}({self.consumable!r})'.format(self=self, type=type(self))

    def consume(self, buffer):
        if buffer[0] in self.consumable:
            consumed = buffer[0]
            buffer.advance(1)
            return Result(consumed)
        raise ParseException(
            'Expected {self!r} at {buffer.position}'.format(
                self=self,
                buffer=buffer),
            buffer)


class Literal(Matcher):
    """
    Consumes a literal word by decomposing it into individual Letter() matchers.
    """
    def __init__(self, literal, **kwargs):
        self.literal = literal
        self.letters = map(Letter, literal)
        super(Literal, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Literal) and self.literal == other.literal

    def __repr__(self):
        return '{type.__name__}({self.literal!r})'.format(self=self, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        try:
            consumed = ''
            for letter in self.letters:
                consumed += letter.consume(buffer)
            buffer.forget_mark()
            return Result(consumed)
        except ParseException:
            buffer.restore_mark()
            raise ParseException(
                'Expected {self!r} at {buffer.position}'.format(
                    self=self,
                    buffer=buffer),
                buffer)


class Word(Matcher):
    """
    Consumes as many characters as possible from a list of acceptable
    characters by consuming as many Letter matches as possible.  You can pass
    min and max, if there is a desired length.  If the length of the consumed
    word is less than min, or greater than max, a ParseException is raised.
    """
    def __init__(self, consumable, **kwargs):
        """
        kwargs can contain 'max' and 'min' options
        """
        self.consumable = consumable
        self.letter = Letter(consumable)
        self.min = kwargs.pop('min', 1)
        self.max = kwargs.pop('max', None)
        super(Word, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Word) and self.consumable == other.consumable

    def __repr__(self):
        ret = '{type.__name__}({self.consumable!r}'
        if self.min != 1:
            ret += ', min={self.min!r}'
        if self.max != None:
            ret += ', max={self.max!r}'
        ret += ')'
        return ret.format(self=self, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        consumed = ''
        try:
            while True:
                consumed += self.letter.consume(buffer)
        except ParseException:
            pass
        if self.min != None and len(consumed) < self.min:
            buffer.restore_mark()
            raise ParseException(
                'Expected {self!r} at {buffer.position}'.format(
                    self=self,
                    buffer=buffer),
                buffer)
        if self.max != None and len(consumed) > self.max:
            buffer.restore_mark()
            raise ParseException(
                'Unexpected {self!r} at {buffer.position}'.format(
                    self=self,
                    buffer=buffer),
                buffer)
        buffer.forget_mark()
        return Result(consumed)


class Whitespace(Word):
    """
    Matches whitespace.  Whitespace is a boundary, and defaults to " \t"
    """
    def __init__(self, consumable=" \t", **kwargs):
        kwargs.setdefault('is_boundary', True)
        super(Whitespace, self).__init__(consumable, **kwargs)


class Regex(Matcher):
    """
    Matches a regular expression.
    """
    def __init__(self, regex, **kwargs):
        """
        kwargs can contain 'flags', 'group' and 'advance' options
        """
        flags = kwargs.pop('flags', 0)
        self.regex = re.compile(regex, flags=flags)
        self.group = kwargs.pop('group', 0)
        self.advance = kwargs.pop('advance', 0)
        super(Regex, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Word) and self.regex == other.regex

    def __repr__(self):
        ret = '{type.__name__}({self.regex!r})'
        return ret.format(self=self, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        match = self.regex.match(buffer.rest())
        if not match:
            buffer.restore_mark()
            raise ParseException(
                'Expected {self!r} at {buffer.position}'.format(
                    self=self,
                    buffer=buffer),
                buffer)
        buffer.advance(match.end(self.advance))
        buffer.forget_mark()
        if isinstance(self.group, tuple) or isinstance(self.group, list):
            return ResultList([Result(match.group(g)) for g in self.group])
        return Result(match.group(self.group))


class AutoSequence(Matcher):
    """
    When Matcher objects are added, they automatically create an AutoSequence,
    which will add in future Matcher objects as well.
    """
    default_whitespace = Whitespace()

    def __init__(self, *matchers, **kwargs):
        """
        A whitespace object can be provided in kwargs, which will override or
        disable (if None) the default Whitespace matcher.
        """
        self.whitespace = kwargs.pop('whitespace', AutoSequence.default_whitespace)
        if isinstance(self.whitespace, type):
            self.whitespace = self.whitespace()
        self.matchers = matchers
        super(AutoSequence, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, AutoSequence) and self.matchers == other.matchers and \
            self.whitespace == other.whitespace

    def __repr__(self):
        matchers = ', '.join(repr(m) for m in self.matchers)
        ret = '{type.__name__}({matchers}'
        if self.whitespace != AutoSequence.default_whitespace:
            ret += ', whitespace={self.whitespace!r}'
        ret += ')'
        return ret.format(matchers=matchers, self=self, type=type(self))

    def __add__(self, other):
        """
        An AutoSequence object is created anytime two Matchers are added, and
        adding subsequent Matchers to that sequence *appends* the matchers.
        """
        self.matchers += (other,)
        return self

    def consume(self, buffer):
        consumed = ResultList()
        rollbacks = []
        matcher_i = 0
        while True:
            if matcher_i == len(self.matchers):
                break
            matcher = self.matchers[matcher_i]

            try:
                if consumed and self.whitespace:
                    self.whitespace.consume(buffer)
                    rollbacks.append(self.whitespace)
                consumed.append(matcher.consume(buffer))
                rollbacks.append(matcher)
            except ParseException:
                if rollbacks:
                    rollback_matcher = rollbacks.pop()
                    result = consumed.pop()
                    rollback_matcher.rollback(buffer, consumed, rollbacks, result)
                else:
                    raise
            else:
                matcher_i += 1
        return consumed


class Sequence(AutoSequence):
    """
    Matches a sequence of Matcher objects separated by Whitespace
    """
    def __init__(self, *matchers, **kwargs):
        """
        You can group Sequences::
            Word('a') + Sequence(L('b') + 'c')

        But if you do, you will get a single AutoSequence object passed to the
        Sequence constructor.  The Sequence constructor will assign the
        AutoSequence object's .matchers property to itself, and throw away the
        AutoSequence object.
        """
        if len(matchers) == 1 and isinstance(matchers[0], AutoSequence):
            matchers = matchers[0].matchers
        super(Sequence, self).__init__(*matchers, **kwargs)

    def __add__(self, other):
        """
        Objects added to a Sequence create a new AutoSequence
        """
        return AutoSequence(self, other)


class NMatches(Matcher):
    def __init__(self, matcher, **kwargs):
        self.matcher = matcher
        self.min = kwargs.pop('min')
        self.max = kwargs.pop('max')
        super(NMatches, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, ZeroOrMore) and self.matcher == other.matcher

    def __repr__(self):
        ret = '{type.__name__}({self.matcher!s})'
        return ret.format(self=self, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        consumed = ResultList()
        try:
            while True:
                matched = self.matcher.consume(buffer)
                print self.matcher, repr(matched)
                consumed.append(matched)
                if self.max is not None and len(consumed) == self.max:
                    break
        except ParseException:
            pass
        if self.min is not None and len(consumed) < self.min:
            buffer.restore_mark()
            raise ParseException(
                'Expected {self!r} at {buffer.position}'.format(
                    self=self,
                    buffer=buffer),
                buffer)
        buffer.forget_mark()
        return consumed

    def rollback(self, buffer, consumed, rollbacks, result):
        if self.min is not None and len(result) > self.min:
            result.pop()
            consumed.append(result)
            rollbacks.append(rollbacks)
            return
        raise


class ZeroOrMore(NMatches):
    def __init__(self, matcher, **kwargs):
        kwargs['min'] = None
        kwargs['max'] = None
        super(ZeroOrMore, self).__init__(matcher, **kwargs)


class Optional(NMatches):
    def __init__(self, matcher, **kwargs):
        kwargs['min'] = 0
        kwargs['max'] = 1
        super(Optional, self).__init__(matcher, **kwargs)


class OneOrMore(NMatches):
    def __init__(self, matcher, **kwargs):
        kwargs['min'] = 1
        kwargs['max'] = None
        super(OneOrMore, self).__init__(matcher, **kwargs)
