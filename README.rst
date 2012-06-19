========
woodpyle
========

I needed a language grammar parser for the plywood project, and modgrammar
looked like it would be perfect, except I couldn't get the simplest of grammars
to work.  pyparsing is excellent, but doesn't give me objects back, only lists
and strings - I need more than that.

I like writing parsers, and I know how I want this one to work, so screw it,
I'll do it myself.

------------
INSTALLATION
------------

::

    $ pip install woodpyle


-----
USAGE
-----

::

    from woodpyle import *

    # basic grammar building blocks:
    #   Word/W, Literal/L, Regex/R
    # advanced building blocks:
    # repetition:
    #   ZeroOrMore, OneOrMore, Optional
    #   Any, NextIs, NextIsNot
    # language building blocks
    #   QuotedString, Number, Integer, Float, Hexadecimal, Octal, Binary
    #   LineComment, BlockComment, Block, IndentedBlock
    # location
    #   NextIs, PreviousWas, NextIsNot, PreviousWasNot
    #   WordStart, WordEnd, LineStart, LineEnd, StringStart, StringEnd

-------
LICENSE
-------

:Author: Colin Thomas-Arnold
:Copyright: 2012 Colin Thomas-Arnold <http://colinta.com/>

Copyright (c) 2012, Colin Thomas-Arnold
All rights reserved.

See LICENSE_ for more details (it's a simplified BSD license).

.. _LICENSE:      https://github.com/colinta/woodpyle/blob/master/LICENSE
.. _Modgrammar:   http://pypi.python.org/pypi/modgrammar
.. _pyparsing:   http://pyparsing.wikispaces.com/
