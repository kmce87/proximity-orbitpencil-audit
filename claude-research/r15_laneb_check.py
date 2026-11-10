#!/usr/bin/env python3
"""Run 15: independent replay of ChatGPT lane B's three new binary UPPER gates of 2026-11-09,
read only:
  5c5d33d (prize-binary-upper-10624-source-audit-20261109): index 917441 scores 106.24, not 106.23;
  6d7f96a (prize-binary-upper-10623-obligation-20261109): the largest 106.23 index is 917378 (+63);
  c117e0b (prize-binary-core-degree-obstruction-20261109): 63 more core points overflow the row
          degree budget (63 + 64 * 16383 = 2^20 - 1).
Their other commits since run 14 are another track (70b7ad4: binary lower 64.01 Johnson radius) or
the Koala track (aef2e79: receipt-format gate), and are not replayed.

Method: the pass test is the Solution.lean inequality 2^(-c/100) <= (a/N)^T in exact integers, and
the score is recomputed separately with 60-digit Decimal logarithms (a different route). The
degree gate is extended to every core size: in the record's shape (row = R * (Q o Y), deg Y = 64,
fibre count = deg Q + 1 + 2^11 by the gap framework, see LEDGER.md), 64 extra core points cost one
fibre, so no trade between core and fibres beats agreement 1179711 (credit: the shape is BitWonka's).
"""
from decimal import Decimal, getcontext

getcontext().prec = 60
N, T, K = 2**21, 128, 2**20            # domain, repetitions, RS dimension (row degree < K)


def passes(centibits, a):
    return 2 ** (21 * 100 * T - centibits) <= a ** (100 * T)


def score(a):                           # 128 * log2(N / a) with 60 significant digits
    return Decimal(T) * (Decimal(N) / Decimal(a)).ln() / Decimal(2).ln()


# 1. source audit: index 917441, agreement 1179711
I = 917441
a = N - I
assert a == 1179711 and I < N // 2
assert passes(10624, a) and not passes(10623, a)
s = score(a)
assert Decimal("106.23") < s <= Decimal("106.24")
print(f"index {I}: agreement {a}, score {s:.6f}; passes 106.24, fails 106.23 (lane B: same)")

# 2. 106.23 obligation: largest passing index
lo, hi = 1, N // 2                      # passes(10623, N - i) is monotone decreasing in i
while lo < hi:
    mid = (lo + hi + 1) // 2
    if passes(10623, N - mid):
        lo = mid
    else:
        hi = mid - 1
assert lo == 917378 and I - lo == 63
assert score(N - lo) <= Decimal("106.23") < score(N - lo - 1)
print(f"largest 106.23 index {lo} (agreement {N - lo}), {I - lo} positions beyond the record (lane B: 917378, 63)")

# 3. degree budget of the core extension, and the general core/fibre trade
CORE, FIB, QDEG, GAP = 63, 64, 2**14 - 1, 2**11
assert CORE + FIB * QDEG == K - 1                     # the record fills the budget exactly
assert (CORE + 63) + FIB * QDEG == K + 62             # naive +63 core: over by 63
assert (K - 1 - (CORE + 63)) // FIB == 16382          # so deg Q must drop by one
assert (QDEG + 1) + GAP == 18432                      # fibre count at deg Q = 2^14 - 1
best = 0
for c in range(0, K):                                 # every core size with row degree < K
    q = (K - 1 - c) // FIB                            # largest admissible deg Q
    if q < 0:
        break
    best = max(best, c + FIB * (q + 1 + GAP))
assert best == 1179711
trade = (CORE + 63) + FIB * (18432 - 1)
assert trade == 1179710 and 1179774 - trade == 64
print(f"degree budget: 63 + 64*16383 = 2^20 - 1; 126 core points force deg Q <= 16382, agreement {trade} "
      f"(64 short of 106.23); best over all core sizes {best} = the record")
print("PASS: all three new lane B upper gates reproduced; negative, nothing changes the FINAL")
