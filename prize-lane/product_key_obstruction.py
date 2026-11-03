#!/usr/bin/env python3
"""Practical falsification of the naive 256 -> 63 product-key compression.

This is a finite exact-arithmetic calculation and algebraic audit, NOT a
proof that no improved OrbitPencil construction exists.

For m=136 subsets U of {1,...,255}, each V_U(0)=(-1)^m eta^sum(U)
where eta is a primitive 256th root. On a fixed rational pencil with
numerator V0 - V_U + gamma_U H and denominator T(T-alpha), divisibility
by T implies
    V0(0) - V_U(0) + gamma_U H(0) = 0.
If H(0)=0, the constants must all match, so full product residues must
match. If H(0)!=0, gamma_U depends ONLY on the product residue, giving
at most 256 different slopes. This is an algebraic dichotomy, not a
claim about other denominator designs, other code structures, or the
sufficiency of the full coefficient-key condition.

Exact global distribution of product residues: cyclic character inversion.
For a character of order d=2^j>1 on Z/256, the coefficient of u^m in
prod_{b=1}^{255}(1+u*chi(b)) is
    (-1)^(m+floor(m/d))*C(256/d-1, floor(m/d)).
Inverse DFT via Ramanujan sums yields exact cardinalities of every residue.
"""
from itertools import combinations
from math import comb

P = 2130706433
C = 256
M = 136
B = P**6 // 2**128


def ramanujan_prime_power_two(d, residue):
    if d == 1:
        return 1
    if residue % d == 0:
        return d // 2
    if residue % (d // 2) == 0:
        return -(d // 2)
    return 0


def character_coefficient(columns, selected, order):
    if order == 1:
        return comb(columns - 1, selected)
    assert columns % order == 0 and order > 1 and order & (order - 1) == 0
    q = columns // order
    j = selected // order
    return (-1)**(selected + j) * comb(q - 1, j)


def exact_residue_counts(columns, selected):
    assert columns >= 4 and columns & (columns - 1) == 0
    divisors = [1 << h for h in range(columns.bit_length())]
    coefficients = {d: character_coefficient(columns, selected, d) for d in divisors}
    counts = []
    for residue in range(columns):
        numerator = sum(coefficients[d] * ramanujan_prime_power_two(d, residue)
                        for d in divisors)
        assert numerator % columns == 0
        counts.append(numerator // columns)
    assert sum(counts) == comb(columns - 1, selected)
    return counts


def main():
    # Validate the character formula against exhaustive small-instance
    # subsets before applying it to the 256-column case.
    for columns, m in ((8, 3), (16, 7), (32, 5)):
        observed = [0] * columns
        for U in combinations(range(1, columns), m):
            observed[sum(U) % columns] += 1
        assert observed == exact_residue_counts(columns, m)

    counts = exact_residue_counts(C, M)
    total = comb(C - 1, M)
    assert all(x > 0 for x in counts)
    richest = sorted(counts, reverse=True)
    best_63 = sum(richest[:63])
    assert best_63 * 256 < total * 64
    spread = max(counts) - min(counts)
    print(f'p={P}; C={C}; m={M}; target distinct slopes={B+1}')
    print(f'total candidates={total}')
    print(f'min class size={min(counts)}')
    print(f'max class size={max(counts)}')
    print(f'global class-size spread / average (exact) = {spread*C}/{total}')
    print(f'fraction in the largest 63 of 256 classes (exact) = {best_63}/{total}')

    # Counterexample to treating equality of sums modulo 64 as equality
    # of V_U(0): the difference of sums is 64 modulo 256.
    U = set(range(1, M + 1))
    W = (U - {100}) | {164}
    assert len(W) == M and 0 not in W
    assert (sum(W) - sum(U)) % C == 64
    assert sum(W) % 64 == sum(U) % 64
    eta = pow(3, (P - 1) // C, P)
    assert pow(eta, C, P) == 1 and pow(eta, C // 2, P) != 1
    assert pow(eta, 64, P) != 1
    v0_U = pow(eta, sum(U), P) # m even, sign = +1
    v0_W = pow(eta, sum(W), P)
    assert v0_U != v0_W
    print('EXACT COUNTEREXAMPLE: same residue mod64, different V_U(0) in GF(p).')
    print(f'eta={eta}, eta^64={pow(eta,64,P)} != 1 (mod p)')
    print('ALGEBRAIC NO-GO within the fixed T(T-alpha) pencil: H(0)=0 '
          'demands equal constants; H(0)!=0 limits slopes to 256.')
    print('PASS: naive 63-residue truncation does not save two bits.')


if __name__ == '__main__':
    main()
