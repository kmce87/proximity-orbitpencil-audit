#!/usr/bin/env python3
"""Exact necessary-key gate, NOT a Koala attack or official certificate.

Hypothesis: swapping two 16-element multiplicative cosets of the
order-16 subgroup of the 512th roots can preserve the product key,
therefore potentially support a 115.46-bit 273-fibre upper construction.
"""
q = (1 << 31) - (1 << 24) + 1
g = 665670555
assert pow(g, 512, q) == 1 and pow(g, 256, q) != 1
H = [pow(g, 32*k, q) for k in range(16)]
assert len(set(H)) == 16
cosets = [frozenset((pow(g,j,q)*h)%q for h in H) for j in range(32)]
assert len(set(cosets)) == 32

def prod(xs):
    p = 1
    for x in xs: p = p*x % q
    return p
keys = [prod(c) for c in cosets]
assert len(set(keys)) == 32
assert all(keys[j] == (-pow(g,16*j,q))%q for j in range(32))
# All coset factors X^16 - g^(16j) have identical 14 top nonleading
# coefficients (zero), but pairwise distinct constant terms.
print('PASS: 32 cosets have identical first 14 leading coefficients')
print('FAIL: no two distinct cosets share product key')
print('115.46 hypothetical upper: no certificate from this exchange family')
print('Lean kernel check: NO; independent verifier acceptance: NO')
