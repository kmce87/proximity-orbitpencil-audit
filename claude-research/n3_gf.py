#!/usr/bin/env python3
"""Small shared toolbox for the N3 toy checks: GF(2^16) with log tables (x^16+x^5+x^3+x+1) and polynomial helpers.
Polynomials are coefficient lists, lowest degree first."""
import numpy as np
POLY,MB=0x1002B,16
ORDER=65535
def _rawmul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a>>MB:a^=POLY
    return r
def _rawpow(a,e):
    r=1
    while e:
        if e&1:r=_rawmul(r,a)
        a=_rawmul(a,a);e>>=1
    return r
GEN=next(g for g in range(2,65536) if all(_rawpow(g,ORDER//p)!=1 for p in (3,5,17,257)))
EXP=np.zeros(2*ORDER+2,dtype=np.int64);LOG=np.zeros(65536,dtype=np.int64)
_x=1
for _i in range(ORDER):
    EXP[_i]=_x;LOG[_x]=_i;_x=_rawmul(_x,GEN)
EXP[ORDER:2*ORDER]=EXP[:ORDER]
def mul(a,b):
    return 0 if a==0 or b==0 else int(EXP[LOG[a]+LOG[b]])
def inv(a):
    assert a
    return int(EXP[(ORDER-LOG[a])%ORDER])
def fpow(a,e):
    if a==0:return 0 if e else 1
    return int(EXP[(int(LOG[a])*e)%ORDER])
def vmul(c,v):
    """scalar times numpy vector"""
    if c==0:return np.zeros_like(v)
    r=np.zeros_like(v);m=v!=0
    r[m]=EXP[LOG[c]+LOG[v[m]]]
    return r
def vvmul(u,v):
    r=np.zeros_like(u);m=(u!=0)&(v!=0)
    r[m]=EXP[LOG[u[m]]+LOG[v[m]]]
    return r
def locator(pts):
    P=np.array([1],dtype=np.int64)
    for v in pts:
        Q=np.zeros(len(P)+1,dtype=np.int64)
        Q[1:]^=P
        Q[:-1]^=vmul(v,P)
        P=Q
    return P
def pmul(A,B):
    A=np.asarray(A,dtype=np.int64);B=np.asarray(B,dtype=np.int64)
    R=np.zeros(len(A)+len(B)-1,dtype=np.int64)
    for i,a in enumerate(A):
        if a:R[i:i+len(B)]^=vmul(int(a),B)
    return R
def deg(P):
    nz=np.nonzero(P)[0]
    return int(nz[-1]) if len(nz) else -1
def evalp(P,x):
    r=0
    for c in reversed(list(P)):
        r=mul(r,x)^int(c)
    return r
def powers(xs,m):
    """matrix[j,i]=xs[i]^j for j<m"""
    xs=np.asarray(xs,dtype=np.int64)
    M=np.zeros((m,len(xs)),dtype=np.int64)
    M[0]=1
    for j in range(1,m):
        M[j]=vvmul(M[j-1],xs)
    return M
def span(gens):
    s=[0]
    for g in gens:
        s=s+[u^g for u in s]
    return s
class Elim:
    """Incremental row reduction over GF(2^16); rows are numpy int64 vectors."""
    def __init__(self,ncols):
        self.n=ncols;self.rows=[];self.piv=[]
    def add(self,row):
        row=row.copy()
        for r,p in zip(self.rows,self.piv):
            c=int(row[p])
            if c:row^=vmul(c,r)
        nz=np.nonzero(row)[0]
        if len(nz)==0:return False
        p=int(nz[0]);row=vmul(inv(int(row[p])),row)
        self.rows.append(row);self.piv.append(p)
        return True
    @property
    def rank(self):return len(self.rows)
    def nullspace(self):
        """basis of right kernel"""
        n=self.n
        A=np.array(self.rows,dtype=np.int64) if self.rows else np.zeros((0,n),dtype=np.int64)
        # back-substitute to RREF
        piv=list(self.piv)
        for i in range(len(piv)):
            for k in range(len(piv)):
                if k!=i and A[k,piv[i]]:
                    A[k]^=vmul(int(A[k,piv[i]]),A[i])
        free=[c for c in range(n) if c not in set(piv)]
        B=[]
        for f in free:
            v=np.zeros(n,dtype=np.int64);v[f]=1
            for i,p in enumerate(piv):
                v[p]=A[i,f]
            B.append(v)
        return B
