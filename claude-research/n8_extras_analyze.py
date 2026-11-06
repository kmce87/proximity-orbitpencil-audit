#!/usr/bin/env python3
"""N8: analyze explicit extra members of the n = 6 class for given labels: exact top check in BF64, Walsh spectrum, residues."""
import sys, collections
POLY=(1<<64)|0x1B
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a>>64:a^=POLY
    return r
def lab(ell,v):
    x=0
    for i,e in enumerate(ell):
        if v>>i&1:x^=e
    return x
def top(ell,mask):
    e1=e2=e3=0
    for v in range(64):
        if mask>>v&1:
            p=lab(ell,v)
            e3^=mul(p,e2);e2^=mul(p,e1);e1^=p
    return e1,e2,e3
def walsh(mask):
    f=[1 if mask>>v&1 else 0 for v in range(64)]
    a=[(-1)**x if False else x for x in f]
    a=f[:]
    for b in range(6):
        for i in range(64):
            if i>>b&1:
                x,y=a[i^(1<<b)],a[i]
                a[i^(1<<b)],a[i]=x+y,x-y
    return a
if __name__=="__main__":
    fn=sys.argv[1];ell=[int(x,16) for x in sys.argv[2].split(',')];w1,w2=int(sys.argv[3]),int(sys.argv[4])
    # L_W
    a1,a2=lab(ell,w1),lab(ell,w2)
    # X^4 + aX^2 + bX: a = a1^2+a1 a2+a2^2, b = a1 a2 (a1+a2)
    a=mul(a1,a1)^mul(a1,a2)^mul(a2,a2);b=mul(mul(a1,a2),a1^a2)
    masks=[int(l,16) for l in open(fn).read().split()]
    bad=0;hist=collections.Counter();odd=collections.Counter();rs=collections.Counter()
    for m in masks:
        assert bin(m).count('1')==36
        if top(ell,m)!=(0,a,b):bad+=1
        W=walsh(m)
        hist[tuple(sorted(collections.Counter(W[1:]).items()))]+=1
        R=tuple(chi for chi in range(64) if W[chi]%8)
        rs[R]+=1
    print("samples",len(masks),"top failures",bad)
    print("distinct Walsh value profiles",len(hist))
    for k,c in hist.most_common(6):print(c,k)
    print("distinct residue sets (Walsh not divisible by 8):",len(rs))
    for k,c in rs.most_common(10):print(c,k)
