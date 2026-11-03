#!/usr/bin/env python3
"""One falsifiable hypothesis: a four-valued correlated auxiliary key remains
within the 273-fibre Koala OrbitPencil pigeonhole budget, whereas an
eight-valued key does not. Exact integers only; NO third-root construction,
Lean certificate, or independently accepted benchmark improvement.

Published construction belongs to its original authors.
Baseline: 116.13 bits, unsafe index 122369.
Target: 116.12 bits, unsafe index <=122362.
"""
from math import comb
Q = 2**31 - 2**24 + 1
family = comb(511, 273)
base = Q**14 * 512 * 2**59
assert family > 4 * base, "4-valued key exceeds budget"
assert family <= 8 * base, "8-valued key unexpectedly affordable"
assert family // base == 6, "counting headroom changed"
# 273 fibres, 14 fixed top coefficients, 3 common roots: difference
# degree <=258, quotient degree <=255 (row-degree budget).
assert 273 - 14 - 1 - 3 == 255
# 273 fibres give 140287 agreeing coordinates, versus 139775 baseline.
assert 273*512+511 == 140287
assert 272*512+511 == 139775
print("PASS: four-valued extra key affordable by exact pigeonhole count")
print("PASS: eight-valued extra key not guaranteed")
print("exact ratio numerator:",family)
print("exact ratio denominator:",base)
print("maximum guaranteed auxiliary alphabet:",(family-1)//base)
print("BLOCKER: exhibit a four-valued invariant that FORCES a third")
print("common polynomial root, and prove distinct slopes; none known.")
print("STATUS: arithmetic only; no Lean proof, no accepted prize result.")
