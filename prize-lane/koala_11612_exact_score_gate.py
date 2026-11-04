#!/usr/bin/env python3
"""Exact integer score-boundary gate for protected Koala upper certificate.
No winning-set proof, Lean compilation, or verifier acceptance claimed.
"""
N=262144

def score_holds(B,i):
    # 2^(-B/100) <= ((N-i)/N)^128; raise both sides to 100.
    return N**12800 <= (N-i)**12800 * 2**B

def max_index(B):
    lo,hi=0,N-1
    while lo<hi:
        mid=(lo+hi+1)//2
        if score_holds(B,mid): lo=mid
        else: hi=mid-1
    return lo

if __name__=="__main__":
    for B in (11613,11612,11546):
        i=max_index(B)
        assert score_holds(B,i) and not score_holds(B,i+1)
        print(f"B={B}: largest score-admissible index {i}; next {i+1} fails")
    assert not score_holds(11612,122369)
    assert score_holds(11613,122369)
    assert max_index(11612)==122362
    print("116.12 requires suffix start <=122362, seven steps before 122369.")
