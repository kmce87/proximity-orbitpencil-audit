#!/usr/bin/env python3
"""Exact integer gates for published Koala OrbitPencil architecture.
Reproduce: python3 prize-lane/koala_11612_architecture_gate_20261107.py
NOT a Lean certificate. Official source: ProximityPrize/SubmissionUpper/OrbitPencil.lean.
"""
from math import comb
N=262144
K=131072
FIELD=2**31-2**24+1
KEY_14=FIELD**14*512
KEY_15=FIELD**15*512
CHALLENGES=2**59

def score_ok(agreement, centibits):
    # 2^(-centibits/100) <= (agreement / 2^18)^128
    return agreement**12800 * 2**centibits >= 2**(18*12800)

minimum=next(a for a in range(139775,139900) if score_ok(a,11612))
assert minimum==139782 and not score_ok(minimum-1,11612)
assert score_ok(139775,11613)
# Published: 272 fibres, 511 core, 14 top coefficients, one product key.
# Core 512: degree bound becomes exactly K, not strictly below K.
# 273 fibres with 14 keys: degree difference <259, two roots => Q <=256.
# 273 fibres with 15 keys: Q <=255, but pigeonhole cardinality fails.
assert comb(511,273)>KEY_14*CHALLENGES
assert comb(511,273)<KEY_15*CHALLENGES
assert 511+512*255 == K-1
assert 512+512*255 == K
assert 511+512*256 == K+511
print('KOALA 116.12 EXACT ARCHITECTURE GATE')
print('published agreement=139775, min agreement for 11612=',minimum,'extra=',minimum-139775)
print('272 fibres + 512 core: agreement=',272*512+512,'degree_cap=',512+512*255,'allowed_max=',K-1)
print('273 fibres + 511 core, 14 top keys: agreement=',273*512+511,'degree_cap=',511+512*256,'allowed_max=',K-1)
print('273 fibres + 511 core, 15 top keys: degree_cap=',511+512*255,'allowed_max=',K-1)
print('14-key pigeonhole holds:',comb(511,273)>KEY_14*CHALLENGES)
print('15-key pigeonhole holds:',comb(511,273)>KEY_15*CHALLENGES)
print('15-key available cardinality floor:',comb(511,273)//KEY_15,'required:',CHALLENGES+1)
print('PASS: naive core enlargement / 273-fibre same-key / extra-key approaches cannot certify 11612 with published inequalities')
