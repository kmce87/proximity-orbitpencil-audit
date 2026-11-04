#!/usr/bin/env python3
"""Lane B: exact structural gate for 115.46-bit Koala 273-fibre proposal.

Hypothesis: exchanging 3..14 roots while retaining a common untouched factor
can preserve all 14 leading coefficients and product key yet change derivative.
FALSIFIED algebraically for any field: monic replacement polynomials coincide.

Let V=W*P and V'=W*Q, where W is monic of degree d and P,Q are monic
of degree k<=14. If the first 14 coefficients below the leading term
of V,V' agree, then the first min(k,14) coefficients below the leading
term of P,Q agree (triangular coefficient comparison). For every k<=14, all k nonleading coefficients agree. Hence P=Q.
The product key is redundant for this small-swap obstruction.
This does not rule out replacing >=15 roots, or changes with no common W.
"""
Q = 2130706433

def multiply(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%Q
    return c

def poly_roots(roots):
    p=[1]
    for r in roots:p=multiply(p,[(-r)%Q,1])
    return p

def top(p,n):return tuple(p[-2:-n-2:-1])

# Exercise the coefficient-triangular identity with a nonconstant shared W.
for k in range(3,15):
    w=poly_roots(range(100,120))
    p=poly_roots(range(1,k+1))
    v=multiply(w,p)
    assert len(top(v,14))==14
    # Change one root: a nontrivial change must show up in top coefficients.
    alt=poly_roots([*range(1,k),k+1])
    v2=multiply(w,alt)
    assert top(v,14)!=top(v2,14)

# Formal triangular reconstruction for arbitrary coefficients, not just roots.
# Given monic W and the top k coefficients of W*P, recover P recursively.
def recover(w, top_product, k):
    d=len(w)-1
    p=[0]*(k+1)
    p[k]=1
    for j in range(1,k+1):
        target=top_product[j-1]
        known=sum(w[d-i]*p[k-(j-i)] for i in range(1,min(j,d)+1))
        p[k-j]=(target-known)%Q
    return p
for k in range(3,15):
    w=poly_roots(range(100,120))
    p=poly_roots(range(1,k+1))
    v=multiply(w,p)
    assert recover(w,top(v,k),k)==p
print('PASS: triangular coefficient reconstruction for k=3..14')
print('PROVED algebraically: k<=14 top-14 fixes replacement polynomial')
print('Product key not needed for this obstruction')
print('Hypothesis of a nontrivial <=14-root swap: FALSIFIED')
print('NEXT: >=15-root coordinated replacement; no 115.46 certificate')
