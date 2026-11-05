#!/usr/bin/env python3
"""Koala 116.12: falsify automatic constancy of the 15th power sum.
Not a collision of the historical 14-coefficient key; not a Lean proof.
"""
Q = 2**31 - 2**24 + 1
N = 512
assert (Q-1) % N == 0
# Find an element of exact order 512 in the prime field.
omega = next(pow(a, (Q-1)//N, Q) for a in range(2,1000)
             if pow(pow(a,(Q-1)//N,Q),N//2,Q) != 1)
assert pow(omega,N,Q)==1 and pow(omega,N//2,Q)!=1
y = [pow(omega,b,Q) for b in range(N)]
U = set(range(1,273))
W = (U-{272})|{273}
assert len(U)==len(W)==272 and 0 not in U and 0 not in W
def p15(s): return sum(pow(y[b],15,Q) for b in s)%Q
assert p15(U)!=p15(W)
# Newton identity for monic V: 15*e15 = sum_{j=1}^{15} (-1)^(j-1)*e_(15-j)*p_j.
# Thus fixing e1..e14 fixes e15 iff p15 is fixed (15 invertible mod Q).
assert 15%Q!=0
print("q",Q,"omega",omega,"p15(U)",p15(U),"p15(W)",p15(W))
print("PASS: 15th power sum not constant across allowed 272-root subsets.")
print("LIMIT: U and W are NOT asserted to share the existing 14-key/product key.")
