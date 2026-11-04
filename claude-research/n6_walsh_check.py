#!/usr/bin/env python3
"""N6 (a): gap >= 2^(k-1) <=> 2^k divides all Walsh coefficients of 1_S - 1_S' (generic labels).
1. Exhaustive at n = 4, |S| = 9 and |S| = 8: grouping by top coefficients of V_S equals grouping by Walsh residues.
2. Leading coefficient formula: for independent w_1..w_j, P(x_w1...x_wj) = 1 + c X^(-2^(j-1)) + ..., c = prod over odd subsets U of l(sum_U w).
3. Injectivity on I^j/I^(j+1): the polynomials c(2^t x_T) in F_2[l_1..l_n] have distinct leading monomials (exact, n <= 7)."""
import itertools,random
from collections import defaultdict
POLY,MB=0x1002B,16
EXP=[0]*(2*65536);LOG=[0]*65536
def rawmul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a>>MB:a^=POLY
    return r
def rawpow(a,e):
    r=1
    while e:
        if e&1:r=rawmul(r,a)
        a=rawmul(a,a);e>>=1
    return r
GEN=next(g for g in range(2,65536) if all(rawpow(g,65535//p)!=1 for p in (3,5,17,257)))
x=1
for i in range(65535):
    EXP[i]=x;LOG[x]=i;x=rawmul(x,GEN)
for i in range(65535,131072):EXP[i]=EXP[i-65535]
def mul(a,b): return 0 if a==0 or b==0 else EXP[LOG[a]+LOG[b]]
def locator(pts):
    P=[1]
    for v in pts:
        Q=[0]*(len(P)+1)
        for i,c in enumerate(P):
            Q[i+1]^=c;Q[i]^=mul(c,v)
        P=Q
    return P
pc=[bin(i).count('1')&1 for i in range(1<<16)]
rng=random.Random(4)
# 1. exhaustive n=4
n=4
while True:
    ell=rng.sample(range(1,65536),n)
    sp={0}
    for e in ell:sp|={u^e for u in sp}
    if len(sp)==2**n:break
lab=[0]*2**n
for v in range(2**n):
    for i in range(n):
        if v>>i&1:lab[v]^=ell[i]
for size in (9,8):
    for k in (2,3):
        gap=2**(k-1)
        g1=defaultdict(list);g2=defaultdict(list)
        for S in itertools.combinations(range(16),size):
            V=locator([lab[v] for v in S])
            g1[tuple(V[size-gap+1:size])].append(S)
            w=tuple(sum(1-2*pc[v&chi] for v in S)%2**k for chi in range(16))
            g2[w].append(S)
        same=sorted(map(sorted,g1.values()))==sorted(map(sorted,g2.values()))
        print(f"n=4 |S|={size} gap>={gap}: top classes {len(g1)}, Walsh mod {2**k} classes {len(g2)}, identical partitions: {same}")
        assert same
# 2. leading coefficient formula
def laurent_quot_top(num,den,terms):
    # num, den coefficient lists, same degree; series in 1/X of num/den up to given number of terms
    dn,dd=len(num)-1,len(den)-1
    assert dn==dd
    out=[]
    rem=num[:]
    for t in range(terms):
        c=mul(rem[dn-t],EXP[(65535-LOG[den[dd]])%65535]) if rem[dn-t] else 0
        out.append(c)
        if c:
            for i in range(0,dd+1):
                j=dn-t-(dd-i)
                if j>=0: rem[j]^=mul(c,den[i])
    return out
ok=True
for trial in range(30):
    j=rng.randint(2,5)
    while True:
        w=rng.sample(range(1,65536),j)
        sp={0}
        for e in w:sp|={u^e for u in sp}
        if len(sp)==2**j:break
    even=[];odd=[]
    for T in range(2**j):
        s=0
        for i in range(j):
            if T>>i&1:s^=w[i]
        (even if bin(T).count('1')%2==0 else odd).append(s)
    N,D=locator(even),locator(odd)
    ser=laurent_quot_top(N,D,2**(j-1)+1)
    c=1
    for s in odd:c=mul(c,s)
    ok&=ser[0]==1 and all(a==0 for a in ser[1:2**(j-1)]) and ser[2**(j-1)]==c
print("leading coefficient formula on 30 random cubes:",ok); assert ok
# 3. independence by leading monomials over F_2[l_0..l_(n-1)]
def pmulF2(A,B):
    R=set()
    for a in A:
        for b in B:
            R^={tuple(x+y for x,y in zip(a,b))}
    return R
def cpoly(T,t,n):
    P={tuple([0]*n)}
    for r in range(1,len(T)+1,2):
        for U in itertools.combinations(T,r):
            f={tuple(1 if i==u else 0 for i in range(n)) for u in U}
            P=pmulF2(P,f)
    return {tuple(e*2**t for e in m) for m in P}
for n in (4,5,6):
    for j in range(1,5):
        lead={}
        cnt=0
        for m in range(1,j+1):
            t=j-m
            for T in itertools.combinations(range(n),m):
                P=cpoly(T,t,n)
                L=max(P)
                assert sum(1 for q in [L] if q in lead)==0,(n,j,T,t)
                lead[L]=(T,t);cnt+=1
        print(f"n={n} j={j}: basis size {cnt}, all leading monomials distinct")
