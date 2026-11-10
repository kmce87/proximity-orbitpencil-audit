#!/usr/bin/env python3
"""GF(2) toy audit: three affine constant choices preserve degree-16 coefficient.
The production-source implication requires fixed row,jr,rr,mr,jn,ee.
Not a Lean proof or a binary upper improvement.
"""
from itertools import product
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i+j]^=x&y
 return c
LW=[1,1,1]
G=mul(mul(LW,LW),LW)
vals=[]
for aa,e0,e1 in product(range(2),repeat=3):
 f=[[aa,1,0,0,1],[e0,0,1,0,1],[e1,1,1,0,1]]
 F=[1]
 for p in f:F=mul(F,p)
 vals.append(mul(G,F)[16])
assert len(vals)==8 and len(set(vals))==1
print("PASS: 8 constant assignments, invariant degree-16 coefficient")
print("No zero-coefficient cardinality or 106.23-bit improvement established")
