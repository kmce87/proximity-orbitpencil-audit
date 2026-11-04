#!/usr/bin/env python3
"""Koala 15-root swap obstruction. Not a Lean/prize certificate."""
from random import Random
q=(1<<31)-(1<<24)+1
rng=Random(20261104)
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%q
 return c
def recover(W,top,constant,k):
 m=len(W)-1
 P=[0]*(k+1); P[k]=1
 for r in range(1,min(k,14)+1):
  known=sum(W[m-j]*P[k-r+j] for j in range(1,min(r,m)+1))
  P[k-r]=(top[r-1]-known)%q
 if k==15: P[0]=constant*pow(W[0],-1,q)%q
 else: assert W[0]*P[0]%q==constant
 return P
for k in range(1,16):
 W=[rng.randrange(1,q)]+[rng.randrange(q) for _ in range(273-k-1)]+[1]
 P=[rng.randrange(1,q)]+[rng.randrange(q) for _ in range(k-1)]+[1]
 V=mul(W,P)
 assert recover(W,[V[-1-r] for r in range(1,15)],V[0],k)==P
print("PASS: exact modular reconstruction k=1..15")
print("First potentially nontrivial exchange: k=16")
print("No Lean certificate or independent acceptance")
