from chomsky import *


def test_flattened():
    matcher = Flatten(Chars('aeiou') + (Chars('pqrst') + Chars('12345')))
    assert matcher('aeioupqrst12345') == ['aeiou', 'pqrst', '12345']
