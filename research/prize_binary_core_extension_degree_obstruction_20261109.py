#!/usr/bin/env python3
"""Audit of a proposed 63-extra-core-point extension of the official
binary upper CorePencil proof. Necessary degree-budget check ONLY.

Official source: ProximityPrize/SubmissionBinaryUpper/CorePencil.lean
The current proof uses deg(R)=63, deg(Q)<=16383, deg(Y)=64,
row polynomial degree <1048576, and 64-point label fibres.
"""
N=2**21
row_dimension=2**20
fibres=18432
fibre_size=64
core=63
target_index=917378
current_index=917441
extra=current_index-target_index
assert extra==63
existing_agreement=fibres*fibre_size+core
needed_agreement=N-target_index
assert existing_agreement==N-current_index
assert needed_agreement-existing_agreement==extra
q_degree_bound=16383
current_degree_bound=core+fibre_size*q_degree_bound
new_degree_bound=(core+extra)+fibre_size*q_degree_bound
assert current_degree_bound==row_dimension-1
assert new_degree_bound==row_dimension+extra-1
max_q_degree=(row_dimension-1-(core+extra))//fibre_size
assert max_q_degree==16382
print("Current agreement:",existing_agreement)
print("106.23 required agreement:",needed_agreement)
print("Additional core points:",extra)
print("Current degree upper bound:",current_degree_bound)
print("Naively extended degree upper bound:",new_degree_bound)
print("Permitted maximum degree:",row_dimension-1)
print("Required Q-degree upper bound for extension:",max_q_degree)
print("Existing Q-degree upper bound:",q_degree_bound)
print("RESULT: Naive extension fails the existing degree-bound proof.")
print("NOT an impossibility proof: actual polynomial cancellations or a different")
print("construction may allow a smaller degree or better agreement.")
