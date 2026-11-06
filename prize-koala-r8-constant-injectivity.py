#!/usr/bin/env python3
"""Exact arithmetic gate for eight-swap fixed-base injectivity.

Proof sketch (not Lean checked):
H is monic squarefree degree 272 with nonzero roots. Each candidate Vi is
H*Bi/Ai where Ai divides H, deg Ai=deg Bi=r and Ai,Bi are monic.
Let L=lcm(A1,A2). Then H/L divides both V1,V2 and hence D=V1-V2.
Equal top 15 nonleading coefficients imply deg D <=256.
deg(H/L)>=272-2*r. For r<=7 this forces D=0.
For r=8, D can only be zero or a scalar multiple of H/L.
Equal constant coefficients give D(0)=0, but (H/L)(0)!=0,
so D=0. Thus at most one resulting polynomial per base H per
(top-15-coefficient, constant) key for r<=8.
This does not prove any improved benchmark claim.
"""
from math import comb
N=272
D=256
BASES=comb(31,17)
REQUIRED=2**59+1
assert BASES==265182525
assert N-2*7>D
assert N-2*8==D
assert N-2*9<D
assert BASES<REQUIRED
for r in (7,8,9):
    print(r,N-2*r,"injectivity by this argument:",r<=8)
print("bases",BASES,"required",REQUIRED)
print("PASS exact arithmetic; no Lean verification")
