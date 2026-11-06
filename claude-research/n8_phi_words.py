#!/usr/bin/env python3
"""N8: words of ker Phi_j as functions on the dual and the distance from the T_W words R_W = W^perp.  Word of 2^t x_T: chi -> prod_(i in T) chi_i."""
import sys, itertools
from n8_phi import *
def word_table(ker_elt,names,n):
    # truth table on 2^n characters as python int bitmask
    N=1<<n
    tab=0
    for k,(t,T) in enumerate(names):
        if ker_elt>>k&1:
            m=0
            for chi in range(N):
                if all(chi>>i&1 for i in T):m|=1<<chi
            tab^=m
    return tab
def weights_of_kernel(ell,j,limit=1<<16):
    vecs,names=phi(ell,j);kd,ker=kernel_dim(vecs,want=True)
    n=len(ell)
    tabs=[word_table(k,names,n) for k in ker]
    return kd,ker,names,tabs
def span_tables(tabs):
    out=[0]
    for t in tabs:
        out+= [x^t for x in out]
    return out
def subspaces_W_perp(n):
    """all 4-dim subspaces of the dual, as truth tables (W^perp through 0): only for small n"""
    N=1<<n;seen=set();out=[]
    def rref_span(gens):
        s={0}
        for g in gens:
            s|={x^g for x in s}
        return frozenset(s)
    for a in range(1,N):
        for b in range(a+1,N):
            s2={0,a,b,a^b}
            if len(s2)<4:continue
            if min(s2-{0})!=a:continue
            for c in range(b+1,N):
                if c in s2:continue
                s3=s2|{x^c for x in s2}
                if min(s3-s2)!=c:continue
                for d in range(c+1,N):
                    if d in s3:continue
                    s4=frozenset(s3|{x^d for x in s3})
                    if s4 in seen:continue
                    seen.add(s4)
                    m=0
                    for x in s4:m|=1<<x
                    out.append(m)
    return out
if __name__=="__main__":
    n=int(sys.argv[1]);mode=sys.argv[2]
    if mode=="kry":ell=[1<<i for i in range(n)]
    else:
        z=int(mode,16)
        # f' = 1: labels u^2 + z u on the non-pivot monomials of D = P_(n+1)
        piv=z.bit_length()-1
        ell=[mul(1<<i,1<<i)^mul(z,1<<i) for i in range(n+1) if i!=piv]
    kd,ker,names,tabs=weights_of_kernel(ell,n-4)
    print("n",n,"ker dim",kd)
    allw=span_tables(tabs)
    hist={}
    for t in allw:
        w=bin(t).count("1");hist[w]=hist.get(w,0)+1
    print("kernel word weights:",sorted(hist.items()))
    if n<=7:
        Ws=subspaces_W_perp(n)
        print("number of W:",len(Ws))
        res={}
        for w in Ws:
            best=[]
            for t in allw:
                if t==0:continue
                best.append(bin(w^t).count("1"))
            for b in best:res[b]=res.get(b,0)+1
        print("weights of R_W + k (k != 0), over all W:",sorted(res.items()))
