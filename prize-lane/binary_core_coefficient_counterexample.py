#!/usr/bin/env python3
"""Exact characteristic-two audit of the published binary CorePencil top
correction coefficient. Independent Python arithmetic; NOT a Lean certificate.
Source compared: ProximityPrize/SubmissionBinaryUpper/{LabelFamily,LabelSpace,
LabelTable,FlatPoly}.lean at proximity-prize/proximity-prize main (2026-11-03).
"""
M=(1<<64)|(1<<4)|(1<<3)|(1<<1)|1
def mul(a,b):
    c=0
    while b:
        if b&1:c^=a
        b>>=1
        a<<=1
        if a>>64:a^=M
    return c
def ev(c,x):
    z=0
    for v in c:
        z^=mul(v,x)
        x=mul(x,x)
    return z
def poly(basis):
    c=[1]
    for u in basis:
        v=ev(c,u)
        n=[0]*(len(c)+1)
        for i,z in enumerate(c):
            n[i]^=mul(z,v)
            n[i+1]^=mul(z,z)
        c=n
    return c
def kernel(rows):
    rows=list(rows);piv=[]
    for j in range(15):
        i=next((i for i in range(len(piv),len(rows)) if rows[i]>>j&1),None)
        if i is None:continue
        rows[i],rows[len(piv)]=rows[len(piv)],rows[i]
        for k in range(len(rows)):
            if k!=len(piv) and rows[k]>>j&1:rows[k]^=rows[len(piv)]
        piv.append(j)
    assert len(piv)==3
    basis=[]
    for f in range(15):
        if f in piv:continue
        z=1<<f
        for i,p in enumerate(piv):
            if rows[i]>>f&1:z^=1<<p
        assert all((z&r).bit_count()%2==0 for r in rows)
        basis.append(z)
    assert len(basis)==12
    return basis
def beta(s,j):
    low=(s&-s).bit_length()-1
    return j%(1<<low)+(1<<(low+1))*(j//(1<<low))
def result(nu0):
    ys=poly([1<<i for i in range(6)])
    ell=[ev(ys,1<<(6+i)) for i in range(15)]
    def label(bits):
        x=0
        for i in range(15):
            if bits>>i&1:x^=ell[i]
        return x
    lw=poly(ell[:11])
    # LabelTable first row (q1,q2,q3,s0,s1,s2)=(1,2,4,8,15,7).
    s=(8,15,7);q=(1,2,4)
    # Valid LabelFamily.Param: row0, jr=0, aa=ee=e0=e1=0,
    # rr=y0 (pivot 0), mr=(1,2,4), jn=(nu0,0,0).
    jn=(nu0,0,0)
    flats=[]
    for t in range(3):
        rhoLin=s[0] if t==2 else 0
        nuLin=beta(s[t],jn[t])
        rows=[s[t]<<11, 1|(rhoLin<<11),
              (2<<(t)) | (nuLin<<11)] # reduced m=(1,2,4) inserts at pivot0
        # Correct inserted m_t occupies y bits 1,2,3:
        rows[2]=(2<<(t))|(nuLin<<11)
        flats.append(poly([label(v) for v in kernel(rows)]))
    # Cp = Gq*Fprod - (LW^3)*X^12288.
    # Its X^16384 coefficient is sum of flat X^2048
    # coefficients + sum of the 3 selected LW(q) constants.
    top=flats[0][-2]^flats[1][-2]^flats[2][-2]
    for z in q:top^=ev(lw,label(z<<11))
    return top
def main():
    a,b=result(0),result(1)
    assert a==0x0e59c693810b0892,hex(a)
    assert b==0xba04f7acef7f2972,hex(b)
    assert a!=b
    print(f'PASS: two valid Params have Cp[X^16384] = {a:#018x}, {b:#018x}')
    print('Common-top-coefficient cancellation over the entire family is FALSE.')
    print('No improved official binary attack or Lean kernel certificate asserted.')
if __name__=='__main__':main()
