#!/usr/bin/env python3
"""Lane B: falsify the single-polynomial-zero-set interpretation of OrbitPencil agreement."""
N = 1 << 18
ROW_DIM = 1 << 17
MAX_DEGREE = ROW_DIM - 1
CORE = 511
FIBRE = 512
SELECTED = 272
AGREEMENT = CORE + FIBRE * SELECTED
TARGET_INDEX = 122362
REQUIRED = N - TARGET_INDEX
assert AGREEMENT == 139775
assert REQUIRED == 139782
assert AGREEMENT > MAX_DEGREE
assert REQUIRED > MAX_DEGREE
print(f'maximum nonzero message-polynomial roots: {MAX_DEGREE}')
print(f'published guaranteed agreement positions: {AGREEMENT}')
print(f'116.12 candidate required positions: {REQUIRED}')
print('PASS: neither agreement set can be the zero set of a single nonzero message polynomial.')
print('Scope: degree/root theorem only; does not refute interleaved winning-set construction.')
