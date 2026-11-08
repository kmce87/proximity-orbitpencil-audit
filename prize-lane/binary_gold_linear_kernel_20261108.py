#!/usr/bin/env python3
"""Exact BF64 Gold polar-kernel restriction on the fixed 21-bit binary domain.
Standalone numerical GF(2) checker, not Lean or independent acceptance.
"""
MOD=(1<<64)|(1<<4)|(1<<3)|(1<<1)|1
N=21
def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a>>64:a^=MOD
    return z
def trace(a):
    z=0
    for _ in range(64):
        z^=a;a=mul(a,a)
    assert z in (0,1)
    return z
def encode_polar(a):
    out=0;k=0
    for i in range(N):
        for j in range(i+1,N):
            if trace(mul(a,(1<<(2*i+j))^(1<<(i+2*j)))):out|=1<<k
            k+=1
    return out
def kernel(cols):
    piv={};ker=[]
    for j,c in enumerate(cols):
        v=c;combo=1<<j
        while v:
            p=v.bit_length()-1
            if p not in piv:
                piv[p]=(v,combo);break
            v^=piv[p][0];combo^=piv[p][1]
        if not v:ker.append(combo)
    return len(piv),ker
def linear_restriction(a):
    return sum(trace(mul(a,1<<(3*i)))<<i for i in range(N))
if __name__=='__main__':
    rank,ker=kernel([encode_polar(1<<i) for i in range(64)])
    assert rank==57 and len(ker)==7
    assert all(encode_polar(a)==0 for a in ker)
    lin=[linear_restriction(a) for a in ker]
    linrank,lin_ker=kernel(lin)
    assert linrank==3 and len(lin_ker)==4
    assert all(linear_restriction(a^b)==linear_restriction(a)^linear_restriction(b) for a,b in zip(ker,ker[1:]))
    assert sum(1 for mask in range(128) if linear_restriction(
        __import__('functools').reduce(lambda x,i:x^ker[i] if mask>>i&1 else x,range(7),0)
    )==0)==16
    print('polar rank',rank,'polar kernel dimension',len(ker))
    print('kernel basis',*[hex(a) for a in ker])
    print('linear restriction rank',linrank,'nullity',len(lin_ker))
    print('linear restrictions',*[hex(a) for a in lin])
    print('identically-zero Gold forms on V:',1<<len(lin_ker))
    print('nonzero linear Gold forms on V:',(1<<len(ker))-(1<<len(lin_ker)))
    print('zeros per nonzero linear form:',1<<(N-1))
    print('full zero count for identically-zero form:',1<<N)
    print('Not a valid IRS challenge-count or agreement certificate.')
