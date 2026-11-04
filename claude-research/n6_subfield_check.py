#!/usr/bin/env python3
"""Non-generic labels? dim(V cap g V) for g generating each subfield of BF64, V = D (domain) and V = labels L_Z(D), Z = first 2^f words."""
POLY=(1<<64)|0x1B
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a>>64:a^=POLY
    return r
def pw(a,e):
    r=1
    while e:
        if e&1:r=mul(r,a)
        a=mul(a,a);e>>=1
    return r
def rank(vs):
    b={}
    for v in vs:
        while v:
            h=v.bit_length()-1
            if h in b:v^=b[h]
            else:
                b[h]=v;break
    return len(b)
def subspace_poly(basis):
    # returns coefficients c[i] of X^(2^i)
    P=[1]
    def ev(P,x):
        r=0;p=x
        for c in P:
            if c:r^=mul(c,p)
            p=mul(p,p)
        return r
    for u in basis:
        c=ev(P,u);Q=[0]*(len(P)+1)
        for i,a in enumerate(P):
            Q[i+1]^=mul(a,a);Q[i]^=mul(c,a)
        P=Q
    return P,ev
D=[1<<i for i in range(21)]
assert rank(D)==21
N=(1<<64)-1
# generator of the multiplicative group: 2^64-1 = 3*5*17*257*641*65537*6700417
primes=[3,5,17,257,641,65537,6700417]
g=next(c for c in range(2,1000) if all(pw(c,N//p)!=1 for p in primes))
for k in (2,4,8,16,32):
    z=pw(g,N//(2**k-1))
    assert pw(z,2**k)==z
    out=[f"F_(2^{k}):"]
    for name,V in [("D",D)]+[(f"f={f}",None) for f in (6,7,8)]:
        if V is None:
            f=int(name[2:]);P,ev=subspace_poly(D[:f]);V=[ev(P,x) for x in D[f:]]
            assert rank(V)==21-f
        dim=2*len(V)-rank(V+[mul(z,v) for v in V])
        out.append(f"{name}: dim(V cap zV)={dim}")
    print(" ".join(out))
