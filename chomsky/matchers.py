import re
import string

from .exceptions import ParseException, RollbackException
from .result import Result, ResultList
from .buffer import Buffer


Infinity = float('inf')


def to_matcher(obj):
    if isinstance(obj, type):
        return obj

    if isinstance(obj, Matcher):
        return obj

    if isinstance(obj, str):
        return Literal(obj)

    if isinstance(obj, list) or isinstance(obj, tuple):
        return Sequence(*obj)

    raise TypeError('Unknown type {obj!r}'.format(obj=obj))


class Matcher(object):
    """
    Provides functionality shared with all Matcher objects.

    Any methods added here should also be added to the GrammarType class.
    """
    default_suppressed = False

    def __init__(self, *args, **kwargs):
        self.grammar = None
        self.suppress = kwargs.pop('suppress', self.default_suppressed)
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
        if self.suppress != self.default_suppressed:
            args = ('suppress={self.suppress!r}'.format(self=self),)
        else:
            args = ()
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

    def __add__(self, other):
        return AutoSequence(self, to_matcher(other))

    def __radd__(self, other):
        return to_matcher(other) + self

    def __mul__(self, other):
        if isinstance(other, int):
            return AutoSequence(*([self] * other))
        else:
            raise TypeError

    def __or__(self, other):
        return AutoAny(self, to_matcher(other))

    def __ror__(self, other):
        return to_matcher(other) | self

    def __call__(self, string):
        return self.consume(Buffer(string))

    def rollback(self, result, buffer):
        # Moves the buffer position, and then claims that it can't rollback.
        # What a liar.
        if result:
            buffer.advance(-len(result))
        raise RollbackException()

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return Infinity


class GrammarType(type):
    def __init__(cls, classname, bases, cls_dict):
        cls.suppress = cls_dict.get('suppress', getattr(cls, 'suppress', False))
        cls.ignore_whitespace = cls_dict.get('ignore_whitespace', getattr(cls, 'ignore_whitespace', True))
        cls.whitespace = cls_dict.get('whitespace', getattr(cls, 'whitespace', Whitespace()))

    def __add__(cls, other):
        return cls.grammar.__add__(other)

    def __radd__(cls, other):
        return cls.grammar.__radd__(other)

    def __mul__(cls, other):
        return cls.grammar.__mul__(other)

    def __or__(cls, other):
        return cls.grammar.__or__(other)

    def __ror__(cls, other):
        return cls.grammar.__ror__(other)

    def rollback(cls, *args, **kwargs):
        return cls.grammar.rollback(*args, **kwargs)

    def minimum_length(cls, *args, **kwargs):
        return cls.grammar.minimum_length(*args, **kwargs)

    def maximum_length(cls, *args, **kwargs):
        return cls.grammar.maximum_length(*args, **kwargs)

    def consume(cls, buffer):
        try:
            return cls.grammar.consume(buffer)
        except ParseException:
            if cls.ignore_whitespace:
                cls.whitespace.consume(buffer)
                return cls.grammar.consume(buffer)
            raise

    def __repr__(cls):
        return cls.__name__


class SuppressedMatcher(Matcher):
    default_suppressed = True


class NoMatch(SuppressedMatcher):
    def consume(self, buffer):
        raise ParseException(
            'NoMatch {self!r} at {buffer.position}'.format(
                self=self,
                buffer=buffer),
            buffer)

    def minimum_length(self):
        return 1

    def maximum_length(self):
        return 1


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
        args = ('{self.consumable!r}'.format(self=self), ) + super(Letter, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

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
        args = ('{self.literal!r}'.format(self=self),) + super(Literal, self).__repr__(args_only=True)
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

    def consume(self, buffer):
        buffer.mark()
        for c in self.literal:
            try:
                b = buffer[0]
            except ParseException:
                buffer.restore_mark()
                raise
            if b == c:
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


class Chars(Matcher):
    """
    Consumes as many characters as possible from a list of acceptable
    characters by consuming as many Letter matches as possible.  You can pass
    min and max, if there is a desired length.  If the length of the consumed
    word is less than min, or greater than max, a ParseException is raised.
    """
    default_word = None
    default_min = 1
    default_max = None

    def __init__(self, consumable, **kwargs):
        """
        kwargs can contain 'max' and 'min' options
        """
        self.consumable = consumable
        self.letter = Letter(consumable)
        self.min = kwargs.pop('min', self.default_min)
        if self.min == None:
            self.min = 0
        self.max = kwargs.pop('max', self.default_max)
        super(Chars, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Chars) and self.consumable == other.consumable \
            and self.letter == other.letter \
            and self.min == other.min \
            and self.max == other.max \
            and super(Chars, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = []
        if self.consumable != self.default_word:
            args.append('{self.consumable!r}'.format(self=self))
        if self.min != self.default_min:
            args.append('min={self.min!r}'.format(self=self))
        if self.max != self.default_max:
            args.append('max={self.max!r}'.format(self=self))

        args.extend(super(Chars, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

    def consume(self, buffer):
        buffer.mark()
        consumed = ''
        try:
            while True:
                consumed += self.letter.consume(buffer)
                if self.max != None and len(consumed) == self.max:
                    break
        except ParseException:
            pass
        if self.min and len(consumed) < self.min:
            buffer.restore_mark()
            raise ParseException(
                'Expected {self!r} at {buffer.position}'.format(
                    self=self,
                    buffer=buffer),
                buffer)
        buffer.forget_mark()
        return Result(consumed)

    def rollback(self, result, buffer):
        if len(result) > self.min:
            buffer.advance(-1)
            return result[:-1]
        raise RollbackException()

    def minimum_length(self):
        return self.min

    def maximum_length(self):
        return self.max if self.max is not None else Infinity


class Whitespace(Chars):
    """
    Matches whitespace.  Defaults to string.whitespace
    """
    default_suppressed = True
    default_word = string.whitespace
    default_min = 0

    def __init__(self, consumable=None, **kwargs):
        if consumable is None:
            consumable = self.default_word
        kwargs.setdefault('suppress', True)
        super(Whitespace, self).__init__(consumable, **kwargs)


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
        args = ['{self.regex.pattern!r}'.format(self=self)]

        if self.group != self.default_group:
            args.append('group={self.group!r}'.format(self=self))
        if self.advance != self.default_advance:
            args.append('advance={self.advance!r}'.format(self=self))
        args.extend(super(Regex, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

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
        type_name = type(self).__name__
        if type_name == 'AutoSequence':
            type_name = 'Sequence'
            joiner = ' + '
        else:
            joiner = ', '

        matchers = joiner.join(repr(m) for m in self.matchers)
        args = ['{matchers}'.format(matchers=matchers)]
        if self.separated_by is not None:
            args.append('sep={self.separated_by!r}'.format(self=self))
        args.extend(super(AutoSequence, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type_name}({args})'.format(args=', '.join(args), type_name=type_name)

    def __add__(self, other):
        """
        An AutoSequence object is created anytime two Matchers are added, and
        adding subsequent Matchers to that sequence *appends* the matchers.
        """
        self.matchers.append(to_matcher(other))
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
            except ParseException, error:
                if rollbacks:
                    # rollback until successful
                    while matcher_i > 0:
                        rollback_matcher, result = rollbacks.pop()
                        # remove the matched content, if it wasn't suppressed
                        if not rollback_matcher.suppress and result is not None:
                            consumed.pop()

                        try:
                            new_result = rollback_matcher.rollback(result, buffer)
                            if not rollback_matcher.suppress and new_result is not None:
                                consumed.append(new_result)
                            rollbacks.append((rollback_matcher, new_result))
                            break
                        except RollbackException:
                            # couldn't rollback, so move the matcher pointer and
                            # try to rollback the next item.
                            matcher_i -= 1

                if not rollbacks:
                    raise error
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
            Chars('a') + Sequence(L('b') + 'c')

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
        args = ['{self.matcher!r}'.format(self=self)]
        if self.min != self.default_min:
            args.append('min={self.min!r}'.format(self=self))
        if self.max != self.default_max:
            args.append('max={self.max!r}'.format(self=self))

        args.extend(super(NMatches, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

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

    def rollback(self, result, buffer):
        min = 0 if self.min is None else self.min
        if len(result) > min:
            buffer.advance(-len(result[-1]))
            return result[:-1]
        raise RollbackException()

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


class AutoAny(Matcher):
    """
    Created when the `|` operator is used to combine matchers (an implicit
    `Any` matcher)
    """
    def __init__(self, *matchers, **kwargs):
        self.matchers = [to_matcher(m) for m in matchers]
        super(AutoAny, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, AutoAny) and self.matchers == other.matchers \
            and super(Any, self).__eq__(other)

    def __or__(self, other):
        """
        An AutoAny object is created anytime two Matchers are added, and
        adding subsequent Matchers to that sequence *appends* the matchers.
        """
        self.matchers.append(to_matcher(other))
        return self

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

    def __repr__(self, args_only=False):
        type_name = type(self).__name__
        if type_name == 'AutoAny':
            type_name = 'Any'
            joiner = ' | '
        else:
            joiner = ', '

        matchers = joiner.join(repr(m) for m in self.matchers)
        args = ['{matchers}'.format(matchers=matchers)]
        # args = [repr(m) for m in self.matchers]
        args.extend(super(AutoAny, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type_name}({args})'.format(type_name=type_name, args=', '.join(args))

    def minimum_length(self):
        return min(m.minimum_length() for m in self.matchers)

    def maximum_length(self):
        return max(m.maximum_length() for m in self.matchers)


class Any(AutoAny):
    """
    Accepts a list of Matcher objects and consumes the first that passes.
    """
    def __init__(self, *matchers, **kwargs):
        """
        You can group Any operations::
            Chars('a') + Any(L('b') | 'c')

        But if you do, you will get a single AutoAny object passed to the Any
        constructor.  The Any constructor will assign the AutoAny object's
        .matchers property to itself, and throw away the AutoAny object.
        """
        if len(matchers) == 1 and isinstance(matchers[0], AutoAny):
            matchers = matchers[0].matchers
        super(Any, self).__init__(*matchers, **kwargs)

    def __or__(self, other):
        """
        Objects OR'd to an Any create a new AutoAny::

            Any('a', 'b') | 'c' => 'a' | 'b' | 'c'
        """
        return AutoAny(*self.matchers) | other


class StringStart(SuppressedMatcher):
    def consume(self, buffer):
        if buffer.position != 0:
            raise ParseException('Expected buffer to be at StringStart(0), not {0}'.format(buffer.position), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class StringEnd(SuppressedMatcher):
    def consume(self, buffer):
        if buffer.position != len(buffer):
            raise ParseException('Expected buffer to be at StringEnd({0}), not {1}'.format(len(buffer), buffer.position), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class LineStart(SuppressedMatcher):
    def consume(self, buffer):
        if buffer.position > 0 and buffer[-1] != "\n":
            raise ParseException('Expected {self!r} at {0}, not {1!r}'.format(buffer.position - 1, buffer[-1], self=self), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class LineEnd(SuppressedMatcher):
    def consume(self, buffer):
        if buffer.position < len(buffer) and buffer[0] != "\n":
            raise ParseException('Expected {self!r} at {0}, not {1!r}'.format(buffer.position, buffer[0], self=self), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class WordStart(SuppressedMatcher):
    default_word = string.letters

    def __init__(self, consumable=None, **kwargs):
        self.consumable = consumable if consumable else self.default_word
        super(WordStart, self).__init__(**kwargs)

    def consume(self, buffer):
        if buffer.position > 0 and buffer[-1] in self.consumable:
            raise ParseException('Expected {self!r} at {0}, not {1!r}'.format(buffer.position - 1, buffer[-1], self=self), buffer)
        if buffer[0] not in self.consumable:
            raise ParseException('Expected {self!r} at {0}, not {1!r}'.format(buffer.position, buffer[0], self=self), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class WordEnd(SuppressedMatcher):
    default_word = string.letters

    def __init__(self, consumable=None, **kwargs):
        self.consumable = consumable if consumable else self.default_word
        super(WordEnd, self).__init__(**kwargs)

    def consume(self, buffer):
        if buffer[-1] not in self.consumable:
            raise ParseException('Expected {self!r} at {0}, not {1!r}'.format(buffer.position - 1, buffer[-1], self=self), buffer)
        if buffer.position < len(buffer) and buffer[0] in self.consumable:
            raise ParseException('Expected {self!r} at {0}, not {1!r}'.format(buffer.position, buffer[0], self=self), buffer)
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class NextIs(SuppressedMatcher):
    def __init__(self, matcher, **kwargs):
        self.matcher = to_matcher(matcher)
        super(NextIs, self).__init__(**kwargs)

    def __repr__(self, args_only=False):
        args = ['{self.matcher!r}'.format(self=self)]
        args.extend(super(NextIs, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

    def consume(self, buffer):
        buffer.mark()
        self.matcher.consume(buffer)
        buffer.restore_mark()
        return None

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


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


class PrevIs(SuppressedMatcher):
    """
    This matcher is very resource intensive, because it needs to reverse check
    that any previous text would match self.matcher.
    """
    def __init__(self, matcher, **kwargs):
        self.matcher = to_matcher(matcher)
        super(PrevIs, self).__init__(**kwargs)

    def __repr__(self, args_only=False):
        args = ['{self.matcher!r}'.format(self=self)]
        args.extend(super(PrevIs, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

    def consume(self, buffer):
        buffer.mark()
        length = self.matcher.minimum_length()
        max_length = self.matcher.maximum_length()
        # assert False
        while buffer.position > 0:
            buffer.advance(-1)
            test_buffer = buffer[0:length]
            try:
                self.matcher.consume(test_buffer)
                # make sure we used the entire buffer
                if not test_buffer.rest():
                    # it worked!  restore the mark and continue
                    buffer.restore_mark()
                    return None
            except ParseException:
                pass
            length += 1
            if length > max_length:
                break

        buffer.restore_mark()
        raise ParseException('Expect buffer to be {self.matcher!r}, at {buffer.position}'.format(self=self, buffer=buffer), buffer)

    def minimum_length(self):
        return 0

    def maximum_length(self):
        return 0


class PrevIsNot(PrevIs):
    """
    This matcher is very resource intensive, because it needs to reverse check
    that no previous text would match self.matcher.  It is helped (but not by
    much) by using the "minimum_length" and "maximum_length" methods.
    """
    def consume(self, buffer):
        buffer.mark()
        length = self.matcher.minimum_length()
        max_length = self.matcher.maximum_length()
        raise_me = None
        while buffer.position > 0:
            buffer.advance(-1)
            test_buffer = buffer[0:length]
            try:
                self.matcher.consume(test_buffer)
                # make sure we used the entire buffer
                if not test_buffer.rest():
                    # it worked!  dang
                    buffer.restore_mark()
                    raise_me = ParseException('Did not expect buffer to be {self.matcher!r}, at {buffer.position}'.format(self=self, buffer=buffer), buffer)
                    break
            except ParseException:
                pass
            length += 1
            if length > max_length:
                break

        if raise_me:
            raise raise_me
        buffer.restore_mark()
        return None


class Group(Matcher):
    """
    Flattens a Sequence into one string.
    """
    def __init__(self, matcher, *args, **kwargs):
        if args:
            self.matcher = Sequence(matcher, *args)
        else:
            self.matcher = to_matcher(matcher)
        super(Group, self).__init__(self, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Group) and self.matcher == other.matcher \
            and super(Group, self).__eq__(other)

    def __repr__(self, args_only=False):
        args = ['{self.matcher!r}'.format(self=self)]
        args.extend(super(Group, self).__repr__(args_only=True))
        if args_only:
            return args
        return '{type.__name__}({args})'.format(type=type(self), args=', '.join(args))

    def consume(self, buffer):
        return ''.join(str(s) for s in self.matcher.consume(buffer))

    def minimum_length(self):
        return self.matcher.minimum_length()

    def maximum_length(self):
        return self.matcher.maximum_length()
