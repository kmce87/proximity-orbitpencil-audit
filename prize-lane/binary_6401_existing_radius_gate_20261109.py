#!/usr/bin/env python3
"""Exact score feasibility at the published binary lower candidate radius.
Source: proximity-prize/proximity-prize, main,
ProximityPrize/SubmissionBinaryLower/Solution.lean
No Lean proof or independent acceptance is claimed.
"""
P, Q, T = 78622925, 268435456, 128
def score_passes(B):
    # ((Q-P)/Q)^T <= 2^(-B/100)
    # Raise both sides to the 100th power, then clear denominator.
    return ((Q-P)**(T*100)) * (2**B) <= Q**(T*100)
assert score_passes(6400)
assert not score_passes(6401)
print("PASS: 64.00 bits at existing binary radius")
print("FAIL: 64.01 bits at the same radius")
print("No improvement; changing score metadata alone cannot work.")
