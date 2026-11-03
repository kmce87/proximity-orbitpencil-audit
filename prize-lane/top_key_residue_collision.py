#!/usr/bin/env python3
"""Exact 256-column OrbitPencil obstruction: equal 6 top coefficients need
NOT imply equal constant coefficients. A falsification of an automatic
product-key collapse, NOT a complete impossibility proof for conditional
key distributions and NOT a prize certificate."""
from math import comb
P=2130706433
ETA=pow(3,(P-1)//256,P)

def coefficients(U):
    c=[1]
    for b in sorted(U):
        root=pow(ETA,b,P)
        nxt=[0]*(len(c)+1)
        for i,v in enumerate(c):
            nxt[i]=(nxt[i]-root*v)%P
            nxt[i+1]=(nxt[i+1]+v)%P
        c=nxt
    return c

def coset(r):
    return {r+32*j for j in range(8)}

def main():
    assert pow(ETA,256,P)==1 and pow(ETA,128,P)!=1
    for r in (1,17,18,31):
        c=coefficients(coset(r))
        assert c[0]==(-pow(ETA,8*r,P))%P and c[1:8]==[0]*7 and c[8]==1
    # Every union of 17 distinct nonzero 8-cosets produces V_U(T)
    # as a polynomial in T^8; coefficients at degrees 135..130 are zero.
    U=set().union(*(coset(r) for r in range(1,18)))
    W=set().union(*(coset(r) for r in list(range(1,17))+[18]))
    assert len(U)==len(W)==136 and 0 not in U and 0 not in W
    u,w=coefficients(U),coefficients(W)
    assert all(u[d]==w[d]==0 for d in range(130,136))
    su,sw=sum(U)%256,sum(W)%256
    assert (su,sw)==(72,80)
    assert u[0]==pow(ETA,su,P) and w[0]==pow(ETA,sw,P) and u[0]!=w[0]

    # Exact DP: all choose(31,17) unions have the same top-six key,
    # but their product residues range across all 32 multiples of 8.
    dp=[[0]*32 for _ in range(18)]
    dp[0][0]=1
    for r in range(1,32):
        for j in range(17,0,-1):
            for t in range(32):
                dp[j][(t+r+16)%32]+=dp[j-1][t]
    counts=dp[17]
    assert sum(counts)==comb(31,17)==265182525
    assert all(c>0 for c in counts)
    B=P**6//2**128
    assert sum(counts)<B+1
    print(f'prime={P} eta={ETA}')
    print('top six matching coefficients degrees 135..130: all zero')
    print(f'product residues={su},{sw}; constants={u[0]},{w[0]}')
    print(f'whole-8-coset family={sum(counts)}; target slopes={B+1}')
    print(f'number of different product residues with SAME top-six key={sum(c>0 for c in counts)}')
    print(f'exact per-residue count: min={min(counts)} max={max(counts)}')
    print('PASS: top-six key does NOT determine product residue.')
    print('Not an official improved attack; general conditional concentration remains open.')

if __name__=='__main__':
    main()
