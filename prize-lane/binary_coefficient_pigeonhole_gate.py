#!/usr/bin/env python3
"""Lane B: exact cardinality obstruction for uniform leading-coefficient pigeonhole.
Source: official CorePencil.lean card_Param, NN and LabelFamily.lean K=GF(2^15).
This does not calculate the actual coefficient distribution or prove impossibility.
"""
T=420*32*2047*(1023*1022*1021)*512*4
NN=2**64+1
K=2**15
assert T==60144973141589360640
assert T>=NN
assert T<K*NN
assert T//K==1835478916674480
assert T//K<NN
print('parameters:',T)
print('needed distinct parameters:',NN)
print('coefficient field classes:',K)
print('pigeonhole guaranteed largest class:',(T+K-1)//K)
print('required class:',NN)
print('Uniform-class pigeonhole insufficient: PASS')
