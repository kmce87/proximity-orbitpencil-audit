#!/usr/bin/env python3
"""Exact cardinality gate for reusing published 116.13 OrbitPencil witness.
Source: zksecurity/proximity-prize-submissions-lean434
submissions/reduction-upper/11613/{Solution,OrbitPencil}.lean.
Only disproves reuse of unchanged T(U), not existence of other witnesses.
"""
N=262144
OLD_INDEX=122369
NEW_INDEX=122362
CORE=511
FIBRE=512
SELECTED=272
AGREEMENT=CORE+FIBRE*SELECTED
assert AGREEMENT==139775
assert N-OLD_INDEX==AGREEMENT
assert N-NEW_INDEX==139782
assert N-NEW_INDEX-AGREEMENT==7
assert N-NEW_INDEX>AGREEMENT
assert CORE==FIBRE-1
assert (N-NEW_INDEX-CORE+FIBRE-1)//FIBRE==273
print('published agreement:',AGREEMENT)
print('116.12 required agreement:',N-NEW_INDEX)
print('shortfall:',N-NEW_INDEX-AGREEMENT)
print('minimum whole fibres if core unchanged:',273)
print('PASS: unchanged published T(U) cannot witness index 122362')
