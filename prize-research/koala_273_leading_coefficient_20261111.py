#!/usr/bin/env python3
"""Necessary 15th-coefficient equality for 273-fibre Koala pencil; not a Lean proof."""
from math import comb
P=101
def poly(roots):
    a=[1]
    for r in roots:
        b=[0]*(len(a)+1)
        for i,c in enumerate(a):
            b[i]=(b[i]-r*c)%P
            b[i+1]=(b[i+1]+c)%P
        a=b
    return a
a,b=poly((1,2,6,9)),poly((0,2,7,9))
assert a[-1]==b[-1]==1 and a[-2]==b[-2] and a[-3]!=b[-3]
assert max(i for i in range(len(a)) if a[i]!=b[i])==2
q=2**31-2**24+1
assert 511+256*512==131583
assert 511+255*512==131071
assert comb(511,273)//(q**15*512)<2**59
print("PASS: 15th leading coefficient equality necessary; 15-key generic pigeonhole bound insufficient")
