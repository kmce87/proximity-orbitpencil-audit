#!/usr/bin/env python3
"""Exact necessary finite counting budget for a Koala 69.00-bit lower proof.

Checks ONLY whether a uniform C*n^3 bound on exceptional challenges
would imply probability <=2^-128 over GF(q^6).
Does not prove any such bound or the IRS extractor bound.
"""
q = 2**31 - 2**24 + 1
n = 2**18
field = q**6
limit = field // 2**128
max_C = limit // n**3
assert max_C == 15
assert (15*n**3)*2**128 <= field
assert (16*n**3)*2**128 > field
assert (4_001_496*n**2)*2**128 <= field
assert (4_001_497*n**2)*2**128 > field
print(f'q={q}; n={n}; |F|={field}')
print(f'allowable bad challenges <= {limit}')
print(f'C*n^3 can pass only if C <= {max_C} (assuming no additive terms)')
print('15*n^3 PASS; 16*n^3 FAIL')
print('No higher-derivative theorem or extractor bound is established.')
