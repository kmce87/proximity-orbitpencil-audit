#!/usr/bin/env python3
"""
Binary upper track (binary-irs-reduction-threshold-upper): exact model of the
current record (BitWonka, score 106.24, PR #592) and run-1 hypothesis H1.

Profile: K = BF64, challenge field Ext3 with |F| = 2^192, n = 2^21 domain
words forming an F_2-subspace, k = 2^20, budget B* = 2^192 / 2^128 = 2^64.

Pencil shape (CorePencil.lean): fibres = cosets of a 2^f-word subspace, labels
Y in a (21-f)-dim F_2-space; for a family of label sets S whose locators share
a common top R' above degree D = 2^(20-f):  V_S = R' + C_S, deg C_S <= D,
f1 + C_S(alpha) f2 agrees with a degree < 2^20 word on (2^f - 1) + 2^f |S|
points, and distinct members give distinct slopes for generic alpha.
So the score is set by max |S| subject to (#members > 2^64, deg C_S <= D).

Gap framework: if V_S = prod_j (T_j + lower_j) with common T_j and
deg lower_j <= deg factor_j - g_j, then deg C_S <= |S| - min_j g_j, hence
|S| <= D + min_j g_j.
"""
import itertools, random
from math import log2

# ---------------------------------------------------------------- record ----
def score_bits(agreement, N=2**21):
    return -128 * log2(agreement / N)

param_count = 420 * (8*2*2) * 2047 * (1023*1022*1021) * 8**3 * (2*2)
f, S_rec = 6, 3*2**11 + 3*2**12
agree_rec = (2**f - 1) + 2**f * S_rec
print("== record (BitWonka) ==")
print(f"members = {param_count} = 2^{log2(param_count):.3f}  (slack {log2(param_count)-64:.3f} bits over 2^64)")
print(f"|S| = {S_rec} = 2^14 + 2^11, agreement = {agree_rec}, score = {score_bits(agree_rec):.2f}")
print(f"one more label would give score {score_bits(agree_rec + 64):.2f}")
# both degree terms of C_S are exactly at D = 2^14:
D = 2**14
print("reserved term  (t_Q-1)*2^11 + 3*2^12 =", 2*2**11 + 3*2**12, "<= D:", 2*2**11 + 3*2**12 <= D)
print("flat term      t_Q*2^11 + 3*2^12 - 2^11 =", 3*2**11 + 3*2**12 - 2**11, "<= D:", 3*2**11 + 3*2**12 - 2**11 <= D)

# ------------------------------------------------- toy GF(2^m) gap checks ----
M_POLY, MBITS = 0x1002B, 16          # x^16 + x^5 + x^3 + x + 1
def gmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a >> MBITS: a ^= M_POLY
    return r
def is_irreducible():
    # Rabin test for degree 16: x^(2^16) = x and gcd(x^(2^8) - x, f) = 1
    def pmulmod(a, b, mod):
        r = 0
        while b:
            if b & 1: r ^= a
            b >>= 1; a <<= 1
            if a >> MBITS: a ^= mod
        return r
    x = 2; y = x
    for i in range(16):
        y = pmulmod(y, y, M_POLY)
        if i == 7: y8 = y
    return y == x and y8 != x
assert is_irreducible()

def pmul(A, B):
    R = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a:
            for j, b in enumerate(B):
                if b: R[i+j] ^= gmul(a, b)
    return R
def locator(points):
    P = [1]
    for v in points: P = pmul(P, [v, 1])
    return P
def deg(P):
    d = len(P) - 1
    while d >= 0 and P[d] == 0: d -= 1
    return d
def span(basis):
    out = {0}
    for b in basis: out |= {x ^ b for x in out}
    return out

rng = random.Random(5)
n_toy = 8                                  # toy domain: span{1,x,...,x^7}
dom = sorted(span([1 << i for i in range(n_toy)]))
def rand_subspace(dim):
    while True:
        B = rng.sample(dom[1:], dim)
        if len(span(B)) == 2**dim: return B
print("\n== toy checks in GF(2^16), domain dim 8 ==")
# (a) one flat of a varying d-dim subspace: second term at degree 2^(d-1)
for d in (3, 4, 5):
    Ub = rand_subspace(d); a = rng.choice(dom)
    L = locator(sorted({a ^ u for u in span(Ub)}))
    L2 = L[:]; L2[2**d] = 0
    print(f"flat dim {d}: deg(locator - x^{2**d}) = {deg(L2)}  (framework: {2**(d-1)})")
# (b) union of 8 cosets of a codim-4 subspace U' (u = 4): zero class-sum
u = 4
Ub = rand_subspace(u); Uset = span(Ub)
# class representatives: a complement basis
comp = []
for v in dom:
    if len(span(Ub + comp + [v])) > len(span(Ub + comp)): comp.append(v)
    if len(comp) == n_toy - u: break
classes = [0]
for c in comp: classes += [x ^ c for x in classes]
def class_union_locator(reps):
    pts = sorted({r ^ x for r in reps for x in Uset})
    return locator(pts)
nonzero = classes[1:]
zero_sum = next(Mset for Mset in itertools.combinations(nonzero, 8)
                if __import__('functools').reduce(lambda p, q: p ^ q, Mset) == 0)
H = class_union_locator(zero_sum); H2 = H[:]; H2[8*2**u] = 0
nz_sum = next(Mset for Mset in itertools.combinations(nonzero, 8)
              if __import__('functools').reduce(lambda p, q: p ^ q, Mset) != 0)
G = class_union_locator(nz_sum); G2 = G[:]; G2[8*2**u] = 0
print(f"8 classes of codim-4 U', zero sum   : deg(H - x^128) = {deg(H2)}  (framework: {6*2**u})")
print(f"8 classes of codim-4 U', nonzero sum: deg(H - x^128) = {deg(G2)}  (framework: {7*2**u})")

# ----------------------------------------------- H1 exact member count ----
def gauss(n, k):
    if k < 0 or k > n: return 0
    num = den = 1
    for i in range(k):
        num *= 2**(n - i) - 1; den *= 2**(k - i) - 1
    return num // den
def n_meet(nn, a, b, i):
    """# a-dim subspaces of F_2^nn meeting a fixed b-dim subspace in exactly i dims."""
    return gauss(b, i) * 2**((a - i) * (b - i)) * gauss(nn - b, a - i)
V4 = list(range(16))
def zero_sum_8subsets(avail):
    return sum(1 for Mset in itertools.combinations(avail, 8)
               if __import__('functools').reduce(lambda p, q: p ^ q, Mset) == 0)
# H1: S = (a* + U*) with U* fixed of codim 3, plus 8 classes of a varying codim-4 U'
# whose class-sum is zero.  |S| = 5 * 2^(n-3), i.e. 5/8 of the labels.
print("\n== H1: 8 zero-sum classes of a varying codim-4 subspace + one coset of a fixed codim-3 subspace ==")
for fib in range(0, 7):
    nn = 21 - fib; a, b = nn - 4, nn - 3
    total = 0
    # i = dim(U' ∩ U*) from the generic value a+b-nn up to a
    for i in range(max(0, a + b - nn), a + 1):
        cnt_U = n_meet(nn, a, b, i)
        delta = b - i                         # dim of the image of U* in V/U' (= F_2^4)
        if delta > 3: continue                # reserved coset would meet > 8 classes
        cosets_in_sum = 2**((a + b - i) - b)  # cosets of U* inside U* + U'
        if delta == 3:   # image P is a hyperplane of F_2^4 through 0; M = complement, forced
            per_U = (cosets_in_sum - 1) * 1
        elif delta == 2: # P a 2-flat through 0; choose 8 zero-sum classes among the other 12
            per_U = (cosets_in_sum - 1) * zero_sum_8subsets([c for c in V4 if c not in (0, 1, 2, 3)])
        else:            # delta == 1: U' inside U*, P = {a*, a*+u*} avoiding 0; 13 classes left
            per_U = (2**(nn - b) - 1) * zero_sum_8subsets([c for c in V4 if c not in (0, 2, 3)])
        total += cnt_U * per_U
    S_h1 = 5 * 2**(nn - 3); agree = (2**fib - 1) + 2**fib * S_h1
    print(f"f={fib}: members <= {total:.3e} = 2^{log2(total):.2f}  (need > 2^64)  "
          f"score if feasible {score_bits(agree):.2f}  -> {'OK' if total > 2**64 else 'FAILS'}")
