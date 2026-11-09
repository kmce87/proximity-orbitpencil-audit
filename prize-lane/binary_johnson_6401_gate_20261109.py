#!/usr/bin/env python3
"""Falsify classical rate-1/2 Johnson-radius route to binary 64.01 bits.
Only an exact necessary-radius comparison, not a decoding impossibility proof.
"""
from fractions import Fraction
B=6401
Q=2**28
def score_ok(P):
    return (Q-P)**(128*100)*2**B <= Q**(128*100)
lo,hi=0,Q
while lo<hi:
    mid=(lo+hi)//2
    if score_ok(mid): hi=mid
    else: lo=mid+1
P=lo
assert score_ok(P) and not score_ok(P-1)
assert 2*(Q-P)**2 < Q**2
print('64.01-bit minimum grid numerator at Q=2^28:',P)
print('radius:',Fraction(P,Q))
print('exceeds classical rate-1/2 Johnson radius: YES')
print('Does not rule out stronger, non-Johnson soundness arguments.')
