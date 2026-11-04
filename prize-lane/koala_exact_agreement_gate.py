"""OrbitPencil exact agreement identity: finite-field regression, NOT Lean proof.
From published source: Q=(V0-V-gamma*z)/(z*(z-alpha)),
f1+gamma*f2=R*(V0-gamma*z)/(z*(z-alpha)), cpoly=R*Q.
Hence discrepancy=R*V/(z*(z-alpha)).
"""
p=101
alpha=97
U={2,5,9}
core={1,3,7}
U0={2,4,8}
gamma=11
def product(xs):
    out=1
    for x in xs: out=out*x%p
    return out
def roots(z,S):
    return product((z-r)%p for r in S)
checks=0
for x in range(p):
    z=x
    if z in (0,alpha): continue
    R=roots(x,core); V=roots(z,U); V0=roots(z,U0)
    inv=pow(z*(z-alpha)%p,-1,p)
    Q=(V0-V-gamma*z)*inv%p
    lhs=(R*(V0-gamma*z)*inv-R*Q)%p
    assert lhs==R*V*inv%p
    assert (lhs==0)==(x in core or z in U)
    checks+=1
assert checks==99
print("PASS",checks,"points: discrepancy identity and exact zero-set equivalence")
print("Not a Lean kernel certificate or verifier acceptance")
