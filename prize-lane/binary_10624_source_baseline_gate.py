#!/usr/bin/env python3
"""Lane B source-audit gate, 2026-11-06.  Not a Lean proof or service acceptance.

Official binary upper source (pre-existing, attributed to BitWonka):
https://github.com/proximity-prize/proximity-prize/blob/eb82d3bf04a9c876c7ef9c3e6de4640fb85062f2/ProximityPrize/SubmissionBinaryUpper/Solution.lean
Source theorem: ProtocolClaimUpper 10624 917441
Source support: CorePencil.Jset_card = 1179711
"""
N = 2 ** 21
HALF_PLUS_ONE = 2 ** 20 + 1
SOURCE_SCORE = 10624
SOURCE_INDEX = 917441
CORE_SIZE = 63
LABELS = 18432
FIBRE = 64

def valid_score(B, i):
    """Exact 2^(-B/100) <= ((N-i)/N)^128."""
    assert 0 < i < HALF_PLUS_ONE
    return (2 ** B) * ((N - i) ** 12800) >= N ** 12800

def max_index(B):
    low, high = 1, HALF_PLUS_ONE - 1
    while low < high:
        mid = (low + high + 1) // 2
        if valid_score(B, mid):
            low = mid
        else:
            high = mid - 1
    return low

if __name__ == "__main__":
    assert CORE_SIZE + LABELS * FIBRE == 1179711
    assert N - SOURCE_INDEX == 1179711
    assert SOURCE_SCORE < 12799  # supersedes previous proposed binary target
    assert valid_score(SOURCE_SCORE, SOURCE_INDEX)
    assert max_index(SOURCE_SCORE) == 917442
    assert not valid_score(10623, SOURCE_INDEX)
    assert max_index(10623) == 917378
    assert valid_score(10623, 917378) and not valid_score(10623, 917379)
    assert N - 917378 == 1179774
    assert 1179774 - 1179711 == 63
    print("Existing source: ProtocolClaimUpper 10624 917441 (not service-verified)")
    print("Next arithmetic target: ProtocolClaimUpper 10623 917378")
    print("Current 63 + 18432*64 support is short by 63 positions.")
    print("No new unsafeAbove proof, Lean kernel check, or verifier acceptance.")
