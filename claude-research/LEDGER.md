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
words (an F_2-subspace), k = 2^20, budget B* = 2^192 / 2^128 = **2^64** bad slopes (strict: 2^64 + 1 winners needed).
Exact score of the record: 106.2397. A score of 106.23 needs agreement >= 1179774, i.e. 63 more positions.

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
| N6 | the common-top class at f = 7 (ny = 10) has > 2^64 members avoiding label 0 | **fails, exact**: the whole class has M_all(10) = 14201103363987440560, and exactly 7/16 of it avoids a given label: **6212982721744505245 = 2^62.430** (short by a factor 2.969, i.e. 1.57 bits). See Theory below; `n6_*` |
| N3 | some Dao-Kominers-Thaler-Zheng construction (ePrint 2026/2424) lifts to this profile with agreement > 1179711 and > 2^64 slopes | **fails** (the PDF body was not readable, so partly a reconstruction). Third construction = our framework (PR #592 credits them for the pole pair). First needs D to fill a constant fraction of its field; here 2^-43. Second, reconstructed and verified: a K-valued slope word absorbs kappa and lifts to 19/32, but its winners lie in K, at most 2^64 against the strict threshold; escaping needs a second word, which exists only for one varying flat (at most 2^55.6 directions at 19/32, and 35/64 < 9/16 at the next size). See run 4 theory; `n3_*` |

## Theory proved in run 3 (`n6_*`, credit: the record's class is BitWonka's)

Notation: labels V = F_2^n, ell: V -> K injective and F_2-linear, P(g) = prod (X - ell(v))^g(v) for g in Z[V], I = augmentation ideal.
* **T1 (any ell).** g in I with 2^k dividing all Walsh coefficients <=> g in I^k (induction on n), and then P(g) = 1 + O(X^-(2^(k-1))). Generators are translates of 2^t x_w1...x_w(k-t); a cube gives L_H / (L_H + L_H(u)). So S, S' share the top to gap 2^(k-1) as soon as 2^k divides Walsh(1_S - 1_S'). The old conjecture's "if" direction is a theorem.
* **T2 (generic ell).** The leading coefficient c_j: I^j/I^(j+1) -> K, c(2^t x_T) = (prod over odd U in T of ell(sum U))^(2^t), has distinct leading monomials, so it is injective. Gaps are exactly powers of 2 and the "only if" holds. Checked exhaustively at n = 4 (partitions identical), on random cubes, and symbolically for n <= 6 (`n6_walsh_check.py`). A special ell could only add members through K-valued coincidences; the real labels have dim(V cap zV) = 0 for every subfield generator z (`n6_subfield_check.py`), and no two W share a top for any ell. Run 4 corrects "none is structural" at f = 0 (Krylov triple, small).
* **T3 (which classes).** Write A = 16 * (Fourier of 1_S). T1 on the dual gives A in I(V*)^4, so R = {chi: coefficient odd/16} is a word of RM(n-4, n): |R| >= 16 with equality iff R is a 4-flat. Since 9/16 forces 0 in R, the forced mass is >= 15/256 of 63/256, leaving at most 12 characters at +-1/8. Dimensions 2 and 3 are impossible (signed counts over z would be non-integers). R = W^perp is exactly the top L_W^3 X^(3*2^(n-3)). Every other R has |R| >= 24 (Kasami-Tokura weights) and budget <= 10, below the 12 that rank 4 costs in T4, so rank <= 3 is expected; rough counts stay near 2^56. Finer residues (odd/32) add forced mass. This paragraph's last two statements are estimates, not proofs.
* **T4 (the class for R = W^perp).** w_eta(z) = 8 E_y[1_{S_z} chi_eta] lies in Lambda (integer combinations of z-characters), and 8*phi lies in 8 delta_q + Lambda. There are 37 z-profile orbits (`n6_profiles.py`). Odd profiles die by parity (sum b^2 = #odd etas mod 2, while their budgets are even); the bent profile {2:6, 6:10} has all w even since 2 eps' w lies in Lambda. So all w are even, each S_z is empty, full, a hyperplane, a codim-2 flat or complement, or a two-flat selector (no rank-4 quadric fibres), at most 6 etas occur, and **y-rank <= 4**. Rank 4 occurs only for AAA (etas m_i, m_i + r) and AAB, both on the profile {0:1, 4:12, 8:3}; all other rows of the class have rank <= 3.
* **Exact counts.** M_all(ny) = sum_rho [ny, rho]_2 N_rho with N_0..N_4 = 11440, 14721280, 11988756480, 279283630080, 231211008000. N_4 = 560*2520*2^17 (AAA) + 560*3*840*2^15 (AAB). The class is closed under all translations, so exactly 7/16 avoids a fixed label. AAA alone gives 2^61.918 (= BitWonka's 420 rows + the 35 extra rows, exact match), AAA + AAB 2^62.240, everything 2^62.430. f = 6 (ny = 11): 2^66.347 (the record uses 2^65.705).
  Verification: per-profile exhaustive DFS at ny = 2, 3, 4 for all 34 even profiles (`n6_count.cpp`, input `n6_reps.txt`, logs `n6_ny*.log`, totals `n6_total.py`): the formula holds at every rank, rank 4 occurs only on the record's profile with 412876800 = N_4/560 members, and direct locators on 73 members of 22 profile/rank types in GF(2^16) show deg(V_S - top) <= D with a failing negative control (`n6_verify.py`). `n6_shapes.py` enumerates the 6-eta rank-4 shapes.
* **Next level up.** By T2, density above 9/16 needs gap 2^(n-3). At 5/8 the forced mass 7/64 of 15/64 leaves 2 characters at +-1/4, so one free functional; between 9/16 and 5/8 the same count leaves at most 3 characters, so at most two free functionals. That is about 2^(2n + c) members at most (rough), far below 2^64 for every f. This supersedes H1-H3 and N1.

**Consequence.** For generic labels and words of degree exactly |S| (no cofactor): 9/16 is the top density with > 2^64 members, f = 6 is the largest fibre level that keeps > 2^64, so a_max = 9*2^17 + 63 = 1179711. **BitWonka's 106.24 is exactly optimal inside this framework.** The label 0 restriction cannot be softened: the core needs 126 of its 127 points outside fib(S), so one label must host them.

Other relaxations checked on paper this run (not machine-checked). None helps; the first two cost at least one K-valued coincidence (64 bits) against 2.35 bits of slack at f = 6:
* a degree-2 denominator W = (Y - alpha)(Y - beta), which would allow a 127-point core at f = 6, needs C_S(alpha) = C_S(beta) (structurally: e-invariant S, which is the f = 7 class; alpha in K would force gamma in K, at most 2^64 slopes);
* one more label c by changing the word at c needs V_S(c) fixed; on AAA rows V_S(c) is injective in (m_0, jn_0) (from y^2 + c_U y = L_W_t(c')), so at f = 6 fibres have at most about 2^53 members, the same argument as N2;
* virtual cosets outside V (cofactors with additive structure) force a coarser level and lose mass.
* for a quadric, G - P = a*q has top X^(2^(n-1)) * p(B_q) with p: V* -> K injective, so for fixed a only one bilinear form shares a word (translates of one quadric).

## Theory from run 4 (`n3_*`; credit: DKTZ for the pole pair and the slope word, BitWonka for the family)

Sources read: ePrint landing page, IACR news abstract, PR #592 text. The ePrint PDF is blocked for this session (robots) and no mirror was tried, so everything about DKTZ below is a reconstruction from the abstract, checked by computation, not a quotation. Their Lean repository was not located. Their first construction was not reconstructed.
* **Second DKTZ construction, reconstructed** (`n3_single_flat.py`, exhaustive at N = 64, 128, 256). U of codim 2, M = N/4, L_U = X^M + a X^(M/2) + b X^(M/4) + .... On U\0, both X^(M-1) + a X^(M/2-1) and X^(2M-1) + (a^3+b^2) X^(M/2-1) have degree < N/16. (a,b) is injective on the (N-1)(N-2)/6 subspaces (L_D = L_Pi o L_U gives p = a^4 + d1, q = b^4 + d2 + p a^2); a alone is not, in the toy. So f1 = X^(M-1) + beta X^(2M-1), f2 = X^(M/2-1) has one F-valued winner per U, matching the abstract's count and its proper-subfield hypothesis. Agreement is M - 1.
* **K-limit.** Absorbing kappa with a K-valued word g = V_A Y^D instead of a pole leaves degree D - 2^(n-5), so 2^(16-f) fixed labels fit (19/32, score 96.27). But with K-valued f1, f2 and g far from the code, gamma outside K would make g low on the agreement set, so all winners lie in K: at most 2^64, and 2^64 + 1 are needed. A word supported on an avoided W-coset adds only a few thousand winners outside K (rough), which would still require kappa to hit nearly all of K; kappa is a sum of reciprocals of subspace elements and no proof route is visible.
* **Second word.** More winners need T' with T'|_S in K g|_S + Low|_S for all members (f1 = T + beta T', winners kappa + beta lambda). Any such T' lies in G(F) = {u : u|_S has degree <= D on S, for all S in F}. Define extras = dim G - (D+1) - 1 - #unused labels. One flat of any direction, codim c: extras = c - 1 (words Y^(2M), ...). Hyperplanes of one fixed subspace: 0, since a^3 + b^2 = d1 a + d2. 2, 3, 4 disjoint generic flats: 0. Record sub-families (1, 2, 3 flats free, r free, row fixed, all parameters) at ny = 3, 4, 5: 0. Replayed in GF(2^20) with a different algorithm, identical ranks (`n3_second_word*.py`, logs). Specialising labels can only lower the rank, so this covers generic labels at these sizes. Toy evidence, not a proof for all n. The cross-term reason: Y^(3M) mod A_1 A_2 picks up kappa (b_1+b_2) Y^(7M/4), which no fixed combination cancels.
* **One varying flat.** Density 1/2 + 3*2^-(c+2), winners at most [21,c]_2 directions: c = 2: 11/16, 2^39.4; c = 3: 19/32, 2^55.6; c = 4: 35/64 < 9/16, 2^69.7. So neither helps, even before keeping the flat off the fixed part.
* **The real domain is a Krylov space.** D = F_2[x]_{<=20}, dim(D cap xD) = 20, and a(lam U) = lam^(M/2) a(U), so a(U) + a(xU) + a((1+x)U) = 0 for every U in D_{<=19}. This is a structural K coincidence outside the Walsh class: exact in BF64; in a toy Krylov domain the direct locator has no X^(5M/2) term while random disjoint flats do. But three pairwise disjoint flats need codim(U + xU) >= 2, which leaves exactly 7 directions w F_2[x]_{<=n-4}, deg w <= 2 (exhaustive n = 7..11), so it adds a few thousand members, not 2^64 (`n3_krylov.py`). It does not reach the labels: a 13-dim part of the f = 6 labels has 6.7*10^7 distinct ratios and no repeats, against multiplicity 4095 at lam = x for D_<=12 (`n3_ratio_energy.cpp`).
* Over the real K, c_j: I^j/I^(j+1) -> K has an F_2-kernel of dimension at least C(n,j) - 64 by counting, so T2's "only if" is about generic labels. What matters is whether kernel elements are indicator differences of the right density; the pigeonhole version still needs 2^128 members (N2).

## Queue (take the top item each run)

1. **N7** Cofactor words, the only open generalisation. The label-level problem is list decoding of a word G on V by polynomials of degree <= D at agreement 9/16; T - P_S = V_S H_S with H_S nontrivial has not been excluded (run 4 shows cofactors do occur, for one flat: Y^(2M) has H_S of degree M). Toy: n = 5 (gap 2, one check: a linear functional Lambda on monic degree-14 locators of the complement; count distinct P, since evaluation-type Lambda all collapse to P = 0) then n = 6. `dual_rows` in `n3_second_word.py` gives the functionals. Falsifiable: a word with more distinct polynomials than the same-top class (1/32 of all S at n = 5).
2. **N8** Non-generic Z, narrowed by run 4: scaling works at f = 0 but is too small, and the sampled f = 6 labels show no multiplicative structure. Remaining: other fibre subspaces Z. Expected to fail: about 98 bits of Z freedom against 50 bits per coincidence. Low priority.
3. **N5** If nothing beats 106.24 on paper by 2026-11-17: write the FINAL section and stop.

Not blocking: if the user attaches the DKTZ PDF, compare the second construction with the reconstruction and read the first construction's mechanism (49.4% at rate 1/4 on a 2^27 domain, probability above 2^-30).

## Run log

* 2026-11-03 (interactive): H0-H4, framework, queue. Script: `binary_upper_scan.py`.
* 2026-11-03 (scheduled, run 2): N2 failed rigorously (`n2_kappa.cpp`, `n2_toy_replay.py`, `n2_f7_numbers.py`, `qrows.txt` from LabelTable.lean). Found the f = 7 route; new queue top N6.
* 2026-11-04 (scheduled, run 3): N6 failed exactly (2^62.430 < 2^64 at f = 7). Walsh conjecture proved (T1, T2); class classified (T3, T4); framework optimality of 106.24. Scripts `n6_*`; removed the f = 7 route from the queue. New top N3.
* 2026-11-04 (scheduled, run 4): N3 failed. Second DKTZ construction reconstructed from the abstract and verified; K-limit; no second word beyond one flat (two independent replays); Krylov triple found, too small. PDF body not readable. Scripts `n3_*`. New top N7.
