#!/usr/bin/env python3
"""Exact support-capacity gate for unchanged 272-fibre/512-column architecture.
Source: zksecurity/proximity-prize-submissions-lean434,
submissions/reduction-upper/11613/OrbitPencil.lean (coreA, T_card).
Combinatorial bound only; NOT a Lean proof.
"""
FIBRES=272
WIDTH=512
OLD_CORE=511
DOMAIN=262144
TARGET_INDEX=122362
old=FIBRES*WIDTH+OLD_CORE
required=DOMAIN-TARGET_INDEX
max_support=FIBRES*WIDTH+WIDTH
assert old==139775
assert required==139782
assert max_support==139776
assert required-max_support==6
assert required-old==7
print('existing support:',old)
print('116.12 required support:',required)
print('maximum support with 272 complete fibres and one 512-point core:',max_support)
print('remaining shortfall even if core includes all 512 points:',required-max_support)
print('PASS: enlarging only the existing single core cannot reach 116.12')
