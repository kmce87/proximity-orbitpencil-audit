#!/usr/bin/env python3
"""N8: exact checks of two identities in F_2[x] (no reduction, via BF64 with small degrees and via a large-degree random test in BF64):
(1) Carlitz: e_f(xu) = x^(2^f) e_f(u) + (x^(2^f) + x) D_(f-1) e_(f-1)(u), e_f = L_(P_f), D_f = e_f(x^f).
(2) f = 1 half-dimension relation: for z = 1, u_w = (w^2+w)/(x^2+x), x^2 L(u_w) = L(x u_w + w), L(X) = X^2 + X."""
import random
from n8_phi import mul, sq, frob, linpoly, ev
rng=random.Random(3)
X=2
def e(f): return linpoly([1<<i for i in range(f)])
ok=True
for f in range(1,9):
    ef=e(f);ef1=e(f-1);Df1=ev(ef1,1<<(f-1)) if f>=1 else 1
    xq=frob(X,f)
    for _ in range(50):
        u=rng.getrandbits(64)
        lhs=ev(ef,mul(X,u))
        rhs=mul(xq,ev(ef,u))^mul(mul(xq^X,Df1),ev(ef1,u))
        ok&=lhs==rhs
print("Carlitz identity holds for f=1..8 on random u in BF64:",ok)
def pdiv(a,b):
    q=0
    while a and a.bit_length()>=b.bit_length():
        s=a.bit_length()-b.bit_length();q^=1<<s;a^=b<<s
    return q,a
def clsq(a):
    r=0;i=0
    while a>>i:
        if a>>i&1:r^=1<<(2*i)
        i+=1
    return r
ok2=True;count=0
for w in range(2,1<<11):
    q,rem=pdiv(clsq(w)^w,0b110)
    ok2&=rem==0
    u=q
    L=lambda t:sq(t)^t
    u2=(mul(X,u))^w
    ok2&=mul(4,L(u))==L(u2);count+=1
print("x^2 L(u_w) = L(x u_w + w) for all w of degree <= 10:",ok2,"count",count)
