#!/usr/bin/env python3
"""Arithmetic-only necessary degree budget for seven extra OrbitPencil core points.
Source: zksecurity/proximity-prize-submissions-lean434,
submissions/reduction-upper/11613/OrbitPencil.lean.
Not a Lean proof or an accepted attack.
"""
N=262144
historical_core=511
block_agreement=272*512
historical_Q_degree=255
composition_degree=512
max_code_degree=131071
historical_agreement=historical_core+block_agreement
assert historical_agreement==139775
assert historical_core+historical_Q_degree*composition_degree==max_code_degree
required=historical_agreement+7
new_core=historical_core+7
assert required==139782
old_Q_degree_at_new_core=new_core+historical_Q_degree*composition_degree
assert old_Q_degree_at_new_core==131078>max_code_degree
max_Q_degree=(max_code_degree-new_core)//composition_degree
assert max_Q_degree==254
assert new_core+max_Q_degree*composition_degree==130566
print('Historical agreement:',historical_agreement)
print('Required agreement:',required)
print('Proposed core size:',new_core)
print('Degree with unchanged Q:',old_Q_degree_at_new_core)
print('Maximum allowed degree:',max_code_degree)
print('Necessary Q degree cap:',max_Q_degree)
print('Status: original Q<=255 bound does not certify 7 added core points')
