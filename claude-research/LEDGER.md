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

Algebra of the second coefficient a(U) (top coefficient of L_U below the leading term), all checked in
real BF64 and in the toy (`n2_kappa.cpp`, `n2_toy_replay.py`):
* a(Y + <w>) = a(Y)^2 + L_Y(w): additive in w for fixed Y. Gives universal 4-term relations, e.g.
  a(U_0(g)) + a(U_0(g+s_1)) = a(U_1(g)) + a(U_1(g+s_0)) (only when m_0 = m_1).
* For hyperplanes U of a fixed W: a(U)^2 = A(W) + c_U, c_U = L_U(w) (w in W \ U), and 1/c_U is F_2-linear in
  the functional. So a(U) = const + 1/zeta(f) with zeta linear and injective: a is injective on hyperplanes.
* Composition: C_S = kappa X^D + (next term at degree D - 2^(n-5)) + ... (real BF64: 16384, then 15360, 14848).
  So a fixed kappa would buy 2^(16-f) fixed labels at once (19/32 of the domain, score 96.27), not just one.

## Results

| id | hypothesis | outcome |
|---|---|---|
| H0 | exact model of the record | confirmed (numbers above), `binary_upper_scan.py` |
| H1 | 8 zero-sum classes of a varying codim-4 U' + one coset of a fixed codim-3 U*: |S| = 5/8 of labels (would score 86.79) | **fails**: disjointness forces the class pattern; members <= 2^57.0 at f = 0, 2^(57-3f) in general (exact Gaussian-binomial count) |
| H2 | two varying codim-2 flats + fixed codim-3 coset (5/8) | **fails** (rough): disjoint pairs ~2^62 before the fixed coset; keeping the fixed coset disjoint cuts to ~2^27 |
| H3 | 6 zero-sum W-cosets + 4 zero-sum classes of a varying 11-dim U' (5/8) | **fails** (rough): ~2^32 members |
| H4 | add one fixed label by making the degree-2^14 coefficient of C_S constant | needs a K-valued (64-bit) coincidence against 1.7 bits of slack; superseded by N2 |
| N2 | kappa_S takes few values on a sub-family of > 2^64 members of BitWonka's family | **fails, rigorous**: kappa_S = L_W(sum Q) + sum_t a(U_t) (direct locators match); kappa is injective in (m_0, jn_0), which has 1021*8 values with the rest fixed, so every kappa fibre has <= 2^52.709 members and any > 2^64 sub-family has > 2^11 kappa values. Measured: 3*10^6 random members give 3*10^6 distinct values; slice fibres on 8184^3 triples mean 1.0008, max 2; only invariance is (aa, e0, e1). ChatGPT's `prize-binary-coeff-injection-20261103` reaches a weaker bound (|Param|/8) independently. Pigeonhole version needs 2^128 members; the design has at most 2^(4 ny + 22) = 2^90 at f = 0 |

Working conclusion: within subspace/flat families, gaps above 2^(n-4) force all varying parts to
share one subspace, which caps the family far below 2^64, and fixing kappa is out of reach.

**Cheapest remaining route (found in run 2): keep 9/16 but move to f = 7.** The core is 2^f - 1, so
a = 9*2^17 + 2^f - 1. Exact integers (`n2_f7_numbers.py`): 106.23 needs a >= 1179774 (63 more points, unsafe
index <= 917378). f = 7 gives a = 1179775, score 106.23; f = 8 gives 106.21; f = 9 gives 106.17. The only obstacle
is the member count at ny = 17 - f: BitWonka's rows give 2^61.696 at f = 7 (need > 2^64, **short by 2.31 bits**).
Known enlargements of the same common-top class (top = L_W^3 X^(3*2^(n-3)) mod degree <= D):
* 35 more rows (P a linear plane, v_3 = 0, all three constants free): 2^61.918 (exact).
* Shape AAB: two flats over one half-space H plus one flat over a plane in H^c. Toy-verified common top and
  end-to-end pencil replay. Each set has 3 decompositions, so estimated count is about 2^(4 ny + 19.9), total about 2^62.2
  (estimate only). Still short by about 1.8 bits; lower-rank shapes (BBB, 5 cosets + 2 flats) add only a few percent.
Conjecture (unverified) that makes the class finite to classify: S, S' share the top down to gap 2^(n-4) iff every
Walsh coefficient of 1_S - 1_S' is divisible by 2^(n-3). Then 1_S - 1_S' = (1/8) sum c_L chi_L with sum c_L^2 <= 64,
and M(ny) = sum_rho [ny, rho]_2 N_rho, where N_rho counts members of y-rank exactly rho at ny = rho. Per-z
fibres S_z may then be rank-2k quadrics, not only flats (non-affine candidates). For the row pattern with all
characters on half-spaces, AAA is forced; other patterns are open.

## Queue (take the top item each run)

1. **N6** Enlarge the common-top class at f = 7. Falsifiable claim: the class has > 2^64 distinct members at ny = 10.
   Steps: (a) test the Walsh-divisibility conjecture by direct locators at n = 6, 7; (b) enumerate the allowed
   z-patterns of each character (w = 8*G_mu integer-valued, all z-Walsh sums = 0 mod 16, zero on full/empty z) and
   the delta patterns (all z-Walsh sums of delta odd); (c) count distinct sets exactly at small ny, fit M(ny), and
   evaluate M(10). Any member of y-rank >= 5 would likely settle it.
2. **N3** Literature pass: Dao-Kominers-Thaler-Zheng (ePrint 2026/2424, ECCC TR26-237) binary
   and additive-domain constructions; anything with a larger gap/family trade-off.
3. **N1** Exact count for H2 (two varying codim-2 flats + fixed codim-3 coset), all f. Low priority.
4. **N4** Non-affine label sets beyond the N6 class (trace or quadratic conditions at other gaps). Toy first.
5. **N5** If nothing beats 106.24 on paper by 2026-11-17: write the FINAL section and stop.

## Run log

* 2026-11-03 (interactive): H0-H4, framework, queue. Script: `binary_upper_scan.py`.
* 2026-11-03 (scheduled, run 2): N2 failed rigorously (`n2_kappa.cpp`, `n2_toy_replay.py`, `n2_f7_numbers.py`, `qrows.txt` from LabelTable.lean). Found the f = 7 route; new queue top N6.
