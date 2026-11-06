#!/usr/bin/env python3
"""N8: the structural kernel word at r = 8 (Y = q*P_f, q = L_2 = x^2(x+1)^2(x^2+x+1) = 0x6c, any f >= 1, any field): weight, Walsh spectrum, distance to the T_W words,
restriction to hyperplanes.  Run for the real domain f' = 13 and for f' = 1."""
import sys, itertools
from n8_phi import *
from n8_phi_ideal import labels_quot, clmul
from n8_phi_words import word_table
def rref_subspaces(n,k):
    # all k-dim subspaces of F_2^n by RREF
    for pivs in itertools.combinations(range(n),k):
        free=[]
        for r,p in enumerate(pivs):
            for b in range(p):
                if b not in pivs: free.append((r,b))
        for mask in range(1<<len(free)):
            B=[1<<p for p in pivs]
            for i,(r,b) in enumerate(free):
                if mask>>i&1:B[r]^=1<<b
            yield B
def table_of_span(B):
    s=[0]
    for g in B:s+=[x^g for x in s]
    m=0
    for x in s:m|=1<<x
    return m
def walsh_hist(tab,n):
    N=1<<n;a=[1-2*((tab>>i)&1) for i in range(N)]
    for b in range(n):
        for i in range(N):
            if i>>b&1:
                x,y=a[i^(1<<b)],a[i];a[i^(1<<b)],a[i]=x+y,x-y
    h={}
    for v in a:h[v]=h.get(v,0)+1
    return sorted(h.items())
for f in [int(a) for a in sys.argv[1:]]:
    Y=[clmul(0x6c,1<<i) for i in range(f)]
    ell=labels_quot(Y,8+f)
    vecs,names=phi(ell,4);kd,ker=kernel_dim(vecs,want=True)
    k=word_table(ker[0],names,8)
    print("f'",f,"ker",kd,"weight",bin(k).count("1"),"contains 0:",k&1,"Walsh (+-1 form) histogram",walsh_hist(k,8))
    best={}
    for B in rref_subspaces(8,4):
        w=bin(table_of_span(B)^k).count("1")
        best[w]=best.get(w,0)+1
    print("  weights of R_W + k over all 200787 W^perp:",sorted(best.items())[:8])
