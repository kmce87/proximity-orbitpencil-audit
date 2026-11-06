#!/usr/bin/env python3
"""GF(2) symbolic top-coefficient identity for binary CorePencil.
A necessary algebraic identity, NOT a Lean proof or new score.
Original degrees: L=2048, Fl=4096, second term degree <=2048.
"""
from itertools import product

def add(*ps):
    s=set()
    for p in ps:
        for e in p:
            if e in s:s.remove(e)
            else:s.add(e)
    return s

def mul(p,q):
    s=set()
    for a in p:
        for b in q:
            e=a+b
            if e in s:s.remove(e)
            else:s.add(e)
    return s

def power(p,n):
    r={0}
    for _ in range(n):r=mul(r,p)
    return r

def test(a,c):
    # Scale exponents by 1024: LW=2, Fl=4, Rtop=18, Cp max=16.
    L={2}
    Fs=[add({4}, {2} if x else set()) for x in a]
    G={0}
    for x in c:G=mul(G,add(L,{0} if x else set()))
    F={0}
    for p in Fs:F=mul(F,p)
    Cp=add(mul(G,F),mul(power(L,3),{12}))
    assert not any(e>16 for e in Cp)
    # Degree-16 coefficient equals sum of second-high Fl coeffs and cq values.
    assert (16 in Cp)==(sum(a+c)%2==1)
    return 16 in Cp

if __name__=='__main__':
    cases=list(product((0,1),repeat=6))
    outcomes=[test(bits[:3],bits[3:]) for bits in cases]
    assert sum(outcomes)==32
    print('PASS: 64/64 GF(2) coefficient cases; 32 cancel degree-16 term.')
    print('Necessary condition: coeff_16384(Cp) = sum_t coeff_2048(Fl_t) - sum_j cq_j,')
    print('assuming monic LW degree 2048, Fl=X^4096 + degree<=2048.')
    print('NOT tested: actual 420-row values, >=129-row collision, Lean kernel, verifier.')
