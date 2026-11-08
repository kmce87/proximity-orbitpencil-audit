#!/usr/bin/env python3
"""Exact necessary feasibility gate for pinned ArkLib FreeOrder d=2 Koala 69.00.
Not a Lean proof or an extractor certificate.
"""
from fractions import Fraction
from math import floor, ceil
n = 2**18
D = 2**17
radius = Fraction(334773390, 2**30)
epsilon = 1-radius
A = ceil(epsilon*n)
# K=floor((1-theta)*epsilon*n)>=D requires theta <= theta_max.
theta_max = 1-Fraction(D,1)/(epsilon*n)
assert 0 < theta_max < 1
assert floor(theta_max*(2**3)/16) == 0
assert floor(theta_max*(3**3)/16) == 0
assert floor(theta_max*(4**3)/16) == 1
print('target: ProtocolClaim 6900 334773390 1073741824')
print('agreement fraction:',epsilon,'A=ceil(epsilon*n):',A)
print('theta_max with K>=D:',theta_max,'=',float(theta_max))
for d in (2,3,4):
 print('d=',d,'m=',d**3,'max H=floor(theta*m/16):',floor(theta_max*d**3/16))
print('RESULT: d=2 rectangular box width H=0 at every admissible theta; d=3 likewise.')
print('LIMITATION: this excludes this specific rectangular rank-saving instantiation, not all second-order theorems.')
