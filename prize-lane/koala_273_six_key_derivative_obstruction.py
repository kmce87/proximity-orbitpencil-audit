#!/usr/bin/env python3
"""Lane B negative test: a 6-valued auxiliary key is not forced by the
leading-coefficient and constant/product constraints alone.

A *toy* finite-field obstruction over F_97, not an impossibility theorem
for the published KoalaBear fibre family, and not a prize submission.
The official 116.13-bit upper attack belongs to its original authors.
"""
from itertools import combinations
from collections import defaultdict

P = 97
ALPHA = 1
def poly(roots):
    c = [1]
    for r in roots:
        nxt = [0] * (len(c) + 1)
        for i, a in enumerate(c):
            nxt[i] = (nxt[i] - r * a) % P
            nxt[i + 1] = (nxt[i + 1] + a) % P
        c = nxt
    return c

def eval_poly(c, x):
    return sum(a * pow(x, i, P) for i, a in enumerate(c)) % P

def corrected_derivative(c):
    # For P_c(X)=c(X)-c0(X)-gamma X, with
    # gamma=(c(alpha)-c0(alpha))/alpha, the derivative at 0 is
    # (c[1]-c0[1])-(c(alpha)-c0(alpha))/alpha.
    # The reference c0 cancels when comparing values across c.
    return (c[1] - eval_poly(c, ALPHA) * pow(ALPHA, -1, P)) % P

def main():
    buckets = defaultdict(dict)
    witness = None
    for roots in combinations(range(1, 24), 5):
        c = poly(roots)
        # monic degree 5: c[-2] is the fixed leading subcoefficient,
        # c[0] is the fixed constant / root-product key.
        key = (c[-2], c[0])
        k = corrected_derivative(c)
        buckets[key].setdefault(k, roots)
        if len(buckets[key]) >= 8:
            witness = (key, list(buckets[key].items())[:8])
            break
    assert witness is not None
    key, items = witness
    assert len({k for k, _ in items}) == 8
    base = poly(items[0][1])
    for k, roots in items:
        c = poly(roots)
        assert (c[-2], c[0]) == key
        diff = [(x-y)%P for x,y in zip(c,base)]
        gamma = eval_poly(diff, ALPHA) * pow(ALPHA,-1,P) % P
        assert (diff[1]-gamma)%P == (k-items[0][0])%P
        assert (eval_poly(diff,ALPHA)-gamma*ALPHA)%P == 0
        assert diff[0] == 0
    print('PASS: 8 distinct corrected derivatives for identical top/constant keys')
    print('field=F_97; polynomial degree=5; alpha=1; key=',key)
    for k, roots in items:
        print('  corrected derivative representative=',k,'roots=',roots)
    print('Conclusion: the existing keys alone do NOT imply <=6 derivative classes.')
    print('LIMIT: toy finite-field family, not KoalaBear, no Lean certificate.')

if __name__ == '__main__':
    main()
