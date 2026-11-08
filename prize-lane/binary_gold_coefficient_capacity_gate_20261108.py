#!/usr/bin/env python3
"""Exact capacity obstruction for coefficient-only Gold attacks, binary upper 106.23.

Does not assert an IRS witness, soundness, Lean compilation or verifier acceptance.
"""
from fractions import Fraction

N = 2**21
BASE = 2**64
EXT = BASE**3
EPS_DEN = 2**128
SCORE = 10623
INDEX = 917378
AGREEMENT = N - INDEX

# At most 2^64 distinct challenges can arise from one parameter a in GF(2^64).
# Strict winning density > 2^-128 over GF(2^192) requires > 2^64.
max_density = Fraction(BASE, EXT)
threshold = Fraction(1, EPS_DEN)
assert max_density == threshold
assert not max_density > threshold
assert AGREEMENT == 1179774
assert INDEX < 917441

# Exact score check: 2^(-10623/100) <= ((N-INDEX)/N)^128.
assert 2**(21*12800-SCORE) <= AGREEMENT**12800
print("target: ProtocolClaimUpper", SCORE, INDEX)
print("agreement:", AGREEMENT)
print("maximum coefficient-only challenges:", BASE)
print("strict minimum challenges:", BASE+1)
print("maximum density = 2^-128; target strictly > 2^-128")
print("score inequality: PASS (exact integer)")
print("coefficient-only Gold family: IMPOSSIBLE for strict unsafeAbove")
