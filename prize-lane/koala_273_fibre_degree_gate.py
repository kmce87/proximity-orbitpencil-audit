#!/usr/bin/env python3
"""Exact necessary gates for 273-fibre OrbitPencil; not a Lean certificate."""
from math import comb
q = 2**31 - 2**24 + 1
N = 2**59 + 1
for k in (272, 273):
    family = comb(511, k)
    key_budget = q**14 * 512 * 2**59
    bad_budget = N*N*k + 513
    print(f"k={k} orbit_count={family > key_budget} alpha_count={bad_budget < q**6}")
    assert family > key_budget
    assert bad_budget < q**6
    # Equal 14 top coefficients: difference degree <= k-15.
    # Two roots 0 and alpha: quotient Q degree <= k-17.
    print(f"  difference_degree_upper={k-15}, Q_degree_upper={k-17}")
assert 273 - 17 == 256
print("PASS numerical gates; Q<=255 does not follow for k=273")
