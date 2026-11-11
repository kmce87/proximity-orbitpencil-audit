#!/usr/bin/env python3
"""Exact degree/entropy audit of a 273-fibre OrbitPencil variant; not a general impossibility proof."""
from math import comb
q = 2**31 - 2**24 + 1
N = 511
for fibres in (272, 273):
    for k in (14, 15):
        qdegree_bound = fibres - k - 3
        count = comb(N, fibres)
        keys = q**k * 512
        lower_fibre = count // keys
        print(f"f={fibres}, topkeys={k}, quotient degree <= {qdegree_bound}, guaranteed fibre >= {lower_fibre}, >2^59? {count > keys*2**59}")
assert 272-14-3 == 255
assert 273-14-3 == 256
assert 273-15-3 == 255
assert comb(N,273) > q**14*512*2**59
assert comb(N,273) < q**15*512*2**59
print("PASS: 273 with 14 top keys loses degree guarantee; 15 keys loses 2^59 pigeonhole guarantee.")
