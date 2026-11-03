#!/usr/bin/env python3
"""Lane B: no nontrivial two-root swap preserving top coefficient and product.

A monic root product V(X)=W(X)(X-a)(X-b) has next-to-leading
coefficient -sum(roots(W))-a-b and constant W(0)*a*b.
For nonzero roots and W(0)!=0, preserving these keys forces
sum a+b and product ab, hence the unordered root pair.
This is an algebraic obstruction, not a new Koala upper certificate.
"""
from itertools import combinations
q = (1 << 31) - (1 << 24) + 1
assert q == 2130706433
# Test 512th roots of unity (actual field subgroup, not proof of Koala fibre layout).
assert (q-1) % 512 == 0
primitive = next(g for g in range(2,1000) if pow(g,(q-1)//2,q)!=1)
g = pow(primitive,(q-1)//512,q)
assert pow(g,512,q)==1 and pow(g,256,q)!=1
roots=[pow(g,j,q) for j in range(512)]
assert len(set(roots))==512
seen={}
for i,j in combinations(range(512),2):
    a,b=roots[i],roots[j]
    key=((a+b)%q,(a*b)%q)
    if key in seen:
        assert seen[key]==(i,j), ('nontrivial collision',seen[key],(i,j))
    else: seen[key]=(i,j)
assert len(seen)==512*511//2
print('PASS: all 130816 unordered pairs have unique (sum,product) keys')
print('PROVED ALGEBRAICALLY: equal sum/product => equal monic quadratic => same unordered pair')
print('BLOCKER: changing only two roots cannot vary derivative while preserving even first leading and product keys')
print('NO actual 273-fibre construction; NO Lean proof; NO independent acceptance')
