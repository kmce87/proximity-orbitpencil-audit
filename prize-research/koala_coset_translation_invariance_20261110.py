"""Lane B: finite-field exhaustive sanity check for RS coset translation invariance.
Mathematical fact: for linear RS code C and h in C, mapping c -> c+h
bijects C and preserves agreement sets against r -> r+h, at every radius.
This cannot strengthen a Koala upper score for any fixed winning-density criterion.
"""
from itertools import product
P=7
X=tuple(range(P))
K=3

def evaluate(coeff):
    return tuple(sum(a*pow(x,j,P) for j,a in enumerate(coeff))%P for x in X)

C={evaluate(c) for c in product(range(P),repeat=K)}
assert len(C)==P**K
r=tuple((x*x*x+2*x+1)%P for x in X)
h=evaluate((3,4,2))
r2=tuple((a+b)%P for a,b in zip(r,h))

def histogram(received):
    return tuple(sum(sum(a==b for a,b in zip(received,c))>=t for c in C) for t in range(P+1))

assert histogram(r)==histogram(r2)
for c in C:
    cp=tuple((a+b)%P for a,b in zip(c,h))
    assert cp in C
    assert tuple(a==b for a,b in zip(r,c))==tuple(a==b for a,b in zip(r2,cp))
print('PASS: all 343 codewords and all 8 agreement thresholds invariant under RS translation')
print('Conclusion: affine/coset shift alone cannot improve 116.13 -> 116.12.')
