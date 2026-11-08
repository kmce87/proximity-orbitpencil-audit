#!/usr/bin/env python3
"""Run 11 (post-FINAL recheck): independent check of the constants in ChatGPT's lane B
BF64 cancellation gates (branches prize-binary-bf64-*, prize-binary-rr-*, 2026-11-07).

Their gates search for kappa_S = 0, i.e. sum_t a(U_t) = L_W(q1 + q2 + q3), which is H4 of this
ledger; N2 (run 2) bounds every kappa fibre by 2^52.709 members, so no slice result can reach 2^64.
Here: rebuild the labels and L_W from scratch in BF64 (CompPoly modulus x^64+x^4+x^3+x+1) and check
their rhs constant, their label check values, the slice count, and the xcp degree arithmetic.
Credit: the family and the labels are BitWonka's (PR #592).
"""
from math import log2

MOD_TAIL = 0x1B  # x^64 = x^4 + x^3 + x + 1


def gmul(a, b):
    p = 0
    while b:
        if b & 1:
            p ^= a
        b >>= 1
        a <<= 1
        if a >> 64:
            a = (a & (2**64 - 1)) ^ MOD_TAIL
    return p


def lin_eval(coeffs, x):
    """coeffs[i] = coefficient of X^(2^i)."""
    r = 0
    for c in coeffs:
        if c:
            r ^= gmul(c, x)
        x = gmul(x, x)
    return r


def subspace_poly(basis):
    P = [1]
    for u in basis:
        c = lin_eval(P, u)
        Q = [0] * (len(P) + 1)
        for i, a in enumerate(P):
            Q[i + 1] ^= gmul(a, a)
            Q[i] ^= gmul(c, a)
        P = Q
    assert P[-1] == 1
    return P


# Labels: L_fib over the first 64 polynomial-basis words, applied to the next 15 basis words.
L_fib = subspace_poly([1 << i for i in range(6)])
ell = [lin_eval(L_fib, 1 << (6 + i)) for i in range(15)]
assert ell[0] == 0x796ADF34D64462C2 and ell[1] == 0x3438DA15CD9684CD, "label mismatch"

# Sanity: L_fib vanishes on the fibre and is additive.
assert all(lin_eval(L_fib, v) == 0 for v in range(64))
assert lin_eval(L_fib, ell[3] ^ ell[7]) == lin_eval(L_fib, ell[3]) ^ lin_eval(L_fib, ell[7])

# W = {z = 0}: span of the first 11 label coordinates; Q = {1, 2, 4} on the z part (row 0).
L_W = subspace_poly(ell[:11])
assert len(L_W) == 12
rhs = lin_eval(L_W, ell[11]) ^ lin_eval(L_W, ell[12]) ^ lin_eval(L_W, ell[13])
assert rhs == lin_eval(L_W, ell[11] ^ ell[12] ^ ell[13])
print(f"rhs L_W(sum Q) = 0x{rhs:016x} (lane B: 0x17c6dbd8e3893ddc) match={rhs == 0x17C6DBD8E3893DDC}")
assert rhs == 0x17C6DBD8E3893DDC

# Slice size and expected cancellations for a 64-bit target.
slice_tuples = 1023 * 1022 * 1021 * 8**3
assert slice_tuples == 546540352512
print(f"slice tuples = {slice_tuples} = 2^{log2(slice_tuples):.3f}; with (aa,e0,e1): {slice_tuples * 8}")
print(f"expected kappa = 0 hits per slice if kappa were uniform: {slice_tuples / 2**64:.3e}")

# N2 bound for any kappa fibre (whole family / injective (m_0, jn_0) factor), exact integers.
members = 420 * 32 * 2047 * (1023 * 1022 * 1021) * 512 * 4
assert abs(log2(members) - 65.705) < 5e-4
fibre_bound = members // (1021 * 8)
print(f"members = 2^{log2(members):.3f}; any kappa fibre <= members/(1021*8) = 2^{log2(fibre_bound):.3f} < 2^64: {fibre_bound < 2**64}")
assert fibre_bound < 2**64

# xcp gate arithmetic (core 62 + 64 * degree against the row bound 2^20 - 1).
D, CORE, FIB, ROW_MAX = 16384, 62, 64, 2**20 - 1
assert CORE + FIB * (D - 1) == 1048574 <= ROW_MAX < CORE + FIB * D == 1048638
print("xcp arithmetic ok: 62 + 64*16383 = 1048574 <= 1048575 < 1048638 = 62 + 64*16384")
print("PASS")
