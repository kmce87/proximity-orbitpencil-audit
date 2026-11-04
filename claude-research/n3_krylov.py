#!/usr/bin/env python3
"""N3 side result: the real domain is a Krylov space, so a corrects T2's "no structural K coincidence" remark at f = 0.

D = F_2[x]_{<=20} in BF64 = F_2[x]/(x^64+x^4+x^3+x+1).  x D_{<=19} lies in D, so dim(D cap xD) = 20.
Scaling: L_{lam U}(X) = lam^M L_U(X/lam), hence a(lam U) = lam^(M/2) a(U), b(lam U) = lam^(3M/4) b(U).
Frobenius is additive, so for lam in {1, x, 1+x}:  a(U) + a(xU) + a((1+x)U) = 0 exactly, for every U inside D_{<=19}.
The first-level coefficient kappa of U, xU, (1+x)U vanishes, for this non-generic ell, although the Walsh class (T2) would not predict it.

Checks: (a) identity in exact BF64 arithmetic on random U of dimension 18 and smaller, with a failing control;
(b) disjointness: three flats with directions U, xU, (1+x)U are pairwise disjoint only if codim(U + xU) >= 2 in D, and for dim U = n-3 that leaves exactly the 7 subspaces w F_2[x]_{<=n-4}, deg w <= 2
    (exhaustive at n = 7..11, pure F_2 linear algebra);
(c) direct locator replay in a toy Krylov domain of GF(2^16): V_S = X^(3M) + 0 X^(5M/2) + beta X^(9M/4) + ..., with a failing control."""
import random,sys
from n3_gf import locator,deg,span,mul as gmul16,GEN
MOD=(1<<64)|0x1B
def clmul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
    return r
def red(p):
    while p>>64:
        d=p.bit_length()-65
        p^=MOD<<d
    return p
def mul(a,b):return red(clmul(a,b))
def sq(a):return mul(a,a)
def frob(a,k):
    for _ in range(k):a=sq(a)
    return a
def linpoly(basis):
    """coefficients c[i] of X^(2^i) of the subspace polynomial, P_{k+1} = P_k^2 + P_k(u) P_k"""
    c=[1]
    for u in basis:
        v=0;p=u
        for ci in c:
            v^=mul(ci,p);p=sq(p)
        assert v!=0,"dependent basis"
        new=[0]*(len(c)+1)
        for i,ci in enumerate(c):
            new[i+1]^=sq(ci)
            new[i]^=mul(v,ci)
        c=new
    return c
def check_identity(rng):
    X=2;ok=True;neg=0
    onex=3
    for d,top in [(18,19),(18,19),(12,19),(7,19),(3,19)]:
        # random independent elements of D_{<=top}
        while True:
            B=[rng.randrange(1,2**(top+1)) for _ in range(d)]
            # F_2 rank
            piv=[];
            for v in B:
                for p in piv:v=min(v,v^p)
                if v:piv.append(v)
            if len(piv)==d:break
        c1=linpoly(B);c2=linpoly([mul(X,u) for u in B]);c3=linpoly([mul(onex,u) for u in B])
        a=[c[d-1] for c in (c1,c2,c3)]
        ok&=(a[0]^a[1]^a[2])==0
        M=2**d
        # scaling law
        ok&=a[1]==mul(frob(X,d-1),a[0])
        if d>=2:
            b=[c[d-2] for c in (c1,c2,c3)]
            xx=X^mul(X,X)  # x^2+x
            ok&=(b[0]^b[1]^b[2])==mul(b[0],frob(xx,d-2))
        # control: a random third subspace does not cancel
        while True:
            B3=[rng.randrange(1,2**(top+1)) for _ in range(d)]
            piv=[]
            for v in B3:
                for p in piv:v=min(v,v^p)
                if v:piv.append(v)
            if len(piv)==d:break
        c4=linpoly(B3)
        if (a[0]^a[1]^c4[d-1])!=0:neg+=1
    print(f"(a) BF64 identity a(U)+a(xU)+a((1+x)U)=0, scaling law and b-level formula: {'ok' if ok else 'FAIL'}; control cancels in {5-neg}/5 cases")
    return ok and neg==5
def rank(vs):
    piv=[];
    for v in vs:
        for p in piv:v=min(v,v^p)
        if v:piv.append(v)
    return len(piv)
def codim2_subspaces(m):
    """all codim-2 subspaces of F_2^m as bases, from 2-dim subspaces of the dual"""
    seen=set()
    par=lambda x:bin(x).count('1')&1
    for f in range(1,2**m):
        for g in range(f+1,2**m):
            k=frozenset((f,g,f^g))
            if k in seen:continue
            seen.add(k)
            # kernel basis by elimination
            pts=[v for v in range(1,2**m) if par(v&f)==0 and par(v&g)==0] if m<=8 else None
            yield f,g
def kernel_basis(m,fs):
    """basis of common kernel of functionals fs on F_2^m"""
    rows=[];pivs=[]
    for f in fs:
        for r,p in zip(rows,pivs):
            if f>>p&1:f^=r
        if f:
            p=f.bit_length()-1
            for i in range(len(rows)):
                if rows[i]>>p&1:rows[i]^=f
            rows.append(f);pivs.append(p)
    free=[i for i in range(m) if i not in pivs]
    B=[]
    for i in free:
        v=1<<i
        for r,p in zip(rows,pivs):
            if r>>i&1:v|=1<<p
        B.append(v)
    return B
def check_disjoint():
    ok=True
    for n in range(7,12):
        m=n-1
        hits=[];tot=0
        seen=set()
        for f in range(1,2**m):
            for g in range(f+1,2**m):
                if g==f^g or (f^g)<g:continue   # canonical: smallest two of the triple
                tot+=1
                B=kernel_basis(m,[f,g])
                r=rank(B+[u<<1 for u in B])
                if r<=n-2:hits.append(B)
        # expected: the 7 subspaces w F_2[x]_{<=n-4}
        def clm(w,b):
            r=0
            while b:
                if b&1:r^=w
                w<<=1;b>>=1
            return r
        exp=set()
        for w in range(1,8):
            bas=[clm(w,1<<i) for i in range(n-3)]
            # canonical form: sorted reduced basis
            exp.add(tuple(canon(bas)))
        got={tuple(canon(B)) for B in hits}
        print(f"(b) n={n}: {tot} subspaces U of dim n-3 in D_<=n-2; codim(U+xU)>=2 for {len(hits)}; equal to w F_2[x]_<=n-4: {got==exp}")
        ok&=(got==exp) and tot==((2**m-1)*(2**(m-1)-1)//3)
    return ok
def canon(B):
    piv=[]
    for v in B:
        for p in piv:
            if v^p<v:v^=p
        if v:piv.append(v)
    piv.sort(reverse=True)
    for i in range(len(piv)):
        for j in range(len(piv)):
            if i!=j and (piv[j]>>(piv[i].bit_length()-1))&1:piv[j]^=piv[i]
    return sorted(piv)
def check_locator(rng):
    n=9;N=2**n;M=2**(n-3)
    # Krylov domain in GF(2^16): powers of the generator g
    g=GEN
    pw=[1]
    for i in range(1,n):pw.append(gmul16(pw[-1],g))
    def lab(v):
        r=0
        for i in range(n):
            if v>>i&1:r^=pw[i]
        return r
    assert len({lab(v) for v in range(N)})==N
    def clm(w,b):
        r=0
        while b:
            if b&1:r^=w
            w<<=1;b>>=1
        return r
    ok=True;done=0
    for w in range(1,8):
        Ubasis=[clm(w,1<<i) for i in range(n-3)]
        U=span(Ubasis)
        xU=[u<<1 for u in U];oU=[u^(u<<1) for u in U]
        assert max(xU)<N and max(oU)<N
        E=span(Ubasis+[u<<1 for u in Ubasis])
        # offsets in three different cosets of E
        cos=[];seen=set()
        for v in range(N):
            if v in seen:continue
            cs={v^e for e in E};seen|=cs;cos.append(v)
        assert len(cos)>=3
        F1={u^cos[0] for u in U};F2={u^cos[1] for u in xU};F3={u^cos[2] for u in oU}
        assert not(F1&F2 or F1&F3 or F2&F3) and len(F1|F2|F3)==3*M
        V=locator([lab(v) for v in F1|F2|F3])
        # coefficients of X^(3M-M/2)=X^(5M/2) must vanish, and everything between 9M/4 and 3M
        high=[i for i in range(9*M//4+1,3*M) if int(V[i])!=0]
        beta=int(V[9*M//4])
        ok&=(high==[]) ; done+=1
        print(f"(c) w={w}: |S|={3*M}, nonzero coefficients above X^(9M/4) below the top: {high}, beta={beta}")
    # control: same sizes, random flats: X^(5M/2) nonzero
    fails=0
    for _ in range(5):
        while True:
            def rf():
                fs=[rng.randrange(1,N) for _ in range(3)]
                vals=[rng.randrange(2) for _ in range(3)]
                par=lambda x:bin(x).count('1')&1
                return {v for v in range(N) if all(par(v&f)==b for f,b in zip(fs,vals))}
            A,B,C=rf(),rf(),rf()
            if len(A)==M and len(B)==M and len(C)==M and not(A&B or A&C or B&C):break
        V=locator([lab(v) for v in A|B|C])
        if int(V[5*M//2])!=0:fails+=1
    print(f"(c) control: random disjoint flats have nonzero X^(5M/2) coefficient in {fails}/5 cases")
    return ok and fails>=4
rng=random.Random(20261104)
res=[check_identity(rng),check_disjoint(),check_locator(rng)]
print("PASS" if all(res) else "FAIL",res)
sys.exit(0 if all(res) else 1)
