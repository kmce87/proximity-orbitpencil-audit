#!/usr/bin/env python3
"""Run 14: independent replay of ChatGPT lane B's two new binary UPPER gates of 2026-11-09,
read only (branch prize-binary-affine-complement-20261109, commits b724de6 01:02 UTC and
7f608d5 04:00 UTC). Their three other binary commits that day (b694ebc, 7b165e0, add80e9)
are about SubmissionBinaryLower (64.00 / 64.01), another track, and are not replayed.

1. Score boundary: 106.22 bits <=> agreement >= 1179838, i.e. unsafe index <= 917314.
2. Gold row gate: Q_4(v) = Tr(t^2 v^3) on V = span(1, t, ..., t^20) is exactly v_19 v_20,
   so it has 3 * 2^19 zeros (lane B's "prior numerical witness"), more than the
   2^20 - 1 roots a nonzero RS row codeword of degree < 2^20 can have.
   Proof: deg(t^2 v^3) <= 62 < 64 needs no reduction and Tr(a) = a_61 + a_63 for this
   modulus (r13_laneb_gold_check.py), so Q_4(v) = [t^59] v^3 = sum_{2i+j=59} v_i v_j = v_20 v_19.
   Checked here without that closed form: a quadratic form over GF(2) is fixed by its
   21 diagonal values Q(e_i) and its 210 polar values B(e_i, e_j), all recomputed with a
   trace by repeated squaring, plus random points.
3. Affine complement gate: Z(q) and Z(q + 1) partition V for every q, and 2 * 1179838 > N,
   so at most one offset per coefficient a qualifies: at most |BF64| = 2^64 pairs, density
   exactly 2^64 / 2^192 = 2^-128, which fails the strict budget (2^64 + 1 needed). This is
   the K-limit of run 4 again.
Exact integers only (log2 is printed, never compared).
"""
import random

N, T = 2**21, 128
M, TAIL, DIM = 64, 0x1B, 21          # BF64 = F_2[t]/(t^64 + t^4 + t^3 + t + 1), CompPoly modulus


# ---------- 1. score boundary (same pass test as final_check.py / Solution.lean) ----------
def passes(centibits, a):
    return 2 ** (21 * 100 * T - centibits) <= a ** (100 * T)


def min_agreement(centibits):
    lo, hi = N // 2, N
    while lo < hi:
        mid = (lo + hi) // 2
        if passes(centibits, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


a22 = min_agreement(10622)
assert a22 == 1179838 and N - a22 == 917314
assert passes(10622, a22) and not passes(10622, a22 - 1)
assert min_agreement(10623) == 1179774 and min_agreement(10624) <= 1179711
print(f"106.22 needs agreement >= {a22} (unsafe index <= {N - a22}); lane B: 1179838 / 917314")


# ---------- 2. Gold row gate ----------
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
        z = (z & ((1 << M) - 1)) ^ clmul(z >> M, TAIL)
    return z


def fmul(a, b):
    return reduce(clmul(a, b))


def trace(a):                        # repeated squaring, independent of the closed form
    s, x = 0, a
    for _ in range(M):
        s ^= x
        x = fmul(x, x)
    assert s in (0, 1)
    return s


A = 4                                # t^2 in the polynomial basis


def Q(v):
    return trace(fmul(A, fmul(fmul(v, v), v)))


e = [1 << i for i in range(DIM)]
diag = [Q(x) for x in e]
polar = {(i, j): Q(e[i] ^ e[j]) ^ diag[i] ^ diag[j] for i in range(DIM) for j in range(i + 1, DIM)}
assert not any(diag), "diagonal of Q_4 should vanish on the basis"
assert [p for p, b in polar.items() if b] == [(19, 20)], "polar form should be e19*e20 only"

rng = random.Random(20261109)
for _ in range(2000):
    v = rng.getrandbits(DIM)
    assert Q(v) == (v >> 19 & 1) & (v >> 20 & 1)

zeros = N - (N >> 2)                 # #{v : v_19 v_20 = 0}
assert zeros == 3 * 2**19 == 1572864
assert zeros > 2**20 - 1             # root bound for a nonzero codeword of degree < 2^20
print(f"Q_4 = v19*v20 on V (231 basis values + 2000 random points); zeros {zeros} = 3*2^19 "
      f"> 2^20 - 1: direct RS-row embedding impossible (lane B: same)")


# ---------- 3. affine complement gate ----------
assert 2 * a22 > N                   # at most one of Z(q), Z(q+1) can reach a22
eligible = 2**64                     # one offset per a in BF64
assert eligible * 2**128 == 2**192   # density exactly 2^-128
assert not eligible > 2**64          # strict budget needs 2^64 + 1 winners
print("affine pairs reaching 1179838 zeros: at most 2^64 = |BF64|, density exactly 2^-128, "
      "fails strict (K-limit, run 4)")
print("PASS: both new lane B upper gates reproduced; negative, nothing changes the FINAL")
