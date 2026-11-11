#!/usr/bin/env python3
"""Run 17: independent replay of ChatGPT lane B's two binary branches of 2026-11-10, read only:
  61bdc80 (prize-binary-reserved-coset-xor-20261110): over 420 reserved configurations in F_2^4 the XOR
          of the three reserved z-labels is the omitted label, never 0 (each of the 15 labels 28 times);
  4b399f5 (prize-binary-affine-constant-fibre-20261110): GF(2) toy, the 8 affine constants (aa, e0, e1)
          leave the degree-16 coefficient unchanged.
Different routes from lane B: (A) the configurations are rebuilt as the 3-subsets of F_2^4 \\ 0 with
nonzero XOR (C(15,3) - 35) and compared with the record's own 420 Q rows (qrows.txt, read from
BitWonka's LabelTable.lean in run 2); (B) GF(2)[x] as Python ints, exhaustive over every monic quadratic
L and every non-constant part of the three quartics, with the degree bound that makes the invariance
structural and a failing control one degree lower. Lane B's toy is the record's shape at ny = 1:
deg L_W = 2^ny, flats of degree 2^(ny+1), |S| = 9 * 2^ny = 18, D = 8 * 2^ny = 16, and constants reach
only degree 7 * 2^ny = 14. The real-field version (BF64, f = 6, ny = 11) is r17_laneb_real.cpp.
"""
from collections import Counter
from itertools import combinations, product

# ---- A: reserved-coset XOR -------------------------------------------------------------
NZ = range(1, 16)
x3 = lambda q: q[0] ^ q[1] ^ q[2]
allq = list(combinations(NZ, 3))
subs = {frozenset(q) for q in allq if x3(q)}
assert len(allq) == 455 and len(subs) == 420          # 35 triples {a, b, a^b} have XOR 0

planes = {frozenset((0, a, b, a ^ b)) for a, b in combinations(NZ, 2)}
assert len(planes) == 35
configs = []                                          # lane B's (H, A, omitted) construction
for H in planes:
    for A in {frozenset(x ^ h for h in H) for x in range(16)}:
        if 0 not in A:
            configs += [A - {m} for m in A]
assert len(configs) == 420 and set(configs) == subs   # config -> Q is a bijection

rows = [tuple(map(int, l.split())) for l in open("qrows.txt") if l.strip()]
Q = [frozenset(r[:3]) for r in rows]
assert len(rows) == 420 and len(set(Q)) == 420 and set(Q) == subs
om = Counter(x3(r[:3]) for r in rows)
assert sorted(om) == list(NZ) and set(om.values()) == {28}
for r in rows:                                        # omitted label completes an affine plane off 0
    A = set(r[:3]) | {x3(r[:3])}
    assert len(A) == 4 and 0 not in A
print("A: the record's 420 Q rows = all 3-subsets of F_2^4 \\ 0 with nonzero XOR = lane B's 420 "
      "configurations; XOR = omitted label, never 0, each of 15 labels 28 times")

# ---- B: affine constants ---------------------------------------------------------------
def mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r

def coef(p, d):
    return (p >> d) & 1

G = mul(mul(7, 7), 7)                                 # lane B's L_W = 1 + x + x^2, cubed
lane = {coef(mul(G, mul(mul(aa | 0b10010, e0 | 0b10100), e1 | 0b10110)), 16)
        for aa, e0, e1 in product((0, 1), repeat=3)}
assert len(lane) == 1
print(f"B: lane B's toy reproduced, coefficient of x^16 = {lane.pop()} for all 8 constants")

inv_hi, moved14, total = True, 0, 0
for L in (0b100, 0b101, 0b110, 0b111):                # every monic quadratic
    G = mul(mul(L, L), L)
    for parts in product(range(8), repeat=3):         # x^4 + a3 x^3 + a2 x^2 + a1 x
        quart = [0b10000 | (p << 1) for p in parts]
        prods = [mul(G, mul(mul(quart[0] | c0, quart[1] | c1), quart[2] | c2))
                 for c0, c1, c2 in product((0, 1), repeat=3)]
        total += 1
        if len({p >> 15 for p in prods}) != 1:        # every degree >= 15 = 6 + 8 + 1
            inv_hi = False
        if len({coef(p, 14) for p in prods}) > 1:     # control: degree 14 can move
            moved14 += 1
assert inv_hi and moved14 > 0
print(f"B: exhaustive over {total} (L, quartic) choices: every coefficient of degree >= 15 is "
      f"invariant under the 8 constants; degree 14 moves in {moved14} of them (control fails as it must)")
print("PASS: both lane B gates reproduced; neutral for the record (see r17_laneb_real.cpp for BF64)")
