#!/usr/bin/env python3
"""Lane B: test affine-offset invariance of the next-to-leading flat coefficient.
Official LabelFamily.lean: phi uses sig/rr/rhoLin/mm/nuS, while tgt uses
kap/rhoC/bC. Varying aa/e0/e1 in tgt (with phi fixed) translates the
flat, without changing its kernel. This is a finite-field toy test,
not a Lean proof of the official construction or verifier acceptance.
"""
from itertools import combinations
def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1
        a<<=1
        if a&16:a^=0b10011
    return z
def polynomial_roots(roots):
    c=[1]
    for r in roots:
        out=[0]*(len(c)+1)
        for j,v in enumerate(c):
            out[j]^=mul(v,r)
            out[j+1]^=v
        c=out
    return c
spaces={tuple(sorted((0,a,b,a^b))) for a,b in combinations(range(1,16),2)}
assert len(spaces)==35
for space in spaces:
    baseline=polynomial_roots(space)[2]
    for offset in range(16):
        assert polynomial_roots([x^offset for x in space])[2]==baseline
print("PASS: 35 two-dimensional GF(16) subspaces x 16 translations = 560")
print("Affine translations do not tune the degree-2 coefficient.")
print("No official 106.23 proof, kernel check, or independent acceptance.")
