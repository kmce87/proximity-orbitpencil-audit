# Claude research ledger: official benchmark, binary upper track

Owner: Claude (scheduled job, self-managed). ChatGPT owns the OrbitPencil / rs-mca MCA line;
do not duplicate it. Time box: until **2026-11-17**. One falsifiable hypothesis per run.
Maths first (exact integers, toy fields); Lean only if a candidate beats the record on paper.
Never submit to better.codes (the user does that). Credit BitWonka (binary upper record) and
erdkocak (OrbitPencil) in anything that builds on their constructions.

## Target

Track `binary-irs-reduction-threshold-upper` (`proximity-prize/proximity-prize`, Lean 4.34.0,
ArkLib 34a834c, CompPoly 411708c). Record: **106.24 bits** (BitWonka, PR #592, 2026-10-20,
`ProximityPrize/SubmissionBinaryUpper`, unsafe index 917441 / 2^21). Lower score is better.

Profile: K = BF64, challenge field Ext3 (|F| = 2^192), domain = first 2^21 polynomial-basis
words (an F_2-subspace), k = 2^20, budget B* = 2^192 / 2^128 = **2^64** bad slopes.

## Mechanism of the record (exact)

Fibres = cosets of the first 64 words (f = 6); labels in V = F_2^11 x F_2^4 (15 dims).
Family member S (a set of labels) = 3 reserved cosets of W = {z = 0} (z in Q) plus 3 flats of
dim 12 (`F_t = {z in H_t, r.y = rho_t(z), m_t.y = nu_t(z)}`). V_S = L_W^3 X^12288 + C_S with
deg C_S <= 2^14. Slope = C_S(alpha). Agreement = 63 + 64 |S|, |S| = 2^14 + 2^11 = 18432.

* Members: 420 * 32 * 2047 * (1023*1022*1021) * 512 * 4 = 2^65.705 (slack **1.705 bits**).
* Both degree terms of C_S sit exactly at 2^14 (reserved: 2*2^11 + 3*2^12; flats: 3*2^11 +
  3*2^12 - 2^11). One extra label would score 106.23.

## Gap framework (verified in toy GF(2^16) checks)

If V_S = prod_j (common_top_j + lower_j) with deg lower_j <= deg factor_j - g_j, then
|S| <= D + min_j g_j, with D = 2^(20-f).
* varying-direction flat of dim d: gap 2^(d-1)
* m cosets of a FIXED subspace W: gap 2^dim W; if the coset sum is 0, gap 2 * 2^dim W
* 2^j classes of a VARYING subspace U' (dim u) with zero class-sum: gap 2^(u+1)
  (Frobenius: L'^(2^j) has its second term at half degree)

## Results

| id | hypothesis | outcome |
|---|---|---|
| H0 | exact model of the record | confirmed (numbers above), `binary_upper_scan.py` |
| H1 | 8 zero-sum classes of a varying codim-4 U' + one coset of a fixed codim-3 U*: |S| = 5/8 of labels (would score 86.79) | **fails**: disjointness forces the class pattern; members <= 2^57.0 at f = 0, 2^(57-3f) in general (exact Gaussian-binomial count) |
| H2 | two varying codim-2 flats + fixed codim-3 coset (5/8) | **fails** (rough): disjoint pairs ~2^62 before the fixed coset; keeping the fixed coset disjoint cuts to ~2^27 |
| H3 | 6 zero-sum W-cosets + 4 zero-sum classes of a varying 11-dim U' (5/8) | **fails** (rough): ~2^32 members |
| H4 | add one fixed label by making the degree-2^14 coefficient of C_S constant | needs a K-valued (64-bit) coincidence against 1.7 bits of slack; fails unless that coefficient is structurally confined (see N2) |

Working conclusion: within subspace/flat families, gaps above 2^(n-4) force all varying parts to
share one subspace, which caps the family far below 2^64. The record looks locally optimal for
this design space. Improvements likely need non-affine label sets.

## Queue (take the top item each run)

1. **N2** Compute, in the real BF64 label space, the degree-2^14 coefficient
   kappa_S = L_W(sum Q) + sum_t a_11(lab U_t) for random members of BitWonka's family.
   Does it take few values on any sub-family of > 2^64 members? (If yes: +1 label, 106.23.)
2. **N1** Exact count for H2 (two varying codim-2 flats + fixed codim-3 coset), all f.
3. **N3** Literature pass: Dao-Kominers-Thaler-Zheng (ePrint 2026/2424, ECCC TR26-237) binary
   and additive-domain constructions; anything with a larger gap/family trade-off.
4. **N4** Non-affine label sets: zero sets of quadratic forms / trace conditions whose
   locators have sparse structured coefficients. Toy-field experiments first.
5. **N5** If nothing beats 106.24 on paper by 2026-11-17: write the FINAL section and stop.

## Run log

* 2026-11-03 (interactive): H0-H4, framework, queue. Script: `binary_upper_scan.py`.
