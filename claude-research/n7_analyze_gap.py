#!/usr/bin/env python3
"""N7: analyze a word found by n7_gap.  Usage: n7_analyze_gap.py n g seed lam0 ... (hex).
Lists members T (complements of S), their error supports, structure: sums, pair structure, Hankel minimal polynomials."""
import sys,itertools
from collections import Counter
from n7_analyze import MT64,mul,inv
def main():
    n=int(sys.argv[1]);g=int(sys.argv[2]);seed=int(sys.argv[3]);lam=[int(x,16) for x in sys.argv[4:]]
    N=2**n;D=N//2;c=N-D-g;LEN=c+g-1
    assert len(lam)==LEN
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
    def Lam(P,shift=0):
        s=0
        for j,a in enumerate(P):
            s^=mul(lam[j+shift],a)
        return s
    members=[]
    for T in itertools.combinations(range(N),c):
        L=locator(T)
        if all(Lam(L,i)==0 for i in range(g-1)):
            sup=tuple(t for t in T if Lam(locator([u for u in T if u!=t])))
            members.append((T,sup))
    print("members",len(members),"distinct supports",len(set(s for _,s in members)))
    bysup={}
    for T,s in members:bysup.setdefault(s,[]).append(T)
    for s,Ts in sorted(bysup.items(),key=lambda kv:(len(kv[0]),kv[0])):
        x=0
        for t in s:x^=t
        print("  support",s,"xor",x,"#T",len(Ts))
    # Hankel: minimal Q
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
    prev=0
    for e in range(0,LEN+1):
        rows=[[lam[i+j] for j in range(e+1)] for i in range(0,LEN-e)]
        ns=nullspace(rows,e+1) if rows else [[1 if j==k else 0 for j in range(e+1)] for k in range(e+1)]
        print(" e=%d: dim R_e=%d"%(e,len(ns)),end=';')
        if len(ns)>prev+(1 if prev else 0) or (prev==0 and ns):
            print("\n   basis:",[[hex(a) for a in v] for v in ns][:2])
        prev=len(ns)
    print()
if __name__=="__main__":main()
