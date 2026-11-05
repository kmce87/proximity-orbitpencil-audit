#!/usr/bin/env python3
"""N7: analyze a non-top hyperplane class found by n7_hyper at n=4.
Usage: n7_analyze.py n seed lam0 ... lamc   (hex, the order printed by n7_hyper).
Prints the class size, structure of T's and S's: sums, Walsh spectrum, translation stabiliser, Hankel minimal degrees (d1,d2)."""
import sys,itertools
from collections import Counter
class MT64:
    def __init__(s,seed):
        s.mt=[seed&((1<<64)-1)]
        for i in range(1,312):
            s.mt.append((6364136223846793005*(s.mt[-1]^(s.mt[-1]>>62))+i)&((1<<64)-1))
        s.i=312
    def __call__(s):
        if s.i>=312:
            for k in range(312):
                y=(s.mt[k]&0xFFFFFFFF80000000)|(s.mt[(k+1)%312]&0x7FFFFFFF)
                s.mt[k]=s.mt[(k+156)%312]^(y>>1)^(0xB5026F5AA96619E9 if y&1 else 0)
            s.i=0
        y=s.mt[s.i];s.i+=1
        y^=(y>>29)&0x5555555555555555
        y^=(y<<17)&0x71D67FFFEDA60000
        y^=(y<<37)&0xFFF7EEE000000000
        y^=y>>43
        return y&((1<<64)-1)
MOD=(1<<32)|(1<<22)|7
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        a<<=1
        if a>>32:a^=MOD
        b>>=1
    return r
def inv(a):
    r=1;b=a;e=0xfffffffe
    while e:
        if e&1:r=mul(r,b)
        b=mul(b,b);e>>=1
    return r
def main():
    n=int(sys.argv[1]);seed=int(sys.argv[2]);lam=[int(x,16) for x in sys.argv[3:]]
    N=2**n;D=N//2;c=N-D-2
    assert len(lam)==c+1
    rng=MT64(seed);basis=[rng()&0xffffffff for _ in range(n)]
    lab=[0]*N
    for v in range(N):
        for i in range(n):
            if v>>i&1:lab[v]^=basis[i]
    def locator(T):
        P=[1]
        for t in T:
            Q=[0]*(len(P)+1)
            for j,a in enumerate(P):
                Q[j+1]^=a
                Q[j]^=mul(a,lab[t])
            P=Q
        return P
    def Lam(P):
        s=0
        for j,a in enumerate(P):
            s^=mul(lam[j],a)
        return s
    # note: Lambda is applied with P's coefficient of X^j paired with lam[j]
    zeros=[]
    for T in itertools.combinations(range(N),c):
        if Lam(locator(T))==0:zeros.append(T)
    print("zeros",len(zeros))
    masks=[sum(1<<t for t in T) for T in zeros]
    # error supports
    sup=Counter()
    for T in zeros:
        s=tuple(t for t in T if Lam(locator([u for u in T if u!=t])))
        sup[s]+=1
    print("distinct supports",len(sup),"support sizes",Counter(len(s) for s in sup))
    # sums of T
    def xs(T):
        x=0
        for t in T:x^=t
        return x
    print("sum(T) histogram",sorted(Counter(xs(T) for T in zeros).items()))
    # point degree
    deg=Counter()
    for T in zeros:
        for t in T:deg[t]+=1
    print("point degrees",[deg[v] for v in range(N)])
    # stabiliser under translations
    Z=set(masks)
    for u in range(1,N):
        im=sum(1 for T in zeros if sum(1<<(t^u) for t in T) in Z)
        print(" translate by",u,"keeps",im)
    # Hankel minimal degrees
    # Q of degree e with Lam(X^i Q)=0 for i=0..c-e : find smallest e
    def nullspace(rows,ncols):
        rows=[r[:] for r in rows];piv=[];r=0
        for col in range(ncols):
            p=next((i for i in range(r,len(rows)) if rows[i][col]),None)
            if p is None:continue
            rows[r],rows[p]=rows[p],rows[r]
            iv=inv(rows[r][col]);rows[r]=[mul(iv,a) for a in rows[r]]
            for i in range(len(rows)):
                if i!=r and rows[i][col]:
                    f=rows[i][col];rows[i]=[a^mul(f,b) for a,b in zip(rows[i],rows[r])]
            piv.append(col);r+=1
        free=[j for j in range(ncols) if j not in piv]
        out=[]
        for f in free:
            v=[0]*ncols;v[f]=1
            for i,p in enumerate(piv):v[p]=rows[i][f]
            out.append(v)
        return out
    for e in range(0,c+2):
        # unknown Q coefficients q_0..q_e, conditions i=0..c-e
        rows=[]
        for i in range(0,c-e+1):
            rows.append([lam[i+j] for j in range(e+1)])
        ns=nullspace(rows,e+1) if rows else [[1 if j==k else 0 for j in range(e+1)] for k in range(e+1)]
        print(" e=%d: dim R_e=%d"%(e,len(ns)),end=';')
        if ns and e<=c and (not 'first' in dir()):
            first=ns
            print("\n minimal Q coefficients",[hex(a) for a in ns[0]])
    print()
    return zeros,lab,lam
if __name__=="__main__":main()
