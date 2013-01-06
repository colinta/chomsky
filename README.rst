=======
chomsky
=======

I needed a language grammar parser for the plywood_ project, and modgrammar_
looked like it would be perfect, except I couldn't get the simplest of grammars
to work.  pyparsing_ is excellent, but doesn't give me objects back, only lists
and strings - I need more than that.  I would recommend pyparsing_ for *your*
project.  Unless you really want objects, or if you are doing a language
(chomsky_ has lots of built-in stuff for making programming language grammars).

Besides, I like writing parsers, and I know how I want this one to work, so
screw it, I'll do it myself!

------------
INSTALLATION
------------

::

    $ pip install chomsky

-----
USAGE
-----

~~~~~~~~
Matchers
~~~~~~~~

``Matcher`` objects are the most basic building blocks.  They are not smart,
they return only strings and lists, and they make no assumptions about what you
might be trying to build.  For instance, the ``Chars`` Matcher does not assume
that you want to consume whitespace.

``Matcher`` objects are great for building a small parsing language for
consistent data, where ``Grammar`` objects are not needed.  But for building a
language parser, you will probably use the more heavy-duty Grammar building
blocks.

Char
~~~~

Matches a single letter from a string of accepted letters.  There are lots of
built-in strings in the `string module`_.

::

    test/matchers/test_letter_matcher.py

    matcher = Char('abcde')
    matcher('a') => 'a'
    matcher('bcd') => 'b'
    matcher('f') => raise ParseException
    # shorthand:
    matcher = A('abcde')

    import string
    matcher = A(string.letters + string.digits + '_')

Chars
~~~~~

Matches one or more letters from string of accepted letters.

You can also set ``min`` and ``max`` options.  ``min`` will raise a
``ParseException`` if the matched word is not long enough.  Default is ``1``.
``max`` will stop matching once ``max`` characters are matched.

::

    test/matchers/test_word_matcher.py
    matcher = Chars('abcde')
    matcher('a') => 'a'
    matcher('bcd') => 'bcd'
    matcher('defg') => 'defg'
    matcher('fghi') => ParseException

    # max
    matcher = Chars('abcde', max=2)
    matcher('bcd') => 'bc'

    # min
    matcher = Chars('abcde', min=3)
    matcher('ab') => ParseException

Literal
~~~~~~~

Matches a literal string.

::

    test/matchers/test_literal_matcher.py
    matcher = Literal('abcde')
    matcher('a') => 'a'
    matcher('bcd') => 'bcd'
    matcher('defg') => 'defg'
    matcher('fghi') => ParseException

Whitespace
~~~~~~~~~~

::

    test/matchers/test_whitespace_matcher.py
    matcher = Whitespace()  # default is " \t"
    matcher("    ") => "    "
    matcher(" \t\n ") => " \t"
    matcher = Whitespace(" \t\n")
    matcher(" \t\n ") => " \t\n "

Regex
~~~~~

These have two options: ``group`` and ``advance``.

``group`` says which group or groups to return.  Default is ``0`` (the entire
match).  A list or tuple of groups will return a list of results.  ``advance``
indicates what group to advance *past*.  Default is ``0`` (the entire match).
This is a quick way to build a matching system that can parse consistently
formatted data, for example.

::

    test/matchers/test_regex_matcher.py
    matcher = Regex("([a-zA-Z_][0-9])")
    matcher('a1') => 'a1'

    # group
    matcher = Regex("([a-zA-Z_][0-9])", group=1)
    matcher('a1') => 'a'

    # to demonstrate `advance`, I will have to add two regex Matchers, which
    # returns a list
    matcher = Regex("([a-zA-Z_][0-9])", group=1, advance=1) + Regex("([0-9])", group=1)
    matcher('a1') => ['a', '1']

Sequence
~~~~~~~~

There are two flavors of ``Sequence``.  One you can declare yourself, called
``Sequence``, the other is created automatically when you add or multiply
Matcher objects.  Don't worry about that one, it "just works" (we saw it above
in the ``Regex`` example).

::

    test/matchers/test_sequence_matcher.py
    matcher = Sequence(Literal('Hello '), Literal('World'), Char('!.'))
    matcher('Hello World!') => ['Hello ', 'World', '!']
    matcher('Hello World.') => ['Hello ', 'World', '.']
    matcher('Hello, World.') => ParseException

The automatic ``Sequence`` type is created whenever you use addition or
multiplication to repeat a series of ``Matcher``-s.

**Addition**::

    test/matchers/test_matcher_addition.py
    matcher = Literal('Hello ') + Literal('World') + Char('!.')
    matcher('Hello World!') => ['Hello ', 'World', '!']
    matcher('Hello World.') => ['Hello ', 'World', '.']
    matcher('Hello, World.') => ParseException

**Multiplication**::

    test/matcher/test_matcher_multiplication.py
    import string
    matcher = (Chars(string.letters) + Literal(' ')) * 3
    matcher('why hello there ') => [['why', ' '], ['hello', ' '], ['there', ' ']]
    matcher('not enough spaces') => ParseException

NMatches
~~~~~~~~

``NMatches`` is not an intuitively named class, but its child classes are, and
you'll probably use them a lot.

``ZeroOrMore``::

    test/matcher/test_zero_or_more_matcher.py
    matcher = ZeroOrMore(Literal('hi'))
    matcher('') => []
    matcher('hi') => ['hi']
    matcher('hihi') => ['hi', 'hi']

``OneOrMore``::

    test/matcher/test_one_or_more_matcher.py
    matcher = OneOrMore(Literal('hi'))
    matcher('hi') => ['hi']
    matcher('hihi') => ['hi', 'hi']
    matcher('') => ParseException

``Optional``::

    test/matcher/test_optional_matcher.py
    matcher = Literal('Hello') + Optional(Literal(',')) + Literal(' ') + Literal('World')
    matcher('Hello World') => ['Hello', [], ' ', 'World']
    matcher('Hello, World') => ['Hello', [','], ' ', 'World']
    matcher('Hello, Bozo') => ParseException

``NMatches``::

    test/matcher/test_nmatcher.py
    matcher = NMatches(Literal('hi'), min=2, max=3)
    matcher('hi') => ParseException
    matcher('hihi') => ['hi', 'hi']
    matcher('hihihi') => ['hi', 'hi', 'hi']
    matcher('hihihihi') => ['hi', 'hi', 'hi']  # only 3 matches

Any
~~~

Given a list of Matchers, any of them can match (tested in order left-to-right).
The first to match is returned.

::

    test/matcher/test_any_matcher.py
    matcher = Any(Literal('Joey'), Literal('Bob'), Literal('Bill'))
    matcher('Bob') => 'Bob'
    matcher('Jane') => ParseException

Look-ahead and Behind
~~~~~~~~~~~~~~~~~~~~~

Looking-ahead is simple and low-cost.  The ``NextIs`` matcher makes sure that
the ``Matcher`` *would* pass, but then rolls back the cursor and does not return
a Result.  If the ``Matcher`` fails, an exception is raised.

Looking behind is much more expensive, because the number of characters to look
at is not known before hand.  A "best guess" can be made by ``PrevIs`` by using
```minimum_length``` and ```maximum_length``` methods that the ``Matcher``
classes all implement (the base class returns ``0`` and ``float('inf')``).  A
``Literal``, for example, has a definite length that must be present - no more,
and no less characters.  The other classes also provide this min/max length
calculation. But this provides only a modest performance increase.

The ``PrevIs`` matcher does not require that the previous token be an instance of
the specified matcher, only that the buffer previous to the current location
match.  The buffer is rolled back until a match is found, or until the beginning
of the buffer is reached.  Sound resource intensive?  Consider ``PrevIsNot``!
It looks backwards, hoping that the buffer *never* matches, no matter how far
back it goes.

``NextIs``::

    test/matcher/test_nextis_matcher.py
    matcher = '-' + NextIs(Chars('123456789')) + Chars('1234567890')
    matcher('1') => [[], '1']
    matcher('-1') => [['-'], '1']
    matcher('-123') => [['-'], '123']
    matcher('-0') => ParseException

``NextIsNot``::

    test/matcher/test_nextis_matcher.py
    matcher = '-' + NextIsNot('0') + Chars('1234567890')
    matcher('1') => [[], '1']
    matcher('-1') => [['-'], '1']
    matcher('-123') => [['-'], '123']
    matcher('-0') => ParseException

``PrevIs``::

    test/matcher/test_nextis_matcher.py
    matcher = Chars('-.') + PrevIs('-') + Chars('1234567890')
    matcher('-1') => [['-'], '1']
    matcher('.123') => ParseException

``PrevIsNot``::

    test/matcher/test_nextis_matcher.py
    matcher = Chars('abc') + PrevIsNot('c') + Chars('abc')
    matcher('ab') => ['a', 'b']
    matcher('abc') => ['ab', 'c']
    matcher('abcabc') => ['abcab', 'c']
    matcher('cc') => ParseException

~~~~~~~~
Grammars
~~~~~~~~

``Grammar`` objects are what you will want to work with if you are building a
language grammar.  They are composed of ``Mathcer`` classes (and other
``Grammar`` classes), but the objects they return are instances of the
``Grammar``, not simple strings and lists.

The built-in ``Grammar``-s are meant to help you understand how they work, and to
use in your own language.

Numbers
~~~~~~~

``Integer``::

    test/matcher/test_nextis_matcher.py
    matcher = '-' + NextIsNot('0') + Chars('1234567890')
    matcher('1') => [[], '1']
    matcher('-1') => [['-'], '1']
    matcher('-123') => [['-'], '123']
    matcher('-0') => ParseException

Todo
~~~~

::

    QuotedString, Number, Integer, Float, Hexadecimal, Octal, Binary
    LineComment, BlockComment, Block, IndentedBlock

----
TEST
----

::

    $ pip install pytest
    $ py.test

-------
LICENSE
-------

Copyright (c) 2012, Colin Thomas-Arnold
All rights reserved.

:author:    Colin Thomas-Arnold
:copyright: 2012 Colin Thomas-Arnold <http://colinta.com/>
:license:   simplified BSD, see LICENSE_ for more details.

.. _LICENSE:      https://github.com/colinta/chomsky/blob/master/LICENSE
.. _modgrammar:   http://pypi.python.org/pypi/modgrammar
.. _pyparsing:    http://pyparsing.wikispaces.com/
.. _plywood:      http://github.com/colinta/plywood
.. _string module:       http://docs.python.org/library/string.html#string-constants
