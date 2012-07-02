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

Matchers
~~~~~~~~

``Matcher`` objects are the most basic building blocks.  They are not smart,
they return only strings and lists, and they make no assumptions about what you
might be trying to build.  For instance, the ``Word`` Matcher does not assume
that you want to consume whitespace.

``Matcher`` objects are great for building a small parsing language for
consistent data, where ``Grammar`` objects are not needed.  But for building a
language parser, you will probably use the more heavy-duty Grammar building
blocks.

Letter
~~~~~~

Matches a single letter from a string of accepted letters.  There are lots of
built-in strings in the `string module`_.

::

    test/matchers/test_letter_matcher.py

    matcher = Letter('abcde')
    matcher('a') => 'a'
    matcher('bcd') => 'b'
    matcher('f') => raise ParseException
    # shorthand:
    matcher = A('abcde')

    import string
    matcher = A(string.letters + string.digits + '_')

Word
~~~~

Matches one or more letters from string of accepted letters.

You can also set ``min`` and ``max`` options.  ``min`` will raise a
``ParseException`` if the matched word is not long enough.  Default is ``1``.
``max`` will stop matching once ``max`` characters are matched.

::

    test/matchers/test_word_matcher.py
    matcher = Word('abcde')
    matcher('a') => 'a'
    matcher('bcd') => 'bcd'
    matcher('defg') => 'defg'
    matcher('fghi') => ParseException

    # max
    matcher = Word('abcde', max=2)
    matcher('bcd') => 'bc'

    # min
    matcher = Word('abcde', min=3)
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
    matcher = Sequence(Literal('Hello '), Literal('World'), Letter('!.'))
    matcher('Hello World!') => ['Hello ', 'World', '!']
    matcher('Hello World.') => ['Hello ', 'World', '.']
    matcher('Hello, World.') => ParseException

The automatic ``Sequence`` type is created whenever you use addition or
multiplication to repeat a series of ``Matcher``s.

**Addition**::

    test/matchers/test_matcher_addition.py
    matcher = Literal('Hello ') + Literal('World') + Letter('!.')
    matcher('Hello World!') => ['Hello ', 'World', '!']
    matcher('Hello World.') => ['Hello ', 'World', '.']
    matcher('Hello, World.') => ParseException

**Multiplication**::

    test/matcher/test_matcher_multiplication.py
    import string
    matcher = (Word(string.letters) + Literal(' ')) * 3
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

**language building blocks**::

    QuotedString, Number, Integer, Float, Hexadecimal, Octal, Binary
    LineComment, BlockComment, Block, IndentedBlock

**location*::*

    NextIs, PreviousWas, NextIsNot, PreviousWasNot
    WordStart, WordEnd, LineStart, LineEnd,
    StringStart, StringEnd

----
TEST
----

::

    $ pip install pytest
    $ py.test

-------
LICENSE
-------

:Author: Colin Thomas-Arnold
:Copyright: 2012 Colin Thomas-Arnold <http://colinta.com/>

Copyright (c) 2012, Colin Thomas-Arnold
All rights reserved.

See LICENSE_ for more details (it's a simplified BSD license).

.. _LICENSE:      https://github.com/colinta/chomsky/blob/master/LICENSE
.. _modgrammar:   http://pypi.python.org/pypi/modgrammar
.. _pyparsing:    http://pyparsing.wikispaces.com/
.. _plywood:      http://github.com/colinta/plywood
.. _string module:       http://docs.python.org/library/string.html#string-constants
