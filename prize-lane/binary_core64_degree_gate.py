#!/usr/bin/env python3
"""Exact degree gate for a 64-point core in published binary CorePencil.
Source: proximity-prize/proximity-prize, SubmissionBinaryUpper/CorePencil.lean.
No Lean theorem or verifier acceptance is claimed.
"""
N=2**21
MAX_DEG=2**20-1
Y_DEG=64
Q_DEG=16383
BASE_CORE=63
BASE_AGREEMENT=1179711
TARGET_AGREEMENT=N-917378
assert BASE_CORE+Y_DEG*Q_DEG==MAX_DEG
assert BASE_AGREEMENT==63+64*18432
assert TARGET_AGREEMENT==1179774
assert 64+Y_DEG*Q_DEG==MAX_DEG+1
assert 64+Y_DEG*(Q_DEG-1)==MAX_DEG-63
assert TARGET_AGREEMENT-BASE_AGREEMENT==63
print('PASS: core 64 with Q degree 16383 exceeds permitted degree by one')
print('PASS: lowering Q degree to 16382 restores degree admissibility')
print('PASS: core 64 alone gains only one of the 63 required agreements')
