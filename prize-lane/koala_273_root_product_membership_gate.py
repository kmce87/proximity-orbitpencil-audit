#!/usr/bin/env python3
"""Lane B: necessary root-product membership test for previous witness.

Hypothesis: V_0(X)=X^273+1 from the 13-class derivative witness is a
product of 273 distinct linear factors over the Koala base field.
"""
from math import gcd
q=(1<<31)-(1<<24)+1
d=273
assert q==2130706433
assert gcd(d,q-1)==1
# The multiplicative group F_q^* has order q-1.
# Consequently x |-> x^273 is a bijection of F_q^*.
# x^273=-1 has exactly one solution, x=-1 (d is odd).
assert pow(q-1,d,q)==q-1
assert d>1
print('q:',q,'gcd(273,q-1):',gcd(d,q-1))
print('V_0=X^273+1 has exactly ONE distinct F_q root, not 273.')
print('FALSIFIED: V_0 is a 273-distinct-root product.')
print('Not a classification of V_t for t=1..12.')
print('No improved official claim, Lean proof or verifier acceptance.')
