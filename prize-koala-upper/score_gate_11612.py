#!/usr/bin/env python3
"""Exact Koala upper score gate; no unsafeAbove proof asserted."""
N=1<<18
T=128
def holds(b,i):
    assert 0<i<=N//2
    return (1<<b)*(N-i)**(100*T)>=N**(100*T)
def max_index(b):
    lo,hi=1,N//2
    while lo<hi:
        mid=(lo+hi+1)//2
        if holds(b,mid):lo=mid
        else:hi=mid-1
    return lo
if __name__=="__main__":
    assert holds(11613,122369)
    assert not holds(11612,122369)
    assert max_index(11613)==122370
    assert max_index(11612)==122362
    assert holds(11612,122362) and not holds(11612,122363)
    print("116.12 maximum score-admissible index: 122362")
    print("Need unsafeAbove for indices 122362..122368, beyond existing 122369 suffix")
    print("Numerical gate only; no Lean kernel or independent verifier acceptance")
