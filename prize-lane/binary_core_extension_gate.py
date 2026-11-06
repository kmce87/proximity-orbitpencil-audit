#!/usr/bin/env python3
"""Exact degree-budget gate for a naive 63-core-point extension of the
pre-existing BitWonka binary 106.24 upper source. Not a Lean certificate.
Source: ProximityPrize/SubmissionBinaryUpper/CorePencil.lean (2026-11-06).
"""
N=2**21
DEG_CAP=2**20-1
Q_BOUND=16383
FIBRE=64
CORE=63
LABELS=18432
CURRENT=CORE+LABELS*FIBRE
TARGET_INDEX=917378
TARGET=N-TARGET_INDEX
EXTRA=TARGET-CURRENT
assert CURRENT==1179711 and TARGET==1179774 and EXTRA==63
assert CORE+Q_BOUND*FIBRE==DEG_CAP
NEW_CORE=CORE+EXTRA
assert NEW_CORE+Q_BOUND*FIBRE==DEG_CAP+EXTRA
# If no quotient leading-coefficient cancellation, the 126-core polynomial
# exceeds the allowed degree by 63; the existing proof only bounds Q <= 16383.
assert NEW_CORE+Q_BOUND*FIBRE>DEG_CAP
# With 126 core roots, the same degree bound would require Q <= 16382.
assert (DEG_CAP-NEW_CORE)//FIBRE==16382
print('PASS: 106.23 target needs 63 new agreement points')
print('PASS: naive 126-core extension has degree ceiling 1048638 > 1048575')
print('PASS: quotient degree must drop from <=16383 to <=16382')
print('NOT PROVED: a new attack, cancellation, or independent acceptance')
