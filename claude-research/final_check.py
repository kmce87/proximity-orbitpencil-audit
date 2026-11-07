#!/usr/bin/env python3
"""FINAL (run 9): exact recheck of the headline numbers quoted in LEDGER.md.

Pure integer arithmetic except for the printed log2 values. No new hypothesis.
Credits: the record and its family are BitWonka's (PR #592); the pole pair is
from Dao-Kominers-Thaler-Zheng as credited in the ledger.
"""
from fractions import Fraction
from math import log2

N, T = 2**21, 128          # domain size, repetitions


def passes(centibits, a):
    """Solution.lean form: 2^(-c/100) <= (a/N)^T  <=>  2^(21*100*T - c) <= a^(100*T)."""
    return 2 ** (21 * 100 * T - centibits) <= a ** (100 * T)


def min_agreement(centibits):
    lo, hi = N // 2, N
    while lo < hi:                      # passes() is monotone in a
        mid = (lo + hi) // 2
        if passes(centibits, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def score(a):
    return -T * log2(a / N)


rec = 63 + 64 * (2**14 + 2**11)
assert rec == 1179711 and passes(10624, rec) and not passes(10623, rec)
need = min_agreement(10623)
assert need == 1179774 and need - rec == 63
print(f"record agreement {rec}, score {score(rec):.4f}; 106.23 needs >= {need} (+{need - rec})")

members = 420 * 32 * 2047 * (1023 * 1022 * 1021) * 512 * 4
print(f"record members {members} = 2^{log2(members):.3f}")
assert 2**65 < members < 2**66


def gauss(n, r):
    num = den = 1
    for i in range(r):
        num *= 2 ** (n - i) - 1
        den *= 2 ** (i + 1) - 1
    assert num % den == 0
    return num // den


# run 3 (N6): the f = 7 class, ny = 10
Nrho = [11440, 14721280, 11988756480, 279283630080, 231211008000]
M_all = lambda ny: sum(gauss(ny, r) * Nrho[r] for r in range(5))
m10 = M_all(10)
assert m10 == 14201103363987440560 and (7 * m10) % 16 == 0
avoid = 7 * m10 // 16
assert avoid == 6212982721744505245
print(f"f = 7 class (ny = 10): 2^{log2(m10):.3f}, short by {2**64 / m10:.3f}; "
      f"avoiding a label {avoid} = 2^{log2(avoid):.3f}, short by {2**64 / avoid:.3f}")
m11 = M_all(11)
print(f"f = 6 class (ny = 11): 2^{log2(m11):.3f}; avoiding a label 2^{log2(7 * m11 / 16):.3f}")

# run 5 (N7): mean-1/2 quadric family at n = 21
MC = 8 * gauss(21, 2) * (2**19 - 1)
assert MC == 3074447083519519400
print(f"M_C(21)/2 = 2^{log2(MC / 2):.3f}, short of 2^64 by {Fraction(2**64, MC // 2):.4f} = {2**64 / (MC / 2):.3f}")

# run 4 (N3): the K-line route at 19/32, if it ever had > 2^64 winners
k19 = 19 * N // 32
print(f"19/32 agreement {k19}: score {score(k19):.2f} (with the 63 core: {score(k19 + 63):.2f})")
print(f"budget: winners must exceed 2^64 = |BF64|; |Ext3| / 2^128 = {2**192 // 2**128 == 2**64}")
print("ALL CHECKS PASS")
