#!/usr/bin/env python3
"""Exact rational upper bound on pinned FreeOrder rank-comparison at d=4.
Not a Lean proof or a certificate for the whole protocol.
"""
from fractions import Fraction as F
n=262144
k=131072
radius=F(334773390,1073741824)
eps=1-radius
# k <= floor((1-theta)*eps*n) forces theta <= theta_max
th=1-F(k,1)/(eps*n)
assert 0<th<F(1,3)
# rankSavingExponent(theta) = 2theta/(5+theta) < 1/8, hence 4^exponent < 4
assert F(2)*th/(5+th)<F(1,8)
# (1-theta)*eps/2 <= 1/2, theta^3 < 1/27.
# Thus scalar rank-comparison expression < (1/27)/262144*(1/2)*4 = 1/3538944 < 1
bound=F(4,27*262144*2)
assert bound==F(1,3538944) and bound<1
print('Koala 69.00 target radius:',radius)
print('agreement:',eps)
print('theta_max:',th)
print('d=4 scalar rank expression <',bound,'< 1: TRUE')
print('RESULT: pinned sufficient scalar rank condition cannot hold at d=4.')
print('CAVEAT: does not exclude other dimension/rank methods or d>4.')
