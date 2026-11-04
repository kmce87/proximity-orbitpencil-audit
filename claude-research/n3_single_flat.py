#!/usr/bin/env python3
"""N3, reconstruction of the second DKTZ construction from its abstract (rate 1/16, (N-1)(N-2)/6 exceptional challenges).
The PDF body was not readable (robots), so this is a reconstruction, tested here, not a quotation.
Claim tested for every codim-2 subspace U of a random additive domain D of size N (M = |U| = N/4, k = N/16):
 (1) on U\\{0}: X^(M-1) + a X^(M/2-1) agrees with a polynomial of degree < k, where L_U = X^M + a X^(M/2) + b X^(M/4) + ...
 (2) second word: X^(2M-1) + (a^3+b^2) X^(M/2-1) also agrees with a polynomial of degree < k on U\\{0}
 (3) (a,b) is injective on the (N-1)(N-2)/6 subspaces, a alone need not be.  So f1 = X^(M-1) + beta X^(2M-1), f2 = X^(M/2-1)
     has an F-valued winner a + beta (a^3+b^2) for each U, with one slope per subspace.
"""
import random,sys,itertools
from n3_gf import *
def subspaces_codim2(n):
    """all pairs of functionals up to GL2: enumerate 2-dim subspaces of dual F_2^n by reduced echelon pairs"""
    seen=set()
    for a in range(1,2**n):
        for b in range(a+1,2**n):
            key=frozenset((a,b,a^b))
            if key in seen:continue
            seen.add(key)
            yield a,b
def par(x):return bin(x).count('1')&1
def run(n,seed):
    N=2**n;M=N//4;k=N//16
    rng=random.Random(seed)
    while True:
        ell=rng.sample(range(1,65536),n)
        if len(set(span(ell)))==N:break
    def lab(v):
        r=0
        for i in range(n):
            if v>>i&1:r^=ell[i]
        return r
    D=[lab(v) for v in range(N)]
    seen_a={};seen_ab={};cnt=0;fail=0
    for f,g in subspaces_codim2(n):
        U=[v for v in range(N) if par(v&f)==0 and par(v&g)==0]
        pts=[lab(v) for v in U]
        L=locator(pts)
        assert deg(L)==M
        a=int(L[M//2]);b=int(L[M//4])
        assert all(int(L[i])==0 for i in range(M//2+1,M)),"not linearized?"
        cnt+=1
        seen_a.setdefault(a,0);seen_a[a]+=1
        seen_ab.setdefault((a,b),0);seen_ab[(a,b)]+=1
        # R = L/X has only the monomials X^(2^i-1)
        R=L[1:]
        # (1) f1 + a f2 agrees with -(lower part), lower part has degree < k: lower = R minus top two terms
        low=R.copy();low[M-1]^=1;low[M//2-1]^=a
        ok1=deg(low)<k
        # (2) X^(2M-1)+c X^(M/2-1) low on U\0: reduce X^(2M-1) mod R
        c=mul(a,mul(a,a))^mul(b,b)
        rem=np.zeros(2*M,dtype=np.int64);rem[2*M-1]=1;rem[M//2-1]^=c
        # polynomial division by monic R (degree M-1)
        for d in range(2*M-1,M-2,-1):
            q=int(rem[d])
            if q:rem[d-(M-1):d+1]^=vmul(q,R)
        ok2=deg(rem)<k
        # direct evaluation check on the points
        nz=[p for p in pts if p]
        if cnt%500==1:
            for p in nz[:8]:
                v1=fpow(p,M-1)^mul(a,fpow(p,M//2-1))^evalp(low,p)
                assert v1==0
                v2=fpow(p,2*M-1)^mul(c,fpow(p,M//2-1))^evalp(rem,p)
                assert v2==0
        if not(ok1 and ok2):fail+=1
    exp=(N-1)*(N-2)//6
    print(f"n={n} N={N} agreement={M-1} k={k} subspaces={cnt} expected (N-1)(N-2)/6={exp} failures={fail} distinct a={len(seen_a)} distinct (a,b)={len(seen_ab)}")
    return fail==0 and cnt==exp and len(seen_ab)==exp
ok=True
for n,seed in [(6,1),(7,2),(8,3)]:
    ok&=run(n,seed)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
