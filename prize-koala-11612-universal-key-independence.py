#!/usr/bin/env python3
"""Counterexample to universal coefficient redundancy; NOT a candidate-set counterexample."""
q = 2**31 - 2**24 + 1
n = 272
p = {n: 1, 0: 1}
r = {n: 1, n-15: 1, 0: 1}
def top14(poly):
    return tuple(poly.get(n-1-i, 0) % q for i in range(14))
def coefficient15(poly):
    return poly.get(n-15, 0) % q
assert top14(p) == top14(r) == (0,)*14
assert p[0] == r[0] == 1
assert coefficient15(p) == 0 and coefficient15(r) == 1
print('FIELD:', q)
print('DEGREE:', n)
print('P: X^272 + 1')
print('R: X^272 + X^257 + 1')
print('SAME first 14 top coefficients: YES')
print('SAME constant coefficient: YES')
print('DIFFERENT fifteenth coefficient: 0 versus 1')
print('UNIVERSAL coefficient dependency: FALSIFIED')
print('RESTRICTED split-root 272-subset dependency: UNRESOLVED')
