#!/usr/bin/env python3
"""Exact score thresholds and the family count of BitWonka's design at each fibre level f."""
from math import log2
N = 2**21
def centibits(a):
    """Smallest c with 2^(-c/100) <= (a/N)^128, i.e. N^12800 <= 2^c * a^12800 (exact integers)."""
    lhs, ap = N**12800, a**12800
    c = 0
    lo, hi = 0, 40000
    while lo < hi:
        mid = (lo + hi) // 2
        if lhs <= (ap << mid): hi = mid
        else: lo = mid + 1
    return lo
rec = 63 + 64 * 18432
print("record a =", rec, "unsafe index =", N - rec, "centibits =", centibits(rec))
lo, hi = rec, rec + 1000
while lo < hi:
    mid = (lo + hi) // 2
    if centibits(mid) <= centibits(rec) - 1: hi = mid
    else: lo = mid + 1
print("smallest a with centibits <= record - 1:", lo, "gain needed:", lo - rec)
for f in range(4, 10):
    ny = 17 - f
    S = 9 * 2**(ny + 4 - 4)
    a = (2**f - 1) + 2**f * S
    M = 420 * 32 * (2**ny - 1) * (2**(ny-1) - 1) * (2**(ny-1) - 2) * (2**(ny-1) - 3) * 8**3 * 4
    Mx = M + 35 * 32 * (2**ny - 1) * (2**(ny-1) - 1) * (2**(ny-1) - 2) * (2**(ny-1) - 3) * 8**3 * 8
    print(f"f={f}: ny={ny} |S|={S} a={a} centibits={centibits(a)} members(BitWonka rows)=2^{log2(M):.3f}  +35 linear-plane rows=2^{log2(Mx):.3f}  need > 2^64")
# Fixed-kappa route: one K-valued coincidence buys 2^(16-f) labels, i.e. a = 19/32 N + 2^f - 1.
for f in (0, 6):
    ny = 17 - f
    a = (2**f - 1) + 2**f * (9 * 2**ny + 2**(16 - f))
    M = 420 * 32 * (2**ny - 1) * (2**(ny-1) - 1) * (2**(ny-1) - 2) * (2**(ny-1) - 3) * 8**3 * 4
    print(f"fixed kappa at f={f}: a={a} centibits={centibits(a)}; family 2^{log2(M):.1f}, largest kappa fibre heuristically 2^{log2(M)-64:.1f}, need > 2^64")
# Rigorous fibre bound at f = 6: kappa is injective in (m_0, jn_0), which has 1021 * 8 values given the rest.
Mrec = 420 * 32 * 2047 * (1023 * 1022 * 1021) * 8**3 * 4
print(f"rigorous max kappa fibre at f=6: 2^{log2(Mrec / (1021 * 8)):.3f} < 2^64")
