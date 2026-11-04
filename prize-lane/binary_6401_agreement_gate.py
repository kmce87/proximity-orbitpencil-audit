#!/usr/bin/env python3
"""Exact binary 64.01 lower certificate strict-agreement gate."""
from fractions import Fraction
N=2**21
Q=2**28
radii={6400:78622925,6401:78633204}
threshold={}
for score,p in radii.items():
    x=N*(1-Fraction(p,Q))
    threshold[score]=x.numerator//x.denominator+1
    assert Fraction(threshold[score]-1,N)<=1-Fraction(p,Q)
    assert Fraction(threshold[score],N)>1-Fraction(p,Q)
    print(f"{score/100:.2f} bits: radius={p}/{Q}; strict agreement threshold={threshold[score]}; exact real threshold={x}")
assert threshold=={6400:1482911,6401:1482831}
print("New threshold is 80 positions smaller; old P64Final hardcodes 1482911 in interpolation hypotheses.")
