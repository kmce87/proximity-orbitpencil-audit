#!/usr/bin/env python3
"""Exact arithmetic audit of the public 511-choose-272 OrbitPencil key extension.
No claim of existence/nonexistence of particular collisions; no Lean proof.
Source: zksecurity/proximity-prize-submissions-lean434,
submissions/reduction-upper/11613/OrbitPencil.lean.
"""
from math import comb
Q = 2**31 - 2**24 + 1
C = comb(511, 272)
TARGET = 2**59 + 1
for k in (14, 15):
    keys = 512 * Q**k
    guaranteed = (C + keys - 1)//keys  # ceil(C/keys)
    print(f'{k} top coefficients: full candidates={C}; key bound={keys}')
    print(f'  guaranteed maximum fibre >= {guaranteed}; exceeds 2^59: {guaranteed >= TARGET}')
    if k == 15:
        # Need number of attained keys <= floor(C/TARGET) for an average argument.
        max_attained_keys = (C-1)//(TARGET-1)  # sufficient for strict C > 2^59 * keys
        reduction_needed = (keys + max_attained_keys - 1)//max_attained_keys
        print('  key bound reduction factor needed:', reduction_needed)
        print('  maximum keys for strict >2^59 pigeonhole:', max_attained_keys)
assert (C + 512*Q**14-1)//(512*Q**14) >= TARGET
assert (C + 512*Q**15-1)//(512*Q**15) < TARGET
print('PASS: 14-key counting works; naive 15-key counting cannot certify target')
