#!/usr/bin/env python3
"""N8: general merge map Phi_j on I^j/I^(j+1) for arbitrary labels (j = n-4 is the class level).
Generators 2^t x_T (|T| = j-t): x_T = 1_H - 1_(H+u), H = even sums of T, u = first element of T.  P = L_H/(L_H + u'), u' = L_H(u),
so Phi_j(2^t x_T) = ((u' a_s(H))^(2^t))_(s = 0..|T|-1), padded with zeros to length j; positions X^-(2^j - 2^(j-1-s)), a_0 = 1, a_s = coefficient of X^(2^(|T|-1-s)) in L_H.
Injective Phi_i for all i <= n-4 means T2 holds exactly for these labels: classes = Walsh classes."""
import sys, random, itertools
POLY=(1<<64)|0x1B
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a>>64:a^=POLY
    return r
def sq(a):return mul(a,a)
def frob(a,t):
    for _ in range(t):a=sq(a)
    return a
def linpoly(basis):
    c=[1]  # c[i]: coefficient of X^(2^i)
    for u in basis:
        v=0;p=u
        for ci in c:
            v^=mul(ci,p);p=sq(p)
        new=[0]*(len(c)+1)
        for i,ci in enumerate(c):
            new[i+1]^=sq(ci);new[i]^=mul(v,ci)
        c=new
    return c
def ev(c,x):
    v=0;p=x
    for ci in c:
        v^=mul(ci,p);p=sq(p)
    return v
def phi(ell,j):
    n=len(ell);vecs=[];names=[]
    for size in range(1,j+1):
        t=j-size
        for T in itertools.combinations(range(n),size):
            u=ell[T[0]];H=[ell[T[0]]^ell[i] for i in T[1:]]
            c=linpoly(H);up=ev(c,u)
            a=c[::-1]  # a[0]=1 leading, a[s] = coefficient of X^(2^(|H|-s))
            coords=[frob(mul(up,a[s]),t) for s in range(len(a))]+[0]*(j-len(a))
            v=0
            for x in coords:v=(v<<64)|x
            vecs.append(v);names.append((t,T))
    return vecs,names
def kernel_dim(vecs,want=False):
    piv={};ker=[]
    for k,v in enumerate(vecs):
        t=1<<k
        while v:
            h=v.bit_length()-1
            if h in piv:
                v^=piv[h][0];t^=piv[h][1]
            else:
                piv[h]=(v,t);break
        if v==0:ker.append(t)
    return (len(ker),ker) if want else len(ker)
if __name__=="__main__":
    rnd=random.Random(7)
    print("n  j  gens  bits  ker(Krylov 1..x^(n-1))  ker(chain random mu)  ker(random labels)")
    for n in range(5,13):
        j=n-4
        kry=[1<<i for i in range(n)]
        mu=rnd.getrandbits(64);lam=rnd.getrandbits(64);ch=[];p=lam
        for i in range(n):
            ch.append(p);p=mul(p,mu)
        ran=[rnd.getrandbits(64) for _ in range(n)]
        v1,names=phi(kry,j);v2,_=phi(ch,j);v3,_=phi(ran,j)
        print(n,j,len(v1),64*j,kernel_dim(v1),kernel_dim(v2),kernel_dim(v3),flush=True)
