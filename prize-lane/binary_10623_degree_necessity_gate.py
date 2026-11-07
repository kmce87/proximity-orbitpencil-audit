#!/usr/bin/env python3
"""Exact binary 106.23 score gate and necessary leading-coefficient test.
Not a Lean proof, new construction, or independently verified submission.
Source: proximity-prize/proximity-prize, SubmissionBinaryUpper/CorePencil.lean
"""
N=2**21
SOURCE_INDEX=917441
TARGET_INDEX=917378
SOURCE_SCORE=10624
TARGET_SCORE=10623

def score_ok(bits,index):
    return 2**bits * (N-index)**12800 >= N**12800

def max_index(bits):
    lo,hi=0,N//2
    while lo<hi:
        mid=(lo+hi+1)//2
        if score_ok(bits,mid):lo=mid
        else:hi=mid-1
    return lo

assert max_index(TARGET_SCORE)==TARGET_INDEX
assert score_ok(TARGET_SCORE,TARGET_INDEX)
assert not score_ok(TARGET_SCORE,TARGET_INDEX+1)
assert N-TARGET_INDEX==1179774
assert N-SOURCE_INDEX==1179711
assert (N-TARGET_INDEX)-(N-SOURCE_INDEX)==63
assert 126+64*16383==1048638
assert 126+64*16382==1048574
assert 63+64*16383==1048575
# For nonzero f in any field, division by monic (X-a) preserves leading coefficient
# and reduces degree by 1. Consequently if CF has degree 16384,
# Q=(CF-gamma)/(X-alpha) has degree 16383, so the existing bound for
# a 126-point core cannot guarantee a codeword of degree < 1048576.
# A degree <=16382 quotient requires CF degree <=16383; for CF degree <=16384
# this is equivalent to vanishing of its X^16384 coefficient.
print('PASS: 106.23 upper index = 917378; extra agreement = 63')
print('Necessary gate for 126-point core: coeff(CF,16384)=0, or a different degree/cancellation argument')
print('NO new construction, Lean proof, or independent verifier acceptance')
