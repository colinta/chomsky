========
woodpyle
========

I needed a language grammar parser for the plywood_ project, and modgrammar_
looked like it would be perfect, except I couldn't get the simplest of grammars
to work.  pyparsing_ is excellent, but doesn't give me objects back, only lists
and strings - I need more than that.  I would recommend pyparsing_ for *your*
project.  Unless you really want objects, or if you are doing a language
(woodpyle_ has lots of built-in stuff for making programming language grammars).

Besides, I like writing parsers, and I know how I want this one to work, so
screw it, I'll do it myself!

------------
INSTALLATION
------------

::
    $ pip install woodpyle

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

::
    test/matchers/test_sequence_matcher.py


**arithmetic**::

    Matcher + Matcher + Matcher  # tested
    Matcher * 3                  # tested

**repetition**::

    ZeroOrMore  # tested
    OneOrMore   # tested
    Optional    # tested

    Any, NextIs, NextIsNot

**language building blocks*::*

    QuotedString, Number, Integer, Float, Hexadecimal, Octal, Binary
    LineComment, BlockComment, Block, IndentedBlock

**location*::*

    NextIs, PreviousWas, NextIsNot, PreviousWasNot
    WordStart, WordEnd, LineStart, LineEnd,
    StringStart, StringEnd


::
    from woodpyle import *


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

.. _LICENSE:      https://github.com/colinta/woodpyle/blob/master/LICENSE
.. _modgrammar:   http://pypi.python.org/pypi/modgrammar
.. _pyparsing:    http://pyparsing.wikispaces.com/
.. _plywood:      http://github.com/colinta/plywood
.. _string module:       http://docs.python.org/library/string.html#string-constants
