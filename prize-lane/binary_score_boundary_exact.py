#!/usr/bin/env python3
"""Exact integer gate for binary ProtocolClaimUpper.score, NOT unsafeAbove.

For B=10623, index i and n=2^21, the official score inequality
2^(-B/100) <= (1-i/n)^128 is equivalent, by taking the 100th power,
to 2^B*(n-i)^12800 >= n^12800.
"""
N=1<<21
B=10623
E=12800
rhs=N**E
def score_ok(i):
    assert 0<i<N//2
    return (1<<B)*(N-i)**E >= rhs
assert score_ok(917378)
assert not score_ok(917379)
assert score_ok(917377)
assert not score_ok(917441)
print("PASS: 917378 is the largest grid index satisfying the 106.23-bit score inequality")
print("FAIL (expected): 917379 violates score inequality; unsafeAbove cannot rescue it")
print("This proves neither winning-set density nor Lean kernel acceptance.")
