from pytest import raises
from chomsky import *


def test_nomatch_fail():
    with raises(ParseException):
        print NoMatch()('')
