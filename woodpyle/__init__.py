"""
Welcome.  Welcome to woodpyle.
"""
from .buffer import *
from .exceptions import *
from .matchers import *
from .grammar import *
from .result import *


# aliases
A = Letter
L = Literal
W = Word
S = Whitespace
R = Regex

# hide some Matchers
del AutoSequence
