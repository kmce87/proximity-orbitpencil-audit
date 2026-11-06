#!/usr/bin/env python3
"""Necessary geometry gate for proposed Koala 116.12 core extension.
Not a Lean proof, field witness, or general impossibility theorem.
"""
FIBRE=512
CORE=511
BLOCK=139264
TARGET_INDEX=122362
N=262144
DEGREE_MAX=131071
assert BLOCK+CORE == N-122369
needed=N-TARGET_INDEX-BLOCK
assert needed==518
assert needed>FIBRE
assert needed-CORE==7
assert FIBRE-CORE==1
assert needed-FIBRE==6
assert needed+254*FIBRE<=DEGREE_MAX
print('target agreement:',N-TARGET_INDEX)
print('needed fixed-core positions:',needed)
print('maximum positions in original 512-point fibre:',FIBRE)
print('excess beyond fibre:',needed-FIBRE)
print('degree with quotient 254:',needed+254*FIBRE)
print('RESULT: proposed seven-extra-core-points route cannot stay in one original fibre')
print('NOT a general 116.12 impossibility; NO Lean/independent verifier acceptance')
