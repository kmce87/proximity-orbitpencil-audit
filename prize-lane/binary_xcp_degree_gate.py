#!/usr/bin/env python3
"""Gate: does X*Cp retain the published <=16384 degree guarantee?
Official LabelFamily.lean: Cp_natDegree_le <=16384.
Official CorePencil.lean: Q_natDegree_le <=16383.
This is a necessary-condition test, not a proof of nonzero official coefficients.
"""
D=16384
CORE=62
FIBRE_DEGREE=64
ROW_MAX=1048575
def degree_gf2(bits): return bits.bit_length()-1
for bits in (1,3,1<<D,(1<<D)|7):
    assert degree_gf2(bits<<1)==degree_gf2(bits)+1
assert degree_gf2((1<<D)<<1)==D+1
assert CORE+FIBRE_DEGREE*(D-1)==1048574
assert CORE+FIBRE_DEGREE*D==1048638
assert CORE+FIBRE_DEGREE*D>ROW_MAX
print("PASS: the existing Cp degree bound alone is insufficient for X*Cp admissibility")
print("NEXT: prove coeff(Cp,16384)=0 for selected parameters or find alternative degree saving")
