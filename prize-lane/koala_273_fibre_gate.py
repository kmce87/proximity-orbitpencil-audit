#!/usr/bin/env python3
"""Exact necessary count/degree tests for a 273-fibre modification of the
public Koala 512-fibre OrbitPencil attack. NOT a Lean or prize certificate.

The calculation assumes the published pigeonhole key: t prescribed top
coefficients, one product label (512 values), a fixed 511-point core,
two shared polynomial roots, and the same row-degree limit.
Original construction: proximity-prize/proximity-prize,
ProximityPrize/SubmissionUpper/OrbitPencil.lean (2026-11-03).
"""
from math import comb

Q = 2**31 - 2**24 + 1
for k,t in [(272,14),(273,14),(273,15)]:
    n = comb(511,k)
    keys = Q**t * 512
    # Pigeonhole >2^59 members needs n > keys*2^59.
    count_ok = n > keys * 2**59
    # Difference of monic degree-k polynomials with t matching
    # subleading coefficients has degree < k-t. Dividing by two
    # guaranteed shared roots gives degree < k-t-2.
    # Original published proof requires pencil degree <256.
    pencil_lt = k-t-2
    degree_ok = pencil_lt <= 256
    agreement = k*512+511
    print(f'k={k} top={t} agreement={agreement} '
          f'count_ok={count_ok} degree_ok={degree_ok} '
          f'pencil_degree_lt={pencil_lt} '
          f'count_numerator={n} count_denominator={keys*2**59}')
    if (k,t)==(272,14): assert count_ok and degree_ok
    if (k,t)==(273,14): assert count_ok and not degree_ok
    if (k,t)==(273,15): assert not count_ok and degree_ok

print('PASS: neither 273-fibre variant meets both necessary conditions.')
print('No official score improvement, Lean kernel proof, or verifier acceptance.')
