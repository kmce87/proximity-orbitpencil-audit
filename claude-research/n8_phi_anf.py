#!/usr/bin/env python3
import sys
from n8_phi import *
from n8_phi_ideal import labels_quot, clmul
from n8_phi_words import word_table
q=int(sys.argv[1],16);r=int(sys.argv[2])
for f in [int(a) for a in sys.argv[3:]]:
    d=r+f
    Y=[clmul(q,1<<i) for i in range(f)]
    ell=labels_quot(Y,d)
    vecs,names=phi(ell,r-4);kd,ker=kernel_dim(vecs,want=True)
    print("f'",f,"ker",kd)
    for k in ker[:3]:
        terms=[names[i] for i in range(len(names)) if k>>i&1]
        by={}
        for t,T in terms:by.setdefault(len(T),[]).append(T)
        print("  #terms by |T|:",{s:len(v) for s,v in sorted(by.items())},"t-values sizes",sorted(set(t for t,_ in terms)))
        tab=word_table(k,names,r)
        print("  weight",bin(tab).count("1"))
        if f<=2:print("  terms:",terms[:40])
