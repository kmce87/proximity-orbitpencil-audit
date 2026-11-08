#!/usr/bin/env python3
"""Lane B: one-bit affine extension of rank-zero Gold family.

Counts zeros of auxiliary Boolean forms, not IRS agreement or winning challenges.
No Lean compilation, kernel proof, or independent verifier acceptance.
"""
from binary_gold_linear_kernel_20261108 import encode_polar, kernel, linear_restriction

DIM = 21
DOMAIN = 1 << DIM
TARGET_AGREEMENT = 1179774  # binary upper 106.23, index 917378

rank, basis = kernel([encode_polar(1 << i) for i in range(64)])
assert rank == 57 and len(basis) == 7
counts = {0: 0, DOMAIN // 2: 0, DOMAIN: 0}
for mask in range(1 << len(basis)):
    a = 0
    for i, b in enumerate(basis):
        if (mask >> i) & 1:
            a ^= b
    assert encode_polar(a) == 0
    linear = linear_restriction(a)
    for bit in (0, 1):
        zeros = (DOMAIN if bit == 0 else 0) if linear == 0 else DOMAIN // 2
        counts[zeros] += 1
assert counts == {0: 16, DOMAIN // 2: 224, DOMAIN: 16}, counts
assert DOMAIN // 2 < TARGET_AGREEMENT < DOMAIN
assert sum(counts.values()) == 256
print('rank-zero Gold affine family size:', sum(counts.values()))
print('zero counts (positions -> pairs):', counts)
print('agreement target:', TARGET_AGREEMENT)
print('nonconstant affine Gold forms cannot reach target zeros')
print('16 constant-zero forms remain; zero counts do not imply IRS attacks')
