#!/usr/bin/env python3
"""Lane B conditional one-fibre trade gate; not a Lean certificate.

Assume a complete 64-point fibre was supported exclusively by one
linear (Y-a) factor in Q(Y). Remove that factor and insert 63 disjoint
simple X-roots, with all other roots unchanged.
"""
N=2**21
old_index=917441
next_index=917378
old_agreement=N-old_index
required=N-next_index
def score_ok(bits,index):
    return 2**bits*(N-index)**12800 >= N**12800
assert old_agreement==1179711 and required==1179774
assert required-old_agreement==63
assert score_ok(10624,old_index)
assert not score_ok(10623,old_index)
assert score_ok(10623,next_index)
assert not score_ok(10623,next_index+1)
# Removing one (Y-a) factor frees 64 degrees in X;
# adding 63 new X roots spends 63 degrees.
assert 1048575-64+63==1048574
new_agreement=old_agreement-64+63
assert new_agreement==1179710
assert required-new_agreement==64
assert not score_ok(10623,N-new_agreement)
print("PASS: conditional fibre trade gives 1,179,710 agreement; 64 short")
print("This does not exclude other constructions, Lean proof or verifier acceptance.")
