#!/usr/bin/env python3
"""N8: at r = 9 the kernel of Phi_5 is forced (dim >= 61), so rank says nothing.  Information set decoding for low-weight words of ker Phi_5, as truth tables on the 512 characters.
A random [512,61] code has minimum weight about 150 (Gilbert-Varshamov); a word of weight <= 80 would be structural.  Control: Krylov chain of length 9.
Usage: n8_isd9.py iterations"""
import sys, random
from n8_phi import *
from n8_phi_ideal import labels_quot, clmul
from n8_phi_words import word_table
def tables(ell):
    vecs,names=phi(ell,5);kd,ker=kernel_dim(vecs,want=True)
    return kd,[word_table(k,names,9) for k in ker]
def isd(tabs,iters,rng,N=512):
    k=len(tabs);best=10**9;hist={}
    for it in range(iters):
        rows=tabs[:]
        positions=rng.sample(range(N),N)
        piv=0;used=[]
        for p in positions:
            if piv==k:break
            j=next((i for i in range(piv,k) if rows[i]>>p&1),None)
            if j is None:continue
            rows[piv],rows[j]=rows[j],rows[piv]
            for i in range(k):
                if i!=piv and rows[i]>>p&1:rows[i]^=rows[piv]
            piv+=1
        for i in range(piv):
            w=bin(rows[i]).count("1")
            if w<best:best=w
            for j in range(i+1,piv):
                w=bin(rows[i]^rows[j]).count("1")
                if w<best:best=w
    return best
if __name__=="__main__":
    iters=int(sys.argv[1]);rng=random.Random(9)
    cases=[("Krylov chain length 9 (f'=0)",[1<<i for i in range(9)])]
    cases.append(("random labels",[rng.getrandbits(64) for _ in range(9)]))
    for q in (0x6c,0xd8,0x1b0,0x96,0x155):
        f=12
        Y=[clmul(q,1<<i) for i in range(f)]
        cases.append(("real D, Y = %x*P_12"%q,labels_quot(Y,21)))
    # first-words Y = P_12, and random Y containing P_7
    cases.append(("real D, Y = P_12",labels_quot([1<<i for i in range(12)],21)))
    for s in range(2):
        Y=[1<<i for i in range(7)]
        while len(Y)<12:
            c=rng.getrandbits(21);t=Y+[c]
            ech=[]
            ok=True
            for v in t:
                for e in ech:v=min(v,v^e)
                if v:ech.append(v);ech.sort(reverse=True)
                else:ok=False
            if ok:Y=t
        cases.append(("real D, random Y containing P_7",labels_quot(Y,21)))
    for name,ell in cases:
        kd,tabs=tables(ell)
        print(name,"ker",kd,"min weight found",isd(tabs,iters,rng),flush=True)
