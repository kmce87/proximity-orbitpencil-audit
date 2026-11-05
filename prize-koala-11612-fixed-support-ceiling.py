#!/usr/bin/env python3
"""Reproduce the fixed-support obstruction in published 116.13 OrbitPencil.lean.
Sources: OrbitPencil.lean coreA=Finset.univ.erase 0, Candidates=powersetCard 272,
blockPairs=Finset.univ.product U, T_card=139775, window lower=122369/262144.
This is a mathematical bound for the UNCHANGED support architecture, not a
universal impossibility result and not a Lean proof.
"""
N = 262144
FIBRE_SIZE = 512
SELECTED_FIBRES = 272
CORE_MAX = 511
OLD_UNSAFE_INDEX = 122369
NEW_UNSAFE_INDEX = 122362
support_max = SELECTED_FIBRES * FIBRE_SIZE + CORE_MAX
assert support_max == 139775
assert N - OLD_UNSAFE_INDEX == support_max
assert N - NEW_UNSAFE_INDEX == 139782
assert N - NEW_UNSAFE_INDEX - support_max == 7
assert N - NEW_UNSAFE_INDEX - SELECTED_FIBRES * FIBRE_SIZE == 518 > CORE_MAX
print("PASS: unchanged 272-fibre + at-most-511 core supports", support_max)
print("PASS: 116.12 index requires", N - NEW_UNSAFE_INDEX, "agreement points")
print("PASS: support shortfall =", N - NEW_UNSAFE_INDEX - support_max)
