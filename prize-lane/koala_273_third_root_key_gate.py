#!/usr/bin/env python3
"""Exact necessary-count gate for a THIRD forced root in 273-fibre Koala pencil.
One falsifiable hypothesis: add one base-field-valued evaluation key to the
published 14-top-coefficient/product key, preserving >2^59 slopes.
NOT a universal impossibility claim, Lean proof, or accepted attack.
Published construction: ProximityPrize/SubmissionUpper/OrbitPencil.lean.
"""
from math import comb
Q = 2**31 - 2**24 + 1
N = comb(511, 273)
BASE_KEYS = Q**14 * 512
MIN_SLOPES = 2**59
assert N > BASE_KEYS * MIN_SLOPES  # existing 14-key count remains viable
# A 273-degree monic polynomial with 14 common top coefficients has
# pairwise difference degree <=258. A third distinct common root makes
# quotient degree <=255, the published row-degree budget.
assert 273 - 14 - 1 - 3 == 255
# But a new independent K-valued evaluation key costs Q key values.
# Even a much cheaper 512-valued extra key loses the 2^59 guarantee.
assert N <= BASE_KEYS * 512 * MIN_SLOPES
assert N <= BASE_KEYS * Q * MIN_SLOPES
print('PASS: 273 fibres + 14 top coefficients + 3 roots has quotient degree <=255.')
print('PASS: extra 512-valued key cannot guarantee >2^59 parameters.')
print('PASS: extra base-field-valued key cannot guarantee >2^59 parameters.')
print('EXACT ratios (numerator / denominator):')
for name, cost in [('no extra key',1),('512-valued key',512),('base-field key',Q)]:
    d=BASE_KEYS*cost*MIN_SLOPES
    print(name, 'numerator=',N, 'denominator=',d,
          'strict count condition=',N>d)
print('LIMIT: only pigeonhole guarantees; does not rule out structured')
print('evaluation coincidences, lower-cost correlated keys, or new attacks.')
print('No Lean kernel certificate or independent verifier acceptance.')
