#!/usr/bin/env python3
"""Lane B: exact necessary arithmetic for a hypothetical q^2-valued gamma family.
This does NOT construct the family or prove a Lean theorem.
"""
q = 2**31 - 2**24 + 1
N = 2**59 + 1
fibres = 273
fibre_size = 512
core = 511
agreement = fibres*fibre_size + core
max_degree = 131071
# Historical degree budgets from preceding architecture check:
degree_two_roots = 131583
assert degree_two_roots - fibre_size == max_degree
assert N < q*q < q**6
assert N <= q*q
# alpha outside F_(q^2), in F_(q^6), has orbit of size exactly three
# under x -> x^(q^2) if its orbit is not fixed (3 is prime).
# For coefficients of deltaV in F_q, P_U(X)=deltaV_U(X)-gamma_U*X
# has coefficients in F_(q^2) when gamma_U in F_(q^2).
# Thus P_U(alpha)=0 implies P_U(alpha^(q^2))=P_U(alpha^(q^4))=0.
# alpha's q^2 orbit consists of three distinct nonzero roots.
assert degree_two_roots - 2*fibre_size == 130559
print('q:', q)
print('q^2:', q*q)
print('required N:', N)
print('agreement positions:', agreement)
print('two-root degree budget:', degree_two_roots)
print('one extra root degree budget:', degree_two_roots - fibre_size)
print('two extra conjugate roots degree budget:', degree_two_roots - 2*fibre_size)
print('PASS: conditional q^2 orbit supplies TWO extra roots and clears degree ceiling')
print('UNPROVED: existence of >2^59 distinct challenges with gamma in F_(q^2)')
