#!/usr/bin/env python3
"""N8: kernel of Phi_(r-4) on quotient labels L_Y(D) for structured Y = q * P_f (D = P_d, d = r + f) in real BF64 and in the real domain d = 21."""
import sys
from n8_phi import *
def clmul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
    return r
def labels_quot(Ybasis,d):
    # complete Ybasis to D with monomials, labels = L_Y(complement)
    c=linpoly(Ybasis)
    # echelon
    ech=[];comp=[]
    for y in Ybasis:
        for e in ech:y=min(y,y^e)
        if y:ech.append(y);ech.sort(reverse=True)
    for i in range(d):
        v=1<<i
        for e in sorted(ech,reverse=True):v=min(v,v^e)
        if v:
            ech.append(v);ech.sort(reverse=True);comp.append(1<<i)
    return [ev(c,u) for u in comp]
if __name__=="__main__":
    print("pattern check: Y = 0x6c * P_f, r = 8")
    for f in range(0,14):
        d=8+f
        Y=[clmul(0x6c,1<<i) for i in range(f)]
        ell=labels_quot(Y,d)
        assert len(ell)==8
        print(" f'",f,"d",d,"ker",kernel_dim(phi(ell,4)[0]),flush=True)
