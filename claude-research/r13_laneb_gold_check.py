#!/usr/bin/env python3
"""Run 13: independent replay of ChatGPT lane B's Gold-form gates (branch
prize-binary-gold-rank-20261108, 2026-11-08 18:09..22:02 UTC), read only.

Lane B studies Q_a(v) = Tr(a v^3) on the protected domain V = span(1, t, ..., t^20)
inside BF64 = F_2[t]/(t^64 + t^4 + t^3 + t + 1) (CompPoly modulus, as in r11_laneb_check.py).
Polar form B_a(u, v) = Tr(a (u^2 v + u v^2)).

Lane B computes the trace by repeated squaring. Here the trace comes from Newton's
identities instead: P_k = Tr(t^k) is the linear recurring sequence of the modulus, so
Tr(a) = sum_m a_m P_m. A direct squaring trace with separate field arithmetic is only
used to cross-check P on random elements. No numbers are copied from lane B except the
claims being tested. Exact GF(2) linear algebra; no floating point.
"""
import random

M = 64
TAIL = 0x1B                      # t^64 = t^4 + t^3 + t + 1
DIM = 21                         # V = span(t^0..t^20), N = 2^21
N = 1 << DIM

# ---------- field arithmetic (carry-less multiply, then reduce) ----------
def clmul(a, b):
    z = 0
    while b:
        if b & 1:
            z ^= a
        b >>= 1
        a <<= 1
    return z

def reduce(z):
    while z >> M:
        hi = z >> M
        z = (z & ((1 << M) - 1)) ^ clmul(hi, TAIL)
    return z

def fmul(a, b):
    return reduce(clmul(a, b))

def trace_squaring(a):
    s, x = 0, a
    for _ in range(M):
        s ^= x
        x = fmul(x, x)
    assert s in (0, 1)
    return s

# ---------- trace sequence from Newton's identities ----------
# p(x) = x^64 + sum c_i x^i; in characteristic 2, e_j = c_(64-j).
coef = {4: 1, 3: 1, 1: 1, 0: 1}
e = [0] * (M + 1)
for i, c in coef.items():
    e[M - i] = c
KMAX = 2 * M + 3 * DIM + 8
P = [0] * (KMAX + 1)
P[0] = M % 2                     # Tr(1) = 64 = 0
for k in range(1, KMAX + 1):
    s = 0
    for j in range(1, min(k - 1, M) + 1):
        s ^= e[j] & P[k - j]
    if k <= M:
        s ^= (k & 1) & e[k]
    P[k] = s
# closed form for this modulus: Tr(a) = a_61 + a_63
assert [k for k in range(M) if P[k]] == [61, 63]

def trace_seq(a):
    return bin(a & sum(P[m] << m for m in range(M))).count("1") & 1

rng = random.Random(20261109)
for _ in range(300):
    a = rng.getrandbits(M)
    assert trace_seq(a) == trace_squaring(a)

# ---------- polar map a -> B_a on V (210 coordinates) ----------
pairs = [(i, j) for i in range(DIM) for j in range(i + 1, DIM)]

def polar_vec_monomial(m):
    """B_(t^m)(e_i, e_j) = P[m+2i+j] + P[m+i+2j], packed over the 210 pairs."""
    v = 0
    for k, (i, j) in enumerate(pairs):
        if P[m + 2 * i + j] ^ P[m + i + 2 * j]:
            v |= 1 << k
    return v

cols = [polar_vec_monomial(m) for m in range(M)]

def polar_vec(a):
    v = 0
    for m in range(M):
        if a >> m & 1:
            v ^= cols[m]
    return v

def rank_and_kernel(vectors):
    piv, ker = {}, []
    for idx, vec in enumerate(vectors):
        v, comb = vec, 1 << idx
        while v:
            b = v.bit_length() - 1
            if b not in piv:
                piv[b] = (v, comb)
                break
            pv, pc = piv[b]
            v ^= pv
            comb ^= pc
        if not v:
            ker.append(comb)
    return len(piv), ker

rank, ker = rank_and_kernel(cols)
print("polar map rank", rank, "kernel dimension", len(ker), "(lane B: 57 and 7)")
assert (rank, len(ker)) == (57, 7)

# direct check of the polar form with field arithmetic on random pairs in V
def Q(a, v):
    return trace_squaring(fmul(a, fmul(fmul(v, v), v)))

for a in ker:
    for _ in range(40):
        u, w = rng.getrandbits(DIM), rng.getrandbits(DIM)
        assert Q(a, u ^ w) == Q(a, u) ^ Q(a, w)        # B_a = 0: Q_a additive on V

# ---------- linear restriction on the kernel ----------
def lin(a):
    return sum(trace_seq(fmul(a, 1 << (3 * i))) << i for i in range(DIM))

lin_vecs = [lin(a) for a in ker]
lrank, lker = rank_and_kernel(lin_vecs)
print("linear restriction rank", lrank, "nullity", len(lker), "(lane B: 3 and 4)")
assert (lrank, len(lker)) == (3, 4)
zero_forms = []
for mask in range(1 << len(ker)):
    a = 0
    for i in range(len(ker)):
        if mask >> i & 1:
            a ^= ker[i]
    if lin(a) == 0:
        zero_forms.append(a)
assert len(zero_forms) == 16
for a in zero_forms:
    for _ in range(40):
        assert Q(a, rng.getrandbits(DIM)) == 0          # Q_a identically 0 on V
# Why a = 1 is one of them: deg(v^3) <= 60 < 61, so v^3 is unreduced and Tr = bits 61, 63 = 0.
assert 1 in zero_forms
print("Gold forms identically zero on V:", len(zero_forms), "(lane B: 16)")

# ---------- rank histogram on coefficients of weight 1 and 2 ----------
def alt_rank(a):
    rows = [0] * DIM
    v = polar_vec(a)
    for k, (i, j) in enumerate(pairs):
        if v >> k & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    r, _ = rank_and_kernel(rows)
    return r

hist = {}
cands = [1 << i for i in range(M)] + [(1 << i) ^ (1 << j) for i in range(M) for j in range(i + 1, M)]
for a in cands:
    r = alt_rank(a)
    hist[r] = hist.get(r, 0) + 1
hist = dict(sorted(hist.items()))
print("polar rank histogram over", len(cands), "coefficients:", hist)
assert hist == {0: 3, 2: 26, 4: 58, 6: 84, 8: 111, 10: 138, 12: 188, 14: 452, 16: 551, 18: 337, 20: 132}

# ---------- zero counts of affine forms from the kernel ----------
# Additive Q_a with linear part l: Q_a + bit has N/2 zeros unless l = 0 (then N or 0).
counts = {0: 0, N // 2: 0, N: 0}
for mask in range(1 << len(ker)):
    a = 0
    for i in range(len(ker)):
        if mask >> i & 1:
            a ^= ker[i]
    for bit in (0, 1):
        z = (N if bit == 0 else 0) if lin(a) == 0 else N // 2
        counts[z] += 1
assert counts == {0: 16, N // 2: 224, N: 16}
print("affine (a, bit) zero counts:", counts, "(lane B: same)")

# ---------- link to the ledger ----------
# A quadratic form of polar rank 2s with zero radical part has 2^(n-1) +- 2^(n-1-s) zeros,
# so zero density > 9/16 needs s <= 2 (5/8 at rank 4, 3/4 at rank 2). Coefficient-only
# families give at most |BF64| = 2^64 slopes against 2^64 + 1 needed: run 4's K-limit.
assert N // 2 + N // 8 == 5 * N // 8 and N // 2 + N // 16 == 9 * N // 16
assert 2**64 * 2**128 == 2**192         # density exactly 2^-128, not strictly above
SCORE_10623_AGREEMENT = 1179774          # = N - 917378 (run 10, final_check.py)
assert N - 917378 == SCORE_10623_AGREEMENT and N // 2 < SCORE_10623_AGREEMENT < N
print("PASS: lane B Gold gates reproduced independently; all negative, consistent with N3/N7 and the K-limit")
