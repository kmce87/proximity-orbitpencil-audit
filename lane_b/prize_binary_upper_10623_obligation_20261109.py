#!/usr/bin/env python3
"""Exact necessary grid index for binary upper 106.23 bits; no proof claimed."""
N,T,B=2**21,128,10623
def score_ok(i):
    return N**(T*100) <= 2**B*(N-i)**(T*100)
lo,hi=1,N//2
assert score_ok(lo)
while lo<hi:
    mid=(lo+hi+1)//2
    if score_ok(mid): lo=mid
    else: hi=mid-1
i=lo
assert score_ok(i) and not score_ok(i+1)
assert i==917378
print("Maximum unsafeIndex:",i)
print("Extra grid positions:",917441-i)
print("No unsafeAbove proof or verifier acceptance.")
