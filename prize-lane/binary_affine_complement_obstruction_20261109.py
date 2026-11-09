#!/usr/bin/env python3
"""Exact conditional capacity obstruction for affine Gold zero-set attacks.

Assumption: for each (a,b) in GF(2^64) x GF(2), qualifying challenges
are obtained only when Q_a(x)+b has at least N-i zeros. This is NOT
a statement about arbitrary IRS received words or winning challenges.
"""
N=1<<21
I=917314
K=1<<64
CHALLENGE_SPACE=1<<192
EPS_DENOM=1<<128
required=N-I
assert required==1179838 and 2*required>N
# For fixed a, the zero sets of Q_a and Q_a+1 partition the domain.
# Thus at most one offset b can reach the required zero threshold.
max_eligible=K
assert max_eligible*EPS_DENOM==CHALLENGE_SPACE
assert not (max_eligible*EPS_DENOM>CHALLENGE_SPACE)
print(f"N={N}; unsafe index={I}; zero threshold={required}")
print(f"Max eligible affine pairs={max_eligible} (one per coefficient)")
print("Maximum conditional density = 2^-128, fails strict > 2^-128")
print("No IRS certificate, Lean kernel proof, or verifier acceptance")
