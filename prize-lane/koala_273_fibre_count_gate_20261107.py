#!/usr/bin/env python3
"""Exact integer Koala 273-fibre counting gate, not a Lean proof.

Official source: ProximityPrize/SubmissionUpper/OrbitPencil.lean
Candidates, topKey, productKey, orbit_count, cpoly_natDegree_le.
"""
from math import comb

FIELD = 2**31 - 2**24 + 1
REQUIRED = 2**59
DEGREE_CEILING = 131071

def guaranteed(fibres, keys):
    return comb(511, fibres) // (FIELD**keys * 512)

def main():
    baseline = guaranteed(272, 14)
    candidate = guaranteed(273, 14)
    overkeyed = guaranteed(273, 15)
    assert baseline == 4009245024241067460
    assert candidate == 3509925131112143307
    assert overkeyed == 1647305830
    assert candidate > REQUIRED and overkeyed < REQUIRED
    # 273 fibres, monic and 14 fixed top coefficients:
    # deg(delta V) <= 258. Two forced pencil roots give deg(Q) <= 256.
    # A third distinct root, NOT established, would give deg(Q) <= 255.
    two_root_degree = 511 + 256 * 512
    hypothetical_three_root_degree = 511 + 255 * 512
    agreement = 273 * 512 + 511
    assert two_root_degree == 131583 > DEGREE_CEILING
    assert hypothetical_three_root_degree == DEGREE_CEILING
    assert agreement == 140287 > 139782
    print("baseline_272_14", baseline)
    print("candidate_273_14", candidate)
    print("candidate_273_15", overkeyed)
    print("required_strictly_more_than", REQUIRED)
    print("two_root_degree_bound", two_root_degree)
    print("hypothetical_three_root_degree_bound", hypothetical_three_root_degree)
    print("agreement", agreement)
    print("PASS: counting survives 273 fibres; third root remains unproved")

if __name__ == "__main__":
    main()
