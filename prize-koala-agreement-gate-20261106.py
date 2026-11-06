#!/usr/bin/env python3
"""Arithmetic audit of the published 116.13 OrbitPencil proof.
Source: zksecurity/proximity-prize-submissions-lean434,
submissions/reduction-upper/11613/OrbitPencil.lean.
Not a Lean proof or a verifier submission.
"""
from math import comb
n=262144
old_i,new_i=122369,122362
old_agreement=n-old_i
new_agreement=n-new_i
assert old_agreement==139775
assert new_agreement==139782
assert new_agreement-old_agreement==7
# Published: VF_sub_natDegree_lt <258; Q_spec <=255;
# cpoly_natDegree_le <=131071; unsafe window starts at 122369/262144.
K=2**31-2**24+1
candidate_count=comb(511,272)
key_count=512*K**14
fibre=(candidate_count+key_count-1)//key_count
assert fibre>2**61
print('published_agreement=',old_agreement)
print('required_11612_agreement=',new_agreement)
print('additional_agreement_points=',new_agreement-old_agreement)
print('14key_guaranteed_fibre=',fibre)
print('source_proof_degree_bound=131071 (not recomputed from fibre size)')
print('RESULT: 14-key fibre enlargement alone does not discharge the 7-point extension.')
