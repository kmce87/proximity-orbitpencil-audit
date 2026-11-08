#!/usr/bin/env python3
"""Exact BF64 Gold-form polar rank gate on the protected 21-bit domain.
This is NOT a Lean proof or an accepted Proximity Prize certificate.
"""
from collections import Counter
MOD=(1<<64)|(1<<4)|(1<<3)|(1<<1)|1

def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a>>64:a^=MOD
    return z

def trace(a):
    z=0
    for _ in range(64):
        z^=a;a=mul(a,a)
    assert z in (0,1)
    return z

def matrix(a):
    rows=[]
    for i in range(21):
        row=0
        for j in range(21):
            if i!=j and trace(mul(a,(1<<(2*i+j))^(1<<(i+2*j)))):
                row|=1<<j
        rows.append(row)
    assert all((rows[i]>>j&1)==(rows[j]>>i&1) for i in range(21) for j in range(21))
    assert all(not(rows[i]>>i&1) for i in range(21))
    return rows

def rank(rows):
    rows=rows.copy();p=0
    for bit in range(21):
        k=next((i for i in range(p,21) if rows[i]>>bit&1),None)
        if k is None:continue
        rows[p],rows[k]=rows[k],rows[p]
        for j in range(21):
            if j!=p and rows[j]>>bit&1:rows[j]^=rows[p]
        p+=1
    return p

if __name__=='__main__':
    basis=[matrix(1<<i) for i in range(64)]
    candidates=[1<<i for i in range(64)]+[(1<<i)^(1<<j) for i in range(64) for j in range(i+1,64)]
    counts=Counter();best=(None,99)
    for a in candidates:
        rows=[0]*21
        for i in range(64):
            if a>>i&1:rows=[x^y for x,y in zip(rows,basis[i])]
        r=rank(rows)
        assert r%2==0 and r<=20
        counts[r]+=1
        if r<best[1]:best=(a,r)
    print('modulus',hex(MOD),'domain GF(2)-span(1,x,...,x^20)')
    print('Q_a(x)=Tr(a*x^3), coefficients tested:',len(candidates))
    print('polar rank histogram:',dict(sorted(counts.items())))
    print('minimum rank witness:',hex(best[0]),best[1])
    assert best==(1,0)
    assert counts=={0:3,2:26,4:58,6:84,8:111,10:138,12:188,14:452,16:551,18:337,20:132}
    print('RESULT: uniform rank >=20 fails on explicit tested coefficients')
