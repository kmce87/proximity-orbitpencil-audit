#!/usr/bin/env python3
"""N3: second-word test on families of generic flats, with a real positive control.

G(F) = { u on V : u|_S has a polynomial of degree <= D on S for all S in F }.  extras = dim G - (D+1) - (#tops) - #unused labels, #tops = 1 here.
Control: one flat of any direction (codim c >= 2): expected extras = c-1, the words Y^(2M), ..., Y^(2^(c-1) M) (Frobenius reduction).
          If the flats are hyperplanes of one fixed subspace the second word degenerates: a^3 + b^2 = d1 a + d2, extras = 0.
Test:   two or three disjoint flats, D = |S| - M/2: is there any second word?"""
import random,sys
from n3_gf import *
from n3_second_word import dual_rows
def par(x):return bin(x).count('1')&1
def rand_flat(rng,n,c,fixed=None):
    """coset of the common kernel of c independent functionals; returns (set of v, functionals, values)"""
    while True:
        fs=[rng.randrange(1,2**n) for _ in range(c)]
        if fixed:fs=list(fixed)+fs[len(fixed):]
        # independence
        b=[]
        ok=True
        for f in fs:
            x=f
            for y in b:x=min(x,x^y)
            if x==0:ok=False;break
            b.append(x)
        if ok:break
    vals=[rng.randrange(2) for _ in range(c)]
    return fs,vals
def flat_points(n,fs,vals):
    return frozenset(v for v in range(2**n) if all(par(v&f)==b for f,b in zip(fs,vals)))
def run(n,members_iter,D,label,maxmem,seed,topcount=1):
    N=2**n
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
    E=Elim(N);seen=set();used=np.zeros(N,dtype=bool);nm=0;stall=0
    for S in members_iter(rng):
        if S in seen:continue
        seen.add(S);nm+=1
        L=sorted(S)
        before=(E.rank,int(used.sum()))
        used[L]=True
        R=dual_rows([labels[v] for v in L],D)
        for row in R:
            full=np.zeros(N,dtype=np.int64);full[L]=row
            E.add(full)
        stall=stall+1 if (E.rank,int(used.sum()))==before else 0
        if nm>=maxmem or stall>=25:break
    null=N-E.rank;out=int((~used).sum())
    extras=null-(D+1)-topcount-out
    print(f"{label:48s} n={n} D={D:4d} members={nm:4d} rank={E.rank:4d} dimG={null:4d} unused={out:4d} extras={extras}",flush=True)
    return extras
def single(n,c):
    def it(rng):
        while True:
            fs,vals=rand_flat(rng,n,c)
            yield flat_points(n,fs,vals)
    return it
def single_in_hyperplane_of_fixed(n,c):
    # all flats are hyperplanes of one fixed coset of a codim (c-1) subspace
    def it(rng):
        fixed=[1<<i for i in range(c-1)]
        while True:
            fs,vals=rand_flat(rng,n,c,fixed=fixed)
            vals[:c-1]=[0]*(c-1)
            yield flat_points(n,fs,vals)
    return it
def disjoint_flats(n,c,r):
    # r disjoint flats of codim c, rejection sampling
    def it(rng):
        while True:
            Fs=[]
            tries=0
            while len(Fs)<r and tries<2000:
                tries+=1
                fs,vals=rand_flat(rng,n,c)
                P=flat_points(n,fs,vals)
                if all(not(P&Q) for Q in Fs):Fs.append(P)
            if len(Fs)==r:
                yield frozenset().union(*Fs)
    return it
ok=True
print("# controls (one flat)")
for n,c,exp in [(7,2,1),(8,2,1),(8,3,2),(9,3,2)]:
    M=2**(n-c)
    e=run(n,single(n,c),M//2,f"one flat, any direction, codim {c} (expect {exp})",400,17+n+c)
    ok&=(e==exp)
for n,c in [(8,3),(9,3)]:
    M=2**(n-c)
    e=run(n,single_in_hyperplane_of_fixed(n,c),M//2,f"one flat, hyperplanes of a fixed subspace, codim {c}",200,5+n)
print("# tests (several disjoint flats, no common structure imposed)")
for n,c,r in [(7,3,2),(8,3,2),(8,3,3),(9,3,2),(9,3,3),(9,4,2),(9,4,3),(9,4,4)]:
    M=2**(n-c)
    D=r*M-M//2
    run(n,disjoint_flats(n,c,r),D,f"{r} disjoint flats of codim {c}, gap M/2",300,29+n+c+r)
print("controls",'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
