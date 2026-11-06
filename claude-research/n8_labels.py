#!/usr/bin/env python3
"""N8 helper: print the 6 labels L_Z(non-pivot monomials) for Z in P_d, BF64, as hex args for n8_class6."""
import sys
from n8_phi import linpoly, ev
d=int(sys.argv[1]);Z=[int(a,16) for a in sys.argv[2:]]
c=linpoly(Z)
piv=[]
ech=[]
for z in Z:
    v=z
    for e in ech:
        if v>>(e.bit_length()-1)&1:v^=e
    ech.append(v);ech.sort(reverse=True);piv.append(v.bit_length()-1)
ell=[ev(c,1<<i) for i in range(d) if i not in piv]
print(' '.join('%x'%e for e in ell))
