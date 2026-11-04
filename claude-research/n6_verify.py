#!/usr/bin/env python3
"""N6 verification by direct locators (no shared code with the DFS).
Toy: K = GF(2^16) (x^16+x^5+x^3+x+1), random injective F_2-linear labels of F_2^(ny+4).  Each dumped member S must satisfy
 (a) |S| = 9*2^ny; (b) deg(V_S - L_W^3 X^(3*2^(n-3))) <= 2^(n-1), where W = {z = 0};
 (c) Walsh coefficients of 1_S - 1_S' divisible by 2^(n-3) for pairs.
Also a negative control: flipping a swap of two labels breaks (b)."""
import random,sys
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
def locator(pts):
    P=[1]
    for v in pts:
        Q=[0]*(len(P)+1)
        lv=LOG[v] if v else None
        for i,c in enumerate(P):
            Q[i+1]^=c
            if c and v:Q[i]^=EXP[LOG[c]+lv]
        P=Q
    return P
def pmul(A,B):
    R=[0]*(len(A)+len(B)-1)
    for i,a in enumerate(A):
        if a:
            la=LOG[a]
            for j,b in enumerate(B):
                if b:R[i+j]^=EXP[la+LOG[b]]
    return R
def deg(P):
    d=len(P)-1
    while d>=0 and P[d]==0:d-=1
    return d
def run(path,ny,trials=2):
    n=ny+4;rng=random.Random(20261104)
    members=[]
    for line in open(path):
        t=list(map(int,line.split()));prof,rk,masks=t[0],t[1],t[2:]
        S=[]
        for z,m in enumerate(masks):
            for y in range(2**ny):
                if m>>y&1:S.append(y|z<<ny)
        members.append((prof,rk,S))
    D=2**(n-1);tally={}
    for tr in range(trials):
        while True:
            ell=rng.sample(range(1,65536),n)
            sp={0}
            for e in ell:sp|={u^e for u in sp}
            if len(sp)==2**n:break
        def lab(v):
            r=0
            for i in range(n):
                if v>>i&1:r^=ell[i]
            return r
        Wpts=[lab(y) for y in range(2**ny)]
        LW=locator(Wpts)
        T=[0]*(3*2**(n-3))+pmul(pmul(LW,LW),LW)
        for prof,rk,S in members:
            assert len(S)==9*2**ny
            V=locator([lab(v) for v in S])
            C=[(V[i] if i<len(V) else 0)^(T[i] if i<len(T) else 0) for i in range(max(len(V),len(T)))]
            d=deg(C)
            ok=d<=D
            tally[(prof,rk)]=tally.get((prof,rk),[0,0]);tally[(prof,rk)][0 if ok else 1]+=1
        # negative control: swap one element of one member with an outside element
        prof,rk,S=rng.choice(members)
        out=next(v for v in range(2**n) if v not in set(S))
        S2=S[1:]+[out]
        V=locator([lab(v) for v in S2])
        C=[(V[i] if i<len(V) else 0)^(T[i] if i<len(T) else 0) for i in range(max(len(V),len(T)))]
        assert deg(C)>D, "negative control failed"
    bad=sum(v[1] for v in tally.values());good=sum(v[0] for v in tally.values())
    print(f"ny={ny}: members checked {len(members)}, direct locator checks ok={good} failed={bad}; profiles/ranks seen: {sorted(tally)[:60]}")
    # Walsh check among pairs
    def walsh(S,chi):
        return sum(1-2*(bin(v&chi).count('1')&1) for v in S)
    bad2=0
    for _ in range(40):
        a=rng.choice(members)[2];b=rng.choice(members)[2]
        for chi in rng.sample(range(2**n),32):
            if (walsh(a,chi)-walsh(b,chi))%2**(n-3):bad2+=1
    print("Walsh divisibility violations on sampled pairs:",bad2)
    return bad+bad2
sys.exit(1 if run(sys.argv[1],int(sys.argv[2])) else 0)
