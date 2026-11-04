#!/usr/bin/env python3
"""Independent replay of the second-word test (different field, different algorithm, shares no code with n3_second_word*.py except the member construction).
Field GF(2^20) (x^20+x^3+1).  Instead of dual rows: for each monomial Y^j, D < j < N, reduce modulo the locator V_S and record the coefficients at degrees > D.
A word modulo the polynomials of degree <= D is a combination of these monomials; G(F)/polys is the kernel of the stacked matrix.
Expected kernel dimension: tops + extras + unused labels, with the values found by n3_second_word_generic.py and n3_second_word.py.
Specialising labels can only lower the rank, so extras = 0 here also rules out extras for generic labels at this size."""
import random,sys
import numpy as np
MB=20;POLY=(1<<20)|0b1001;ORD=2**20-1
EXP=np.zeros(2*ORD+2,dtype=np.int64);LOG=np.zeros(2**20,dtype=np.int64)
x=1
for i in range(ORD):
    EXP[i]=x;LOG[x]=i
    x<<=1
    if x>>MB:x^=POLY
assert x==1,"x must be primitive"
EXP[ORD:2*ORD]=EXP[:ORD]
def vs(c,v):
    if c==0:return np.zeros_like(v)
    r=np.zeros_like(v);m=v!=0
    r[m]=EXP[LOG[c]+LOG[v[m]]]
    return r
def inv(a):return int(EXP[(ORD-LOG[a])%ORD])
def locator(pts):
    P=np.array([1],dtype=np.int64)
    for v in pts:
        Q=np.zeros(len(P)+1,dtype=np.int64);Q[1:]^=P;Q[:-1]^=vs(v,P);P=Q
    return P
def rank_incremental(rows_iter,ncols):
    piv=[];pc=[]
    for row in rows_iter:
        row=row.copy()
        for r,p in zip(piv,pc):
            c=int(row[p])
            if c:row^=vs(c,r)
        nz=np.nonzero(row)[0]
        if len(nz):
            p=int(nz[0]);piv.append(vs(inv(int(row[p])),row));pc.append(p)
    return len(piv)
def run(n,family,D,label,expected,seed,cap=120):
    N=2**n
    rng=random.Random(seed)
    while True:
        ell=rng.sample(range(1,2**20),n)
        s={0}
        for e in ell:s|={u^e for u in s}
        if len(s)==N:break
    def lab(v):
        r=0
        for i in range(n):
            if v>>i&1:r^=ell[i]
        return r
    labels=[lab(v) for v in range(N)]
    cols=list(range(D+1,N))
    def rows():
        seen=set();count=0
        for S in family(rng):
            if S in seen:continue
            seen.add(S);count+=1
            used.update(S)
            V=locator([labels[v] for v in sorted(S)])
            m=len(S)
            # Y^j mod V for all needed j by repeated multiplication by Y
            cur=np.zeros(m,dtype=np.int64)
            table=np.zeros((len(cols),m-D-1),dtype=np.int64)
            cur[D]=1  # Y^D, m > D
            for idx,j in enumerate(cols):
                top=int(cur[m-1])
                cur=np.concatenate(([0],cur[:-1]))
                if top:cur^=vs(top,V[:m])
                table[idx]=cur[D+1:]
            for level in range(m-D-1):
                yield table[:,level]
            if count>=cap:return
    used=set()
    r=rank_incremental(rows(),len(cols))
    nullity=len(cols)-r
    unused=N-len(used)
    print(f"{label:44s} n={n} D={D} rank={r} kernel={nullity} (unused labels {unused}) tops+extras={nullity-unused} expected {expected}",flush=True)
    return nullity-unused==expected
par=lambda z:bin(z).count('1')&1
def rand_flat(rng,n,c):
    while True:
        fs=[rng.randrange(1,2**n) for _ in range(c)]
        b=[]
        for f in fs:
            for y in b:f=min(f,f^y)
            if f:b.append(f)
        if len(b)==c:break
    vals=[rng.randrange(2) for _ in range(c)]
    return frozenset(v for v in range(2**n) if all(par(v&f)==b for f,b in zip(fs,vals)))
def one(n,c):
    def it(rng):
        while True:yield rand_flat(rng,n,c)
    return it
def several(n,c,r):
    def it(rng):
        while True:
            Fs=[]
            while len(Fs)<r:
                P=rand_flat(rng,n,c)
                if all(not(P&Q) for Q in Fs):Fs.append(P)
            yield frozenset().union(*Fs)
    return it
def record(ny):
    import n3_second_word as sw
    def it(rng):
        while True:
            yield frozenset(sw.member(sw.rand_param(rng,ny),ny))
    return it
ok=True
ok&=run(7,one(7,2),16,"one flat, codim 2: tops 1 + extras 1",2,11)
ok&=run(8,one(8,3),16,"one flat, codim 3: tops 1 + extras 2",3,12)
ok&=run(7,several(7,3,2),24,"2 disjoint flats, codim 3: no second word",1,13)
ok&=run(8,several(8,3,3),80,"3 disjoint flats, codim 3: no second word",1,14)
ok&=run(8,record(4),128,"record members, ny=4: no second word",1,15)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
