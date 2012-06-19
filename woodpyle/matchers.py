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
    def __add__(self, other):
        if isinstance(other, str):
            return self + Literal(str)
        elif not isinstance(other, Matcher):
            raise TypeError
        return AutoSequence(self, other)

    def __radd__(self, other):
        return to_matcher(other) + self


class Letter(Matcher):
    """
    Consumes one characters from a list of acceptable characters.
    """
    def __init__(self, consumable):
        self.consumable = consumable

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
    def __init__(self, literal):
        self.literal = literal
        self.letters = map(Letter, literal)

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
    def __init__(self, consumable, min=1, max=None):
        self.consumable = consumable
        self.letter = Letter(consumable)
        self.min = min
        self.max = max

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
        consumed = ''
        buffer.mark()
        try:
            while True:
                consumed += self.letter.consume(buffer)
        except ParseException:
            pass
        if (self.min != None and len(consumed) < self.min) or \
                (self.max != None and len(consumed) > self.max):
            buffer.restore_mark()
            raise ParseException(
                'Expected {self!r} at {buffer.position}'.format(
                    self=self,
                    buffer=buffer),
                buffer)
        buffer.forget_mark()
        return Result(consumed)


class Whitespace(Word):
    """
    Matches whitespace
    """
    def __init__(self, consumable=" \t\n", **kwargs):
        return super(Whitespace, self).__init__(consumable, **kwargs)


class AutoSequence(Matcher):
    """
    When Matcher objects are added, they automatically create an AutoSequence,
    which will add in future Matcher objects as well.
    """
    default_whitespace = Whitespace()

    def __init__(self, *matchers, **kwargs):
        self.whitespace = kwargs.pop('whitespace', AutoSequence.default_whitespace)
        if isinstance(self.whitespace, type):
            self.whitespace = self.whitespace()
        self.matchers = matchers

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
        print 'here'
        consumed = ResultList()
        for matcher in self.matchers:
            if consumed and self.whitespace:
                consumed.append(self.whitespace.consume(buffer), suppress=True)
            consumed.append(matcher.consume(buffer))
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
