#!/usr/bin/env python3
"""Exact score-only gate for official Koala ProtocolClaimUpper.
No attack construction, Lean certificate, or verifier acceptance is claimed.
For 2^(-B/100) <= (1-i/2^18)^128, raise to 100:
2^B * (2^18-i)^12800 >= (2^18)^12800.
"""
N=1<<18
MAX_I=1<<17
def score_ok(bits,index):
    assert 1<=index<=MAX_I and bits>=0
    return (1<<bits)*pow(N-index,12800)>=pow(N,12800)
def maximum_index(bits):
    lo,hi=1,MAX_I
    assert score_ok(bits,lo)
    while lo<hi:
        mid=(lo+hi+1)//2
        if score_ok(bits,mid):lo=mid
        else:hi=mid-1
    assert score_ok(bits,lo)
    if lo<MAX_I:assert not score_ok(bits,lo+1)
    return lo
def main():
    previous_index=122369
    assert score_ok(11613,previous_index)
    assert not score_ok(11612,previous_index)
    assert maximum_index(11613)==122370
    assert maximum_index(11612)==122362
    assert score_ok(11612,122362)
    assert not score_ok(11612,122363)
    print("Official Koala upper: published ProtocolClaimUpper 11613 122369")
    print("116.13 arithmetic maximum unsafe index:",maximum_index(11613))
    print("116.12 arithmetic maximum unsafe index:",maximum_index(11612))
    print("116.12 at old index: FAIL")
    print("New 116.12 requires certified unsafe suffix starting at i<=122362")
    print("At least 7 extra agreement positions needed versus old i=122369")
    print("Necessary score gate only; no new unsafeAbove proof.")
if __name__=="__main__":main()
