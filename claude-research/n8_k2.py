#!/usr/bin/env python3
"""N8: the merge kernel at n = 6.  Phi_2: I^2/I^3 -> K^2, Phi_2(x_a x_b) = (l_a l_b, l_a^2 l_b + l_a l_b^2), Phi_2(2 x_a) = (l_a^2, 0).
S, S' (same e1) share the top X^36 + 0 + e2 X^34 + e3 X^33 iff 1_S - 1_S' is in I^3 + ker Phi_2.  Words: quadratic forms on V* (the residue set R + R')."""
import random, sys, itertools
POLY=(1<<64)|0x1B
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a>>64:a^=POLY
    return r
def phi_vectors(ell):
    n=len(ell);out=[];names=[]
    for i in range(n):
        out.append((mul(ell[i],ell[i]),0));names.append(("b",i))
    for i,j in itertools.combinations(range(n),2):
        a,b=ell[i],ell[j]
        out.append((mul(a,b),mul(mul(a,a),b)^mul(a,mul(b,b))));names.append(("a",i,j))
    return out,names
def kernel(ell):
    vs,names=phi_vectors(ell)
    # gaussian elimination over F_2 on 128-bit vectors with tracking
    piv={};ker=[]
    for k,(c,p) in enumerate(vs):
        v=(c<<64)|p;t=1<<k
        while v:
            h=v.bit_length()-1
            if h in piv:
                v^=piv[h][0];t^=piv[h][1]
            else:
                piv[h]=(v,t);break
        if v==0:ker.append(t)
    return ker,names
def show(t,names):
    return " + ".join(("2x%d"%m[1]) if m[0]=="b" else ("x%dx%d"%(m[1],m[2])) for k,m in enumerate(names) if t>>k&1)
if __name__=="__main__":
    rnd=random.Random(1)
    ell=[1<<i for i in range(6)]
    ker,names=kernel(ell)
    print("Krylov (1,x,..,x^5): dim ker =",len(ker))
    for t in ker:print("  ",show(t,names))
    mu=rnd.getrandbits(64);lam=rnd.getrandbits(64)
    ell2=[];p=lam
    for i in range(6):
        ell2.append(p);p=mul(p,mu)
    ker,names=kernel(ell2);print("chain lam*mu^i, random lam, mu: dim ker =",len(ker))
    for t in ker:print("  ",show(t,names))
    ell3=[rnd.getrandbits(64) for _ in range(6)]
    print("random labels: dim ker =",len(kernel(ell3)[0]))
    # shorter chains
    for pattern in [(5,1),(4,2),(3,3),(4,1,1),(3,2,1),(2,2,2)]:
        ell4=[]
        for L in pattern:
            p=rnd.getrandbits(64)
            for i in range(L):
                ell4.append(p);p=mul(p,mu)
        print("chains of lengths",pattern,"same mu: dim ker =",len(kernel(ell4)[0]))
