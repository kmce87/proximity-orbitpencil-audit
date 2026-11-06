"""Exact degree gate: fixed-base three-root swaps, Koala 116.12 candidate route.
This is a mathematical counting obstruction, not a Lean certificate.
"""
from math import comb
N=272
k=3
fixed_coeffs=15
# V_i = H * B_i / A_i, H monic degree 272, A_i,B_i monic degree 3,
# A_i and B_i coprime. Equality of top 15 nonleading coefficients
# implies deg(V1-V2) <= 256. Cross multiplication gives
# H*(B1*A2-B2*A1) = (V1-V2)*A1*A2.
# RHS degree <= 262, while nonzero LHS degree >= 272.
# Thus B1*A2=B2*A1; coprimality forces identical swaps.
assert N-(fixed_coeffs+1)+2*k == 262
base_count=comb(31,17)
required=(1<<59)+1
assert base_count == 265182525
assert base_count < required
print('RHS max degree:',262)
print('nonzero LHS min degree:',272)
print('max collision multiplicity across bases:',base_count)
print('required collision multiplicity:',required)
print('PASS: degree/count obstruction')
