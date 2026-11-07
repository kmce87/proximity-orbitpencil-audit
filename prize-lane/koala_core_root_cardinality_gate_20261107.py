#!/usr/bin/env python3
"""Koala 116.12-bit core-root cardinality gate.

Hypothesis: rearranging the roots of a nonzero degree-511 core polynomial,
while retaining 272 complete 512-point fibres, can certify 139782
agreement positions using the published two agreement mechanisms.

This does not rule out accidental agreement elsewhere or other architectures.
Source: ProximityPrize/SubmissionUpper/OrbitPencil.lean (official main).
"""
N = 2**18
FIBRE_SIZE = 512
SELECTED_FIBRES = 272
CORE_DEGREE = 511
CENTIBITS = 11612
REPETITIONS = 128

def score_holds(agreement):
    # 2^(-centibits/100) <= (agreement/N)^repetitions
    # Equivalent exact integer inequality:
    return (1 << (18 * REPETITIONS * 100 - CENTIBITS)) <= agreement ** (REPETITIONS * 100)

assert N == 262144
assert SELECTED_FIBRES * FIBRE_SIZE == 139264
assert SELECTED_FIBRES * FIBRE_SIZE + CORE_DEGREE == 139775
assert not score_holds(139781)
assert score_holds(139782)
max_certified = SELECTED_FIBRES * FIBRE_SIZE + CORE_DEGREE
min_needed = 139782
assert min_needed - max_certified == 7
# Nonzero polynomial of degree <= 511 over a field has <= 511 roots.
# For a set B of 272 complete fibres and core roots C,
# |B union C| <= |B| + |C| <= 272*512 + 511.
print('target=ProtocolClaimUpper 11612 122362 (score-grid candidate only)')
print('official_baseline=ProtocolClaimUpper 11613 122369')
print('complete_fibre_points=', SELECTED_FIBRES * FIBRE_SIZE)
print('max_core_roots=', CORE_DEGREE)
print('max_guaranteed_agreement=', max_certified)
print('minimum_agreement_for_11612=', min_needed)
print('missing_positions=', min_needed - max_certified)
print('baseline_score_11612_pass=', score_holds(max_certified))
print('threshold_score_11612_pass=', score_holds(min_needed))
print('RESULT=FALSIFIED for rearrangements preserving 272 fibres and nonzero core degree <=511')
