#!/usr/bin/env python3
"""Exact-integer feasibility gate for a 116.12-bit Koala 273-fibre extension.

Official source: ProximityPrize/SubmissionUpper/OrbitPencil.lean, especially
NN, alpha_count, bad_card_le, gamma_injective and pencil_eval_alpha.
This checks whether the EXISTING collision-root union bound suffices to
choose an alpha from GF(q^2), which could support a q^2-Frobenius third root.
It does NOT rule out the existence of such an alpha or a new 116.12 proof.
"""
from math import gcd
q = 2**31 - 2**24 + 1
N = 2**59 + 1
bad_bound = N*N*272 + 513
field = q**6
subfield = q**2
assert bad_bound < field  # official alpha_count proof's numerical statement
assert not bad_bound < subfield
assert N < subfield
assert q < N
assert gcd(6, 2) == 2
# q^2 fixed points exist in GF(q^6), but cardinality alone does not force
# the published injective gamma family to meet that subfield.
# A guarantee using the existing bad-set upper bound would require
# bad_bound < q^2; that condition is false by a huge margin.
for name,value in [('q',q),('N',N),('q^2',subfield),('q^6',field),('collision_union_upper_bound',bad_bound)]:
    print(f'{name}={value}')
print('N < q^2:',N < subfield)
print('collision_union_upper_bound < q^2:',bad_bound < subfield)
print('collision_union_upper_bound < q^6:',bad_bound < field)
print('RESULT: published union bound cannot guarantee alpha in GF(q^2).')
print('NOT RESULT: no such alpha exists; no third root exists; 116.12 is impossible.')
