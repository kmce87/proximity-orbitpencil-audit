#!/usr/bin/env python3
"""Koala base-field algebraic obstruction; NOT a 273-fibre-family proof.

Hypothesis: fixed 14 leading coefficients, constant/product key and endpoint
values force corrected derivatives into <=12 classes.
V_t(X)=X^273+1+t*X*(X-1) has the same 14 leading coefficients,
constant and endpoint values for all t, yet derivative differences
at zero equal -t, giving 13 distinct classes for t=0,...,12.
"""
Q=(1<<31)-(1<<24)+1
D=273
assert D>=17 and Q>13
def poly(t):
    return {D:1,2:t%Q,1:(-t)%Q,0:1}
def value(p,x):
    return sum(c*pow(x,e,Q) for e,c in p.items())%Q
def derivative_zero(p):
    return p.get(1,0)%Q
base=poly(0)
values=set()
for t in range(13):
    p=poly(t)
    assert all(p.get(k,0)==base.get(k,0) for k in range(D-13,D+1))
    assert p[0]==base[0]==1
    assert value(p,0)==1 and value(p,1)==2
    delta=(derivative_zero(p)-derivative_zero(base))%Q
    assert delta==(-t)%Q
    values.add(delta)
assert len(values)==13
print('PASS: actual Koala base field q =',Q)
print('PASS: 13 distinct derivatives with fixed top 14 coefficients, constant and endpoint values')
print('FALSIFIED: <=12 derivative classes follow from these keys alone')
print('NOT TESTED: actual 273-fibre root-product subfamily; no Lean proof or verifier acceptance')
