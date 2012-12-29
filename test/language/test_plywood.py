'''
load('url')  # basic function call to load in extension
# parentheses are optional, because things like 'if' and 'for' look
# better without 'em.  plywood has no "reserved words"
load 'compress'
debug = true  # yes, this template language has variable assignment

doctype('html')
html:
  head:
    meta(charset="utf-8")
    title:
      # the if statement, which is a rather complicated plugin because it
      # can be followed by any number of elif's and an optional else.
      if title:
        # docstrings *are* stripped of preceding whitespace (they must be
        # indented), and the first and last newline is removed.
        """
        {title} |
        """  # string interpolation is a little more heavy-duty than `.format()`, but more similar than different.
      'Welcome'  # string literals require quotes
'''
# from pytest import raises
from chomsky import *


class Block(Matcher):
    def consume(self, buffer):
        return buffer


class Assignment(Grammar):
    grammar = Variable + '=' + Value


class plywood(Grammar):
    grammar = Block(
        (String | Assignment | Function | BlankLine) + Optional(Comment)
        )


def test_oneline_repr():
    assert repr(plywood('0 + 1')) == "plywood('0+1')"
