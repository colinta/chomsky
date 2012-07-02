import re

from .exceptions import ParseException
from .result import Result, ResultList
from .buffer import Buffer


Infinity = float('inf')


def to_matcher(obj):
    if isinstance(obj, Matcher):
        return obj

    if isinstance(obj, str):
        return Literal(obj)

    if isinstance(obj, list) or isinstance(obj, tuple):
        return Sequence(*obj)

    raise TypeError('Unknown type {obj!r}'.format(obj=obj))


class Matcher(object):
    """
    Base class for Matcher objects, mostly to distinguish them from `Grammar` classes.
    """
    def __init__(self, *args, **kwargs):
        self.suppress = kwargs.pop('suppress', False)
        if kwargs:
            raise TypeError('Unknown options: {type.__name__}({keys!r})'.format(
                type=type(self),
                keys=kwargs.keys()
                ))

    def __eq__(self, other):
        return isinstance(other, Matcher) and self.suppress == other.suppress

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self, args_only=False):
        if args_only:
            if self.suppress:
                return ', suppress=True'
            return ''
        raise TypeError()

    def __add__(self, other):
        return AutoSequence(self, to_matcher(other))

    def __mul__(self, other):
        if isinstance(other, int):
            return AutoSequence(*([self] * other))
        else:
            raise TypeError

    def __radd__(self, other):
        return to_matcher(other) + self

    def parse_string(self, string):
        buffer = Buffer(string)
        return self.consume(buffer)

    __call__ = parse_string

    def rollback(self, buffer, consumed, result):
        raise

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return Infinity


class Letter(Matcher):
    """
    Consumes one characters from a list of acceptable characters.
    """
    def __init__(self, consumable, **kwargs):
        self.consumable = consumable
        super(Letter, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Letter) and self.consumable == other.consumable \
            and super(Letter, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = '{self.consumable!r}'.format(self=self) + super(Letter, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=args)

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

    def minimum_length(self):
        return 1

    def maximum_length(self):
        return 1


class Literal(Matcher):
    """
    Consumes a literal word by decomposing it into individual Letter() matchers.
    """
    def __init__(self, literal, **kwargs):
        self.literal = literal
        super(Literal, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Literal) and self.literal == other.literal \
            and super(Literal, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = '{self.literal!r}'.format(self=self) + super(Literal, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(args=args, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        for c in self.literal:
            if buffer[0] == c:
                buffer.advance(1)
            else:
                buffer.restore_mark()
                raise ParseException(
                    'Expected {self!r} at {buffer.position}'.format(
                        self=self,
                        buffer=buffer),
                    buffer)
        buffer.forget_mark()
        return Result(self.literal)

    def minimum_length(self):
        return len(self.literal)

    def maximum_length(self):
        return len(self.literal)


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
        return isinstance(other, Word) and self.consumable == other.consumable \
            and self.letter == other.letter \
            and self.min == other.min \
            and self.max == other.max \
            and super(Word, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = '{self.consumable!r}'
        if self.min != 1:
            args += ', min={self.min!r}'
        if self.max != None:
            args += ', max={self.max!r}'
        args = args.format(self=self) + super(Word, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(args=args, type=type(self))

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

    def minimum_length(self):
        return self.min

    def maximum_length(self):
        return self.max if self.max is not None else Infinity


class Whitespace(Word):
    default_whitespace = " \t"
    """
    Matches whitespace.  Whitespace is a boundary, and defaults to " \t"
    """
    def __init__(self, consumable=None, **kwargs):
        if consumable is None:
            consumable = self.default_whitespace
        kwargs.setdefault('suppress', True)
        super(Whitespace, self).__init__(consumable, **kwargs)

    def __repr__(self, args_only=False):
        if self.consumable != self.default_whitespace:
            args = '{self.consumable!r}'
            comma = ', '
        else:
            args = ''
            comma = ''
        if self.min != 1:
            args += comma + 'min={self.min!r}'
            comma = ', '
        if self.max != None:
            args += comma + 'max={self.max!r}'
            comma = ', '
        if not self.suppress:
            args += comma + 'suppress=False'
        args = args.format(self=self)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(args=args, type=type(self))


class Regex(Matcher):
    default_group = 0
    default_advance = 0

    """
    Matches a regular expression.
    """
    def __init__(self, regex, **kwargs):
        """
        kwargs can contain 'flags', 'group' and 'advance' options
        """
        flags = kwargs.pop('flags', 0)
        self.regex = re.compile(regex, flags=flags)
        self.group = kwargs.pop('group', self.default_group)
        self.advance = kwargs.pop('advance', self.default_advance)
        super(Regex, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Regex) and self.regex.pattern == other.regex.pattern \
            and self.group == other.group \
            and self.advance == other.advance \
            and super(Regex, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = '{self.regex.pattern!r}'
        if self.group != self.default_group:
            args += ', group={self.group!r}'
        if self.advance != self.default_advance:
            args += ', advance={self.advance!r}'
        args = args.format(self=self) + super(Regex, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(args=args, type=type(self))

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
    def __init__(self, *matchers, **kwargs):
        """
        kwargs can include 'sep', which is a matcher to match in between every item.
        """
        self.separated_by = kwargs.pop('sep', None)
        if isinstance(self.separated_by, type):
            self.separated_by = self.separated_by()
        self.matchers = [to_matcher(m) for m in matchers]
        super(AutoSequence, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, AutoSequence) and self.matchers == other.matchers and \
            self.separated_by == other.separated_by \
            and super(AutoSequence, self).__eq__(other)

    def __repr__(self, args_only=False):
        matchers = ', '.join(repr(m) for m in self.matchers)
        args = '{matchers}'
        if self.separated_by is not None:
            args += ', sep={self.separated_by!r}'
        args = args.format(self=self, matchers=matchers) + super(AutoSequence, self).__repr__(args_only=True)
        if args_only:
            return args

        type_name = type(self).__name__
        if type_name == 'AutoSequence':
            type_name = 'Sequence'
        return '{type_name}({args})'.format(args=args, type_name=type_name)

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
                if consumed and self.separated_by:
                    token_consumed = self.separated_by.consume(buffer)
                    if not self.separated_by.suppress and token_consumed is not None:
                        consumed.append(token_consumed)
                    rollbacks.append((self.separated_by, token_consumed))

                token_consumed = matcher.consume(buffer)
                if not matcher.suppress and token_consumed is not None:
                    consumed.append(token_consumed)
                rollbacks.append((matcher, token_consumed))
            except ParseException:
                if rollbacks:
                    rollback_matcher, result = rollbacks.pop()
                    rollback_matcher.rollback(buffer, consumed, result)
                else:
                    raise
            else:
                matcher_i += 1
        return consumed

    def minimum_length(self):
        return sum(m.minimum_length() for m in self.matchers)

    def maximum_length(self):
        if any(m.maximum_length() == Infinity for m in self.matchers):
            return Infinity
        return sum(m.maximum_length() for m in self.matchers)


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
    default_min = None
    default_max = None

    def __init__(self, matcher, **kwargs):
        self.matcher = to_matcher(matcher)
        self.min = kwargs.pop('min')
        self.max = kwargs.pop('max')
        super(NMatches, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, NMatches) and self.matcher == other.matcher \
            and super(NMatches, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = '{self.matcher!r}'
        if self.min != self.default_min:
            args += ', min={self.min!r}'
        if self.max != self.default_max:
            args += ', max={self.max!r}'

        args = args.format(self=self) + super(NMatches, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(args=args, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        consumed = ResultList()
        try:
            matched_count = 0
            while True:
                matched = self.matcher.consume(buffer)
                if matched is not None:
                    consumed.append(matched)
                matched_count += 1
                if self.max is not None and matched_count == self.max:
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

    def rollback(self, buffer, consumed, result):
        min = 0 if self.min is None else self.min
        if len(result) > min:
            result.pop()
            consumed.append(result)
            return
        raise

    def minimum_length(self):
        if self.min:
            return self.matcher.minimum_length() * self.min
        return 0

    def maximum_length(self):
        if self.max is None or self.matcher.maximum_length() == Infinity:
            return Infinity
        return self.matcher.maximum_length() * self.max


class ZeroOrMore(NMatches):
    default_min = None
    default_max = None

    def __init__(self, matcher, **kwargs):
        kwargs['min'] = None
        kwargs['max'] = None
        super(ZeroOrMore, self).__init__(matcher, **kwargs)


class Optional(NMatches):
    default_min = 0
    default_max = 1

    def __init__(self, matcher, **kwargs):
        kwargs['min'] = 0
        kwargs['max'] = 1
        super(Optional, self).__init__(matcher, **kwargs)


class OneOrMore(NMatches):
    default_min = 1
    default_max = None

    def __init__(self, matcher, **kwargs):
        kwargs['min'] = 1
        kwargs['max'] = None
        super(OneOrMore, self).__init__(matcher, **kwargs)


class Any(Matcher):
    """
    Accepts a list of Matcher objects and consumes the first that passes.
    """
    def __init__(self, *matchers, **kwargs):
        self.matchers = [to_matcher(m) for m in matchers]
        super(Any, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Any) and self.matchers == other.matchers \
            and super(Any, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = ', '.join(repr(m) for m in self.matchers) + super(Any, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(args=args, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        matcher_i = 0
        while True:
            if matcher_i == len(self.matchers):
                break
            matcher = self.matchers[matcher_i]

            try:
                token_consumed = matcher.consume(buffer)
                return token_consumed
            except ParseException:
                matcher_i += 1

        buffer.restore_mark()
        raise ParseException(
            'Expected {self!r} at {buffer.position}'.format(
                self=self,
                buffer=buffer),
            buffer)

    def minimum_length(self):
        return min(m.minimum_length() for m in self.matchers)

    def maximum_length(self):
        return max(m.maximum_length() for m in self.matchers)


class StringStart(Matcher):
    def __init__(self, **kwargs):
        kwargs.setdefault('suppress', True)
        super(StringStart, self).__init__(**kwargs)

    def __repr__(self, args_only=False):
        args = ''
        if not self.suppress:
            args = 'suppress=False'
        return '{type.__name__}({args})'.format(args=args, type=type(self))

    def consume(self, buffer):
        if buffer.position != 0:
            raise ParseException('Expected buffer to be at StringStart(0), not {0}'.format(buffer.position), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class StringEnd(Matcher):
    def __init__(self, **kwargs):
        kwargs.setdefault('suppress', True)
        super(StringEnd, self).__init__(**kwargs)

    def __repr__(self, args_only=False):
        args = ''
        if not self.suppress:
            args = 'suppress=False'
        return '{type.__name__}({args})'.format(args=args, type=type(self))

    def consume(self, buffer):
        if buffer.position != len(buffer):
            raise ParseException('Expected buffer to be at StringEnd({0}), not {1}'.format(len(buffer), buffer.position), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class NextIs(Matcher):
    def __init__(self, matcher, **kwargs):
        self.matcher = to_matcher(matcher)
        super(NextIs, self).__init__(**kwargs)

    def __repr__(self, args_only=False):
        args = '{self.matcher!r}'.format(self=self) + super(NextIs, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(args=args, type=type(self))

    def consume(self, buffer):
        buffer.mark()
        self.matcher.consume(buffer)
        buffer.restore_mark()
        return None

    def minimum_length(self):
        return self.matcher.minimum_length()

    def maximum_length(self):
        return self.matcher.maximum_length()


class NextIsNot(NextIs):
    def consume(self, buffer):
        buffer.mark()
        try:
            super(NextIsNot, self).consume(buffer)
        except ParseException:
            buffer.restore_mark()
            return None
        buffer.restore_mark()
        raise ParseException('Did not expect buffer to be {self.matcher!r}, at {buffer.position}'.format(self=self, buffer=buffer), buffer)
