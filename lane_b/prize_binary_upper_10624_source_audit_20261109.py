#!/usr/bin/env python3
"""Exact arithmetic audit of official binary upper source candidate.
Not a Lean kernel check, nor evidence of independent acceptance.
Source: proximity-prize/proximity-prize
ProximityPrize/SubmissionBinaryUpper/Solution.lean
"""
I,N,T,B=917441,2097152,128,10624
assert N-I==1179711
def valid(b):
    # 2^(-b/100) <= ((N-I)/N)^T
    # raise to 100 and clear denominators
    return N**(T*100) <= 2**b * (N-I)**(T*100)
assert valid(10624)
assert not valid(10623)
assert I < N//2
print("PASS: binary upper 106.24 score inequality at index 917441")
print("FAIL: binary upper 106.23 at unchanged index")
print("No check of unsafeAbove or admissibility; no Lean replay.")
