#!/usr/bin/env python3
"""Necessary degree/pigeonhole gates for 273-fibre Koala upper candidate.
Source: zksecurity/proximity-prize-submissions-lean434, OrbitPencil.lean.
Arithmetic only, not a Lean proof or attack.
"""
from math import comb
p=2**31-2**24+1
candidates=comb(511,273)
for d in (14,15,16):
    quotient_bound=273-d-3
    denominator=p**d*512*2**59
    print(f"d={d} quotient_bound={quotient_bound} degree_ok={quotient_bound<=255} pigeonhole_ok={denominator<candidates}")
assert 273-14-3==256
assert 273-15-3==255
assert comb(511,273)>p**14*512*2**59
assert comb(511,273)<p**15*512*2**59
