#!/usr/bin/env python3
"""N3: does the second word survive for more than one varying flat?

Background.  Absorbing the top coefficient kappa_S of C_S by a K-valued slope word g buys up to 2^(16-f) extra labels (19/32 of the domain),
but a line with K-valued f2 has all winners in K, so at most 2^64 winners against the strict threshold 2^64 < winners.  The only way out with a
polynomial g is a second word T' with  T'|_S in K g|_S + Low|_S  for every member (then f1 = T + beta T', f2 = g has winners kappa_S + beta lambda_S).
For one varying flat T' = V_0 X^(2M) exists (Frobenius reduction, n3_single_flat.py, this reproduces the second DKTZ construction).

Test.  G(F) = { words u on V : u|_S agrees with a polynomial of degree <= D on S, for all S in F }.  Any second word lies in G, since K g + Low has degree <= D.
Trivial part of G: polynomials of degree <= D, the top T of the family, and words supported on labels no member uses.  extras = dim G - trivial.
Run on sub-families of the record's parameters with 1, 2, 3 varying flats and on the full parameter set, over GF(2^16), at ny = 3, 4, 5.
Member construction follows LabelFamily.lean (BitWonka) literally.  Credit: the family is BitWonka's; the slope word idea is reconstructed from DKTZ.
"""
import random,sys
from n3_gf import *
def par(x):return bin(x).count('1')&1
def zdot(s,z):return par(s&z)
def lowbit(s):return (s&-s).bit_length()-1
def betaOf(s,j):
    l=lowbit(s)
    return j%2**l+2**(l+1)*(j//2**l)
ROWS=[tuple(map(int,l.split())) for l in open('qrows.txt') if l.strip()]
KAP=(1,0,0)
def insert_zero(m,pos):
    return (m&((1<<pos)-1))|((m>>pos)<<(pos+1))
class Param:
    """row index, jr, aa, ee, r, m (three distinct nonzero reduced), jn, e0, e1"""
    def __init__(s,**k):s.__dict__.update(k)
    def copy(s):return Param(**s.__dict__)
def member(p,ny):
    R=ROWS[p.row];Q=R[:3];S0=R[3:]
    pv=lowbit(p.r)
    mm=[insert_zero(m,pv) for m in p.m]
    beta=betaOf(S0[0],p.jr)
    coefL=[0,p.ee,p.ee^1];rhoC=[p.aa,p.aa^1^p.ee,p.aa^p.ee]
    if p.aa^p.ee==1:bC=[p.e0,1,p.e1]
    else:bC=[p.e0,p.e1,1]
    nuS=[betaOf(S0[t],p.jn[t]) for t in range(3)]
    S=set()
    for z in range(16):
        if z in Q:
            for y in range(2**ny):S.add(y|z<<ny)
        for t in range(3):
            if zdot(S0[t],z)!=KAP[t]:continue
            rho=rhoC[t]^zdot(beta,z)^(coefL[t]&zdot(S0[0],z))
            nu=bC[t]^zdot(nuS[t],z)
            for y in range(2**ny):
                if par(p.r&y)==rho and par(mm[t]&y)==nu:S.add(y|z<<ny)
    assert len(S)==9*2**ny,len(S)
    return sorted(S)
def rand_param(rng,ny):
    while True:
        m=rng.sample(range(1,2**(ny-1)),3)
        return Param(row=rng.randrange(len(ROWS)),jr=rng.randrange(8),aa=rng.randrange(2),ee=rng.randrange(2),r=rng.randrange(1,2**ny),m=m,
                     jn=[rng.randrange(8) for _ in range(3)],e0=rng.randrange(2),e1=rng.randrange(2))
def vary(p,mode,rng,ny):
    """new member with only the named coordinates changed"""
    q=p.copy();q.m=list(p.m);q.jn=list(p.jn)
    if mode=='flat0' or mode=='flat01' or mode=='flat012':
        ts={'flat0':[0],'flat01':[0,1],'flat012':[0,1,2]}[mode]
        for t in ts:q.jn[t]=rng.randrange(8)
        while True:
            for t in ts:q.m[t]=rng.randrange(1,2**(ny-1))
            if len(set(q.m))==3:break
    elif mode=='rflat012':
        q.r=rng.randrange(1,2**ny)
        q.jn=[rng.randrange(8) for _ in range(3)]
        q.m=rng.sample(range(1,2**(ny-1)),3)
    elif mode=='row_fixed':
        q=rand_param(rng,ny);q.row=p.row
    elif mode=='all':
        q=rand_param(rng,ny)
    else:raise ValueError(mode)
    return q
def dual_rows(xs,D):
    """rows y^j / V_S'(y), j=0..|S|-D-2: kernel on S is exactly the polynomials of degree <= D on S"""
    x=np.asarray(xs,dtype=np.int64);m=len(x)
    d=x[:,None]^x[None,:]
    np.fill_diagonal(d,1)
    assert (d!=0).all()
    lg=LOG[d].sum(axis=1)%ORDER
    w=EXP[(ORDER-lg)%ORDER]
    return vvmul(powers(x,m-D-1),np.tile(w,(m-D-1,1)))
def experiment(ny,mode,seed,maxmem=250):
    n=ny+4;N=2**n;D=N//2
    rng=random.Random(seed)
    while True:
        ell=rng.sample(range(1,65536),n)
        if len(set(span(ell)))==N:break
    def lab(v):
        r=0
        for i in range(n):
            if v>>i&1:r^=ell[i]
        return r
    labels=[lab(v) for v in range(N)]
    Wpts=[lab(y) for y in range(2**ny)]
    LW=locator(Wpts)
    T=pmul(pmul(pmul(LW,LW),LW),np.array([0]*(3*2**(n-3))+[1],dtype=np.int64))
    Tvals=np.array([evalp(T,x) for x in labels],dtype=np.int64)
    base=rand_param(rng,ny)
    E=Elim(N);seen=set();used=np.zeros(N,dtype=bool);nmem=0;stall=0;checked=0
    for it in range(maxmem):
        p=vary(base,mode,rng,ny)
        S=member(p,ny);key=tuple(S)
        if key in seen:
            stall+=1
            if stall>200:break
            continue
        seen.add(key);nmem+=1;stall=0
        used[S]=True
        xs=[labels[v] for v in S]
        if checked<3:
            V=locator(xs);C=V.copy();C[:len(T)]^=T
            assert deg(C)<=D,"member lost the common top"
            checked+=1
        R=dual_rows(xs,D)
        for row in R:
            full=np.zeros(N,dtype=np.int64);full[S]=row
            E.add(full)
    null=N-E.rank
    out=int((~used).sum())
    trivial=D+1+1+out
    # T must lie in the kernel
    bad=0
    for row,piv in zip(E.rows[:20],E.piv[:20]):
        if np.bitwise_xor.reduce(vvmul(row,Tvals))!=0:bad+=1
    print(f"ny={ny} n={n} mode={mode:9s} members={nmem:4d} rank={E.rank:4d} dimG={null:4d} = polys {D+1} + top 1 + unused {out} + extras {null-trivial}   (T in kernel: {bad==0})",flush=True)
    return null-trivial,E,labels,D
if __name__=="__main__":
    mns=[int(a) for a in sys.argv[1:]] or [3,4,5]
    for ny in mns:
        for mode in ['flat0','flat01','flat012','rflat012','row_fixed','all']:
            experiment(ny,mode,1000+ny)
