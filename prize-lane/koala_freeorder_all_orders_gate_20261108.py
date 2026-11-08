#!/usr/bin/env python3
"""Exact rational obstruction for pinned FreeOrder scalar rank comparison.
Not a Lean proof. Assumptions: 0<theta<=theta_max, 0<d<K<=n,
0<epsilon<=1, and FreeOrder's rankSavingExponent=2theta/(5+theta).
"""
from fractions import Fraction as F
n=2**18
k=2**17
agreement=F(369484217,536870912)
theta_max=1-F(k,n)/agreement
assert theta_max==F(101048761,369484217)
assert 0<theta_max<F(1,3)
# d < K <= n. For 0<theta<1/3, 0<2theta/(5+theta)<1/8.
# d^exponent < d^(1/8) < 5 because d<n=262144<5^8.
assert n < 5**8
assert 2*F(1,3)/(5+F(1,3))==F(1,8)
# Thus scalar < (1/27)/262144 * (1/2) * 5.
upper=F(5,27*262144*2)
assert upper < 1
print('theta_max=',theta_max,'=',float(theta_max))
print('d upper=',n,'and 5^8=',5**8)
print('uniform rank scalar strictly less than',upper,'=',float(upper))
print('Required scalar >1: impossible for every admissible 0<d<K<=n.')
print('Scope: FreeOrder sufficient condition only; not all derivative approaches.')
