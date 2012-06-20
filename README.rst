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

**basic grammar building blocks**::

    Letter/A   # tested
    Word/W     # tested
    Literal/L  # tested

**advanced building blocks**::

    Regex/R    # tested

**repetition*::*

    Sequence                     # tested
    Matcher + Matcher + Matcher  # tested
    Matcher * 3                  # tested

    ZeroOrMore, OneOrMore, Optional
    Any, NextIs, NextIsNot

**language building blocks*::*

    QuotedString, Number, Integer, Float, Hexadecimal, Octal, Binary
    LineComment, BlockComment, Block, IndentedBlock

**location*::*

    NextIs, PreviousWas, NextIsNot, PreviousWasNot
    WordStart, WordEnd, LineStart, LineEnd, StringStart, StringEnd


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
.. _pyparsing:   http://pyparsing.wikispaces.com/
.. _plywood:   http://github.com/colinta/plywood
