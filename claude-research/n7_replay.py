#!/usr/bin/env python3
"""N7 independent replay of the shortened quadric family, GF(2^16), a different method from n7_quadric_check.cpp.
Word T = X^(N/2) V_B, B a random set of N/8 labels.  Member: C = F1 u F2, F1 = {f=0, g1=c1}, F2 = {f=1, g2=c2} (rank 2 quadric).
Check by Newton interpolation of T on S = C u B: interpolant degree <= N/2, agreement on all of V, and the pole pair:
f1 = (T - T(a))/(X-a), f2 = 1/(X-a) has f1 + gamma f2 of degree < N/2 on S with gamma = V_C(a) V_B(a) (a outside V).
Negative control: a random set of the same size has interpolant degree |S|-1.  Slopes are distinct across members."""
import random,sys
from n3_gf import *
def par(x):return bin(x).count('1')&1
def newton(xs,ys):
    """interpolating polynomial, coefficient list lowest first"""
    m=len(xs);d=list(ys)
    for j in range(1,m):
        for i in range(m-1,j-1,-1):
            d[i]=mul(d[i]^d[i-1],inv(xs[i]^xs[i-j]))
    P=np.array([0],dtype=np.int64)
    for i in range(m-1,-1,-1):
        Q=np.zeros(len(P)+1,dtype=np.int64)
        Q[1:]^=P
        Q[:-1]^=vmul(xs[i],P)
        Q[0]^=d[i]
        P=Q
    return P
def run(n,seed,trials):
    rng=random.Random(seed);N=2**n;D=N//2
    while True:
        ell=rng.sample(range(1,65536),n)
        if len(set(span(ell)))==N:break
    def lab(v):
        r=0
        for i in range(n):
            if v>>i&1:r^=ell[i]
        return r
    labels=[lab(v) for v in range(N)]
    B=rng.sample(range(N),N//8)
    VB=locator([labels[v] for v in B])
    XD=np.zeros(D+1,dtype=np.int64);XD[D]=1
    T=pmul(XD,VB)
    Tv=[evalp(T,x) for x in labels]
    while True:
        a=rng.randrange(1,65536)
        if a not in labels:break
    Ta=evalp(T,a)
    f1=[mul(Tv[v]^Ta,inv(labels[v]^a)) for v in range(N)]
    f2=[inv(labels[v]^a) for v in range(N)]
    hist={};slopes=set();above=0;done=0
    while done<trials:
        f=rng.randrange(1,N);g1=rng.randrange(1,N);g2=rng.randrange(1,N)
        if g1 in(f,) or g2 in(f,):continue
        c1=rng.randrange(2);c2=rng.randrange(2)
        C=[v for v in range(N) if (par(v&f)==0 and par(v&g1)==c1) or (par(v&f)==1 and par(v&g2)==c2)]
        if len(C)!=D:continue
        done+=1
        S=sorted(set(C)|set(B))
        xs=[labels[v] for v in S];ys=[Tv[v] for v in S]
        P=newton(xs,ys)
        dg=deg(P)
        assert dg<=D,(dg,D)
        agr=sum(1 for v in range(N) if evalp(P,labels[v])==Tv[v])
        assert agr>=len(S)
        hist[len(S)]=hist.get(len(S),0)+1
        if len(S)>9*N//16:above+=1
        # the line: gamma from the multiset locator
        VC=locator([labels[v] for v in C])
        gamma=mul(evalp(VC,a),evalp(VB,a))
        slopes.add(gamma)
        ys2=[f1[v]^mul(gamma,f2[v]) for v in S]
        Q=newton(xs,ys2)
        assert deg(Q)<D,(deg(Q),D)
    # negative control
    R=rng.sample(range(N),9*N//16+1)
    nc=deg(newton([labels[v] for v in R],[Tv[v] for v in R]))
    assert nc>D
    print(f"n={n} seed={seed} members tested {done}, |S| histogram {sorted(hist.items())}, above 9N/16: {above}, distinct slopes {len(slopes)}, interpolant degree <= {D} always, line degree < {D} always; negative control degree {nc}")
if __name__=="__main__":
    run(6,1,300)
    run(7,2,120)
    run(8,3,25)
