#!/usr/bin/env python3
"""Lane B: genuine split square-free degree-273 root-product obstruction.

Falsifiable hypothesis: root-product membership and a fixed product key alone
force <=12 derivative classes in a 512th-root subgroup of the Koala base field.
Counterexample: 13 products. Top 14 coefficients are NOT held fixed.
No official upper claim follows.
"""
q = (1 << 31) - (1 << 24) + 1
assert q == 2130706433
assert (q - 1) % 512 == 0
g = pow(3, (q - 1) // 512, q)
assert pow(g, 512, q) == 1 and pow(g, 256, q) != 1
fixed_exponents = tuple(range(20, 291))
assert len(fixed_exponents) == 271
values = []
constant_products = []
for j in range(1, 14):
    exponents = fixed_exponents + (j, 512-j)
    assert len(exponents) == len(set(exponents)) == 273
    roots = [pow(g, e, q) for e in exponents]
    assert len(set(roots)) == 273 and all(pow(x, 512, q) == 1 for x in roots)
    product = 1
    reciprocal_sum = 0
    for x in roots:
        product = product * x % q
        reciprocal_sum = (reciprocal_sum + pow(x, -1, q)) % q
    # V(X) = prod(X-r); V'(0)/V(0) = -sum(1/r).
    constant = (-product) % q  # degree 273 odd
    derivative = (-constant * reciprocal_sum) % q
    constant_products.append(constant)
    values.append(derivative)
assert len(set(constant_products)) == 1
assert len(set(values)) == 13
print('field:', q, 'primitive 512th root:', g)
print('genuine root-products:', len(values), 'degree:', 273)
print('fixed constant/product key:', constant_products[0])
print('distinct derivative classes:', len(set(values)))
print('derivatives:', values)
print('FALSIFIED: root-product membership + product key imply <=12 classes')
print('NOT TESTED: fixed top 14 coefficients; full official fibre keys')
print('NO attack, Lean kernel proof, independent acceptance')
