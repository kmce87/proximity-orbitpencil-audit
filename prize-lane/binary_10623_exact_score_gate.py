#!/usr/bin/env python3
"""Exact, integer-only binary upper score gate, official Lean 4.34 profile.
No floating-point, no Lean certificate, no independent verifier acceptance.
Source: proximity-prize/proximity-prize:
  ProximityPrize/Benchmark/BinaryTargetUpper.lean
  ProximityPrize/SubmissionBinaryUpper/{score.txt,unsafe-index.txt}
"""
N = 2**21
T = 128
CURRENT_INDEX = 917441
CURRENT_BITS = 10624
PROPOSED_BITS = 10623

def score_holds(bits: int, index: int) -> bool:
    """2^(-bits/100) <= ((N-index)/N)^128.
    Raise both sides to 100, clear powers of 2 exactly."""
    return (N-index)**(T*100) * 2**bits >= N**(T*100)

def largest_index(bits: int) -> int:
    lo, hi = 0, N//2
    while lo < hi:
        mid = (lo + hi + 1)//2
        if score_holds(bits,mid):lo=mid
        else:hi=mid-1
    return lo

def main():
    assert score_holds(CURRENT_BITS,CURRENT_INDEX)
    assert not score_holds(PROPOSED_BITS,CURRENT_INDEX)
    assert largest_index(CURRENT_BITS)==917442
    assert largest_index(PROPOSED_BITS)==917378
    i=largest_index(PROPOSED_BITS)
    assert score_holds(PROPOSED_BITS,i)
    assert not score_holds(PROPOSED_BITS,i+1)
    print("PASS: exact integer score inequality (no rounding)")
    print(f"Published binary source: {CURRENT_BITS/100:.2f} bits at unsafe index {CURRENT_INDEX}")
    print(f"Proposed {PROPOSED_BITS/100:.2f}-bit score requires unsafe index <= {i}")
    print(f"Required additional agreement over source index: {CURRENT_INDEX-i}")
    print(f"Source threshold agreement N-index: {N-CURRENT_INDEX}")
    print(f"Target threshold agreement N-index: {N-i}")
    print("This is NECESSARY score arithmetic, not an upper winning-set proof.")
    print("Independent prize verifier acceptance: NO")
if __name__=="__main__":
    main()
