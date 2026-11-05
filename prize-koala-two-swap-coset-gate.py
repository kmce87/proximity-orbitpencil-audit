#!/usr/bin/env python3
"""Koala 116.12: exact cardinality gate for up to two swaps from complete 16-cosets.
The permitted set has 511 roots: 31 complete 16-cosets plus one 15-root coset.
No Lean proof or independently accepted claim is asserted.
"""
from math import comb
TARGET = (1 << 59) + 1
BASES = comb(31, 17)
REMAINING = 511 - 17*16
assert REMAINING == 239
counts = {k: BASES * comb(272,k) * comb(REMAINING,k) for k in range(3)}
# Unique base reconstruction: after at most two swaps, originally chosen
# cosets have >=14 elements, all other cosets have <=2 elements.
assert counts[0] == 265182525
assert counts[1] == 17238985585200
assert counts[2] == 277970023068557400
assert sum(counts.values()) < TARGET
print('target:', TARGET)
print('counts:', counts)
print('up_to_two:', sum(counts.values()))
print('shortfall:', TARGET - sum(counts.values()))
print('PASS: at most two swaps cannot supply 2^59+1 candidates')
