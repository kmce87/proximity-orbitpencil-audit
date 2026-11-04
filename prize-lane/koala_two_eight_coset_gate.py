#!/usr/bin/env python3
"""16-root exchange: two order-8 cosets of the Koala 512-root subgroup.

Hypothesis: two distinct unordered pairs of 8-cosets share the first 14
nonleading coefficients and the product key, potentially permitting a
115.46-bit Koala upper construction. This is a restricted-family test only.
"""
from itertools import combinations

q = (1 << 31) - (1 << 24) + 1
assert (q - 1) % 512 == 0
g = next(pow(t, (q - 1) // 512, q) for t in range(2, 1000)
         if pow(t, ((q - 1) // 512) * 256, q) != 1)
assert pow(g, 512, q) == 1 and pow(g, 256, q) != 1
a = [pow(g, 8*j, q) for j in range(64)]
assert len(set(a)) == 64

# Two cosets give (X^8-a)(X^8-b)=X^16-(a+b)X^8+ab.
# X^8 is among the 14 nonleading coefficient constraints.
keys = {}
for i, j in combinations(range(64), 2):
    key = ((a[i] + a[j]) % q, (a[i] * a[j]) % q)
    assert key not in keys, (i, j, keys.get(key))
    keys[key] = (i, j)
assert len(keys) == 2016
print("PASS: 2016 distinct two-8-coset pairs have distinct (sum,product) keys")
print("Hypothesis of a key collision within this family: FALSIFIED")
print("Not a Koala upper construction, Lean proof, or accepted submission")
