#!/usr/bin/env python3
"""Exact Gold polar-map kernel for the protected BF64 21-bit evaluation subspace.
Numerical GF(2) certificate only, NOT a Lean proof or a prize submission.
Run from the same directory as binary_gold_rank_gate_20261108.py.
"""
from binary_gold_rank_gate_20261108 import matrix
N=21
def encode(rows):
    v=0;k=0
    for i in range(N):
        for j in range(i+1,N):
            v|=((rows[i]>>j)&1)<<k;k+=1
    return v
def rank_kernel(columns):
    pivots={};kernel=[]
    for j,col in enumerate(columns):
        v=col;combination=1<<j
        while v:
            bit=v.bit_length()-1
            if bit not in pivots:
                pivots[bit]=(v,combination);break
            v^=pivots[bit][0];combination^=pivots[bit][1]
        if not v:kernel.append(combination)
    return len(pivots),kernel
cols=[encode(matrix(1<<j)) for j in range(64)]
rank,ker=rank_kernel(cols)
assert rank==57 and len(ker)==7
assert all(encode(matrix(a))==0 for a in ker)
assert len(set(ker))==7
for i,j in [(0,1),(0,63),(17,23),(31,55)]:
    assert encode(matrix((1<<i)^(1<<j)))==(cols[i]^cols[j])
print('polar-map rank:',rank,'kernel dimension:',64-rank)
print('kernel basis:',*[hex(a) for a in ker])
print('exact number of rank-zero coefficients, including a=0:',1<<(64-rank))
print('nonzero rank-zero coefficients:',(1<<(64-rank))-1)
print('status: exact GF(2) linear algebra only; no 106.23-bit attack')
