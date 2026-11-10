#!/usr/bin/env python3
"""Exhaustive 420-configuration F2^4 reserved-coset XOR check.
No Lean or official verifier claim."""
from collections import Counter
from itertools import combinations
V=range(16)
planes={frozenset((0,a,b,a^b)) for a,b in combinations(range(1,16),2)}
assert len(planes)==35
configs=[]
for H in planes:
    cosets={frozenset(x^h for h in H) for x in V}
    assert len(cosets)==4
    for A in cosets:
        if 0 in A: continue
        for missing in A:
            Q=A-{missing}
            xor_q=0
            for q in Q: xor_q^=q
            assert xor_q==missing!=0
            configs.append((H,A,missing,xor_q))
assert len(configs)==420
counts=Counter(t[3] for t in configs)
assert set(counts)==set(range(1,16))
assert set(counts.values())=={28}
print("PASS: 35 linear planes, 420 configurations")
print("PASS: XOR of three reserved labels = omitted nonzero label")
print("PASS: 15 omitted labels each occur 28 times")
print("NOT PROVED: field injectivity, zero coefficient family, 106.23 attack")
