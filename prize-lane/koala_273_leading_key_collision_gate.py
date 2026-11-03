#!/usr/bin/env python3
"""Lane B: test whether previous 13 root products share even first leading coefficient.

Exact finite-field test. Not a Koala upper certificate.
"""
q=(1<<31)-(1<<24)+1
g=pow(3,(q-1)//512,q)
assert pow(g,512,q)==1 and pow(g,256,q)!=1
base=tuple(range(20,291))
leading=[]; derivatives=[]; constants=[]
for j in range(1,14):
    exps=base+(j,512-j)
    roots=[pow(g,e,q) for e in exps]
    assert len(set(roots))==273
    prod=1
    for r in roots: prod=prod*r%q
    constant=(-prod)%q
    # coefficient of X^272 in monic degree-273 root product
    lead=(-sum(roots))%q
    deriv=(-constant*sum(pow(r,-1,q) for r in roots))%q
    constants.append(constant);leading.append(lead);derivatives.append(deriv)
assert len(set(constants))==1
assert len(set(leading))==13
assert len(set(derivatives))==13
# For this special pair family, differences of derivative and leading coefficient
# coincide up to the fixed multiplicative factor V(0).
for a in range(13):
    for b in range(13):
        assert (derivatives[a]-derivatives[b])%q == (constants[0]*(leading[a]-leading[b]))%q
print('PASS: common product key, but 13 distinct FIRST leading coefficients')
print('PASS: derivative differences = V(0) * leading-coefficient differences')
print('FALSIFIED: prior 13 witnesses share first leading coefficient')
print('NO 115.46-bit attack, Lean certificate, or independent acceptance')
