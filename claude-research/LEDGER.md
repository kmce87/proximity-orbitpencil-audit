# Claude research ledger: official benchmark, binary upper track

Owner: Claude (scheduled job, self-managed). ChatGPT owns the OrbitPencil / rs-mca MCA line;
do not duplicate it. Time box: until **2026-11-17**. One falsifiable hypothesis per run.
**Finished 2026-11-07 (run 9): see FINAL below.**
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

## FINAL (run 9, 2026-11-07): finished, nothing beats 106.24

**Result.** No construction beats BitWonka's record on paper, so no Lean candidate and no research/ branch
were made. The record (agreement 1179711 = 9N/16 + 63, 2^65.705 members, score 106.2397) is optimal in
every framework this job analysed; 106.23 needs agreement 1179774 with more than 2^64 winners. Headline
numbers rechecked with exact integers in run 9 (`final_check.py`, `final_check.log`).

**What was tried** (details in Results and Theory):
* Higher density (H1-H3, N9, N10): every class of mass 5N/8 stays below 2^64 members above 9N/16 at
  n = 21: at most 2^63.125 (run 6), 2^63.595 for every class with phi <= 2 and 2^61.58 unless flat-like
  (run 8). The true size is about M_C/2 = 2^60.415.
* One more label on the record family (H4, N2): kappa is injective in (m_0, jn_0), so every kappa fibre
  has at most 2^52.709 members.
* Coarser fibres (N6): the f = 7 class has exactly 2^63.623 members, 2^62.430 avoiding a label (short by 2.969).
* DKTZ constructions (N3): the K-line (slope word) route lifts to 19/32 (score 96.27), but its winners lie
  in BF64: at most 2^64, and the target is strictly more. A second word exists only for one varying flat.
* Cofactors (N7): the shortened quadric family beats 9N/16 but has M_C(21)/2 = 2^60.415 members, short by exactly 12.
* Special labels (N8): tops are additive in the residue word (map Phi); merges are real at n = 6
  (Krylov labels), none useful in any domain scanned at the real size.

**Proof-level statement.** For generic labels (T2), no family of common-top words (T1-T4), real-root
cofactors (run 6) or signed classes with phi <= 2 (run 8) has more than 2^64 members above agreement
1179711. So 106.24 is optimal in that framework.

**Open gaps** (none is expected to give a record):
1. classes with a point of multiplicity >= 3 (run 8; 2% of the largest signed family in the n = 9 census);
2. the real labels at d = 21: r <= 8 sampled, r >= 9 by information set decoding only (run 7);
3. non-split cofactors of degree >= g: beyond the Johnson bound, open for RS codes in general;
4. the K-line route needs kappa_S to hit BF64 up to a few thousand values, and a proof of it; kappa is a
   sum of three reciprocals over 17-dim subspaces, and Weil-type bounds need dimension about 49.

**Official record, rechecked (runs 9-15).** proximity-prize/proximity-prize main is still eb82d3b
(2026-10-29): SubmissionBinaryUpper score.txt 10624, unsafe-index.txt 917441 (BitWonka). 9 of the 584
submission branches touch that folder, the latest on 2026-10-23 (also 10624); in run 11 (2026-11-08) none of
the 600 branch heads had a commit after 2026-10-29 or a binary upper score below 10624. Since run 12 only the
GitHub search API is used (add_repo is not offered, so the official repo is not attached or cloned). Run 15
(2026-11-10 00:34 UTC): newest PR still #611 (validation bot, 2026-10-29; no PR updated later), newest commit
still eb82d3b (commit search on six terms), and code search gives blob ids 5c74e1d865 (score.txt) and
6be1d72bcc (unsafe-index.txt), exactly `git hash-object` of "10624\n" and "917441\n". Submissions moved off the
repo: #610 points the verifier client at autoresearch.zksecurity.xyz (an authenticated service, not read). Live
board: with the user's approval (run 10) proximityprize.org was read; it shows no standings and names
better.codes as the live scored companion, which the fetch tool blocks outright (site blocked, so approval
does not help; do not retry or work around it). Web search finds nothing newer than PR #592 (titled
"claimed score: 106.25"; validated score.txt 10624); run 15's only news hit with bit counts is a 2026-08-22
item on koalaIRS12 (63.99 / 116.13), another profile. The user checks better.codes before quoting 106.24.

**ChatGPT lane B (read only).** All its binary upper branches up to 2026-11-09 17:03 UTC are negative gates
consistent with this ledger. Runs 9-11 (branches of 2026-11-03..07): coefficient injection, fixed Q, 420-row
XOR, core extension, leading coefficient, affine offsets, 2^15-class coefficient pigeonhole (too weak), 106.23
degree necessity, fibre trade (1179710, 64 short), fixed H-triple capacity (105 triples x 4 rows), score
boundary (largest 106.23 index 917378 = agreement 1179774), 64-point core (one degree over the code), and
five searches for kappa_S = 0 on slices of 2^38.99 tuples with 0 hits (N2 caps every kappa fibre at 2^52.709,
so no slice can matter; `r11_laneb_check.py` rebuilds their labels and rhs 0x17c6dbd8e3893ddc, 0 hits). Pivot
note (`prize-research-pivot-20261108`): binary upper is its priority 3 (Gold-moment / quadratic-rank counts on
the sparse domain); it cites DKTZ as ECCC TR26-237: decision-tree height 3 gives 9/16, height 4 is worse, and
the Gold theorem assumes a dense domain (here a 2^-43 fraction), as in N3. Run 13
(`prize-binary-gold-rank-20261108`): Q_a(v) = Tr(a v^3) on V has polar rank 57 (kernel 7), 16 forms vanish on
V, a coefficient-only family has at most 2^64 slopes, affine kernel forms have 0, N/2 or N zeros
(`r13_laneb_gold_check.py`, independent trace Tr(a) = a_61 + a_63). Run 14
(`prize-binary-affine-complement-20261109`): Q_4 = Tr(t^2 v^3) is exactly v_19 v_20 on V, 3*2^19 zeros, too
many for a nonzero RS row; at 106.22 (index 917314, agreement 1179838) Z(q) and Z(q+1) partition V, so at
most 2^64 pairs, density exactly 2^-128, the K-limit (`r14_laneb_check.py`). Run 15 (three gates,
2026-11-09 15:04-17:03 UTC): 5c5d33d, index 917441 passes 106.24 and fails 106.23; 6d7f96a, the largest
106.23 index is 917378 (+63); c117e0b, 63 more core points overflow the row degree (63 + 64*16383 = 2^20 - 1,
so deg Q would have to drop to 16382). `r15_laneb_check.py` reproduces all three (the score also with 60-digit
logarithms) and extends the last to every core size: in the record's shape 64 core points cost one fibre, so
the best agreement over all core sizes is exactly 1179711.
Other-track commits (binary lower b694ebc, 7b165e0, add80e9, 70b7ad4; Koala aef2e79) are not replayed. Zero
counts of Gold forms are not IRS agreements (lane B says so too). Remaining overlap with this ledger: N7, N9,
N10 (quadric and mean-1/2 classes) and N8 (special labels, open gap 2). The note also says binary acceptance
by the scoring service is unconfirmed (not checked here).

**Recommendation.** Stop this track and do not build a Lean candidate from these ideas. Follow up only if
something changes: (a) with the DKTZ PDF, compare its first construction (49.4% at rate 1/4 on a 2^27
domain) with run 4 (lane B cites a copy as ECCC TR26-237; not fetched here, because the ePrint PDF was
blocked for this job and other copies are not tried, so the user would attach it); (b) under a budget near
2^60 the shortened quadric family beats 9/16; (c) a character-sum bound for reciprocals over small subspaces
would reopen the K-line route (score 96.27; it needs about 2^64 distinct kappa values plus one winner outside
BF64).

**Scheduler.** Run 9 sent the one finishing notification. Disabling the task from inside a run is refused
by the permission classifier (runs 9-15; reason "Cowork Scheduled Task Delete"), so the user has to
switch off "Binary-upper benchmark research" (trig_01JA8ECs6Hg1pJfYLhYBdfr5, cron 34 */12 UTC, still
enabled at run 15, next 2026-11-10 12:34 UTC; it does not stop by itself after 2026-11-17). Later runs:
recheck the official record and any new lane B binary branches, update the "runs 10+" line of the run log
in place (no new line per run), and notify only if the record changes or, once, on the first run after
2026-11-17 if the task is still enabled.

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
| N7 | a cofactor word (T - P_S = V_S H_S, H_S nontrivial) has more polynomials than the same-top class | **true above 9/16, still no record.** One check at 9/16 (n = 5, |S| = 18): no, same-top is the maximum, rigorous (Theorem A below); n = 4 sampling agrees (504, runner-up 190). Above 9/16: yes. New shortened quadric family T = X^(N/2) V_B: at n = 5 quadrics alone give 2324 polynomials at agreement >= 19 against 1323 for the largest same-top class (exhaustive real-root maximum at n = 5: 15736, a small-n effect). But it has at most M_C(n)/2 members above 9N/16, and at f = 0 M_C(21)/2 = 2^60.415, **short of 2^64 by a factor of 12.00**. See Theory run 5; `n7_*` |
| N9 | a class of mass 5N/8 at n = 21 has > 2^64 members of agreement >= 1179712 | **fails, proof-level.** All shapes classified (at most 10 characters). Boolean h: at most M_C/2 (complement pairs). Non-Boolean h need E' = {h = -1} inside B, and a tuple count bounds them: every B has at most 10054856440406858498 = 2^63.125 members, below 2^64. The true size is about M_C/2 = 2^60.415: non-Boolean members grow like 2^(2n) on flat B and vanish from n = 8 on random B. Exact census to n = 10, checked by brute force at n = 5, 6 and against the exhaustive n = 5 class sizes. Classes with only a signed representative are not covered rigorously. See Theory run 6; `n9_*` |
| N8 | a 7-dim Z whose labels L_Z(D) carry a relation big enough for the factor 2.97 at f = 7 | **fails** (rigorous at n = 6 for every Z in the toy domains; sampling and a count at the real size). Large relations exist only at f = 0 (t = n-1) and f = 1 (t about n/2); from f = 2 on t <= 3 and the class is exactly the T4 count (n = 6 exhaustive over 2^60 subsets, 12032931760 for random labels and for the top-relation Z). New exact tool: tops are additive in the residue word (Phi, run 7), and extras need a low-weight word in ker Phi. Only structural ones: full chains lam mu^i (f' = 0, where a merge really adds 77% at n = 6) and one real family at r = 8 (Y = 0x6c P_f, weight 58, useless). See Theory run 7; `n8_*` |
| N10 | a class with only signed representatives has more than M_C/2 members above 9N/16 at n >= 8 (the gap of run 6) | **fails; gap closed for phi <= 2 (proof-level).** New unbiased evaluator of one class (`n10_class.cpp`), matches the n = 5 sizes 15736, 11223, 9056, 6811 and the n = 6 brute force by type. No class without a Boolean rep reaches M_C/2 at n = 8, 9: |P| = 1, 2, 4, 8 random 0.405, 0.180, 0.035, 0.0009 (n = 9), two signed points in two alternative cosets 0.412, hill climbing at n = 8 tops at 0.659. Theorem: at n = 21 every class has at most 2^63.595 members above 9N/16 with phi <= 2, and 2^61.58 unless strictly flat-like. See Theory run 8; `n10_*` |

## Theory proved in run 3 (`n6_*`, credit: the record's class is BitWonka's)

Notation: labels V = F_2^n, ell: V -> K injective and F_2-linear, P(g) = prod (X - ell(v))^g(v) for g in Z[V], I = augmentation ideal.
* **T1 (any ell).** g in I with 2^k dividing all Walsh coefficients <=> g in I^k (induction on n), and then P(g) = 1 + O(X^-(2^(k-1))). Generators are translates of 2^t x_w1...x_w(k-t); a cube gives L_H / (L_H + L_H(u)). So S, S' share the top to gap 2^(k-1) as soon as 2^k divides Walsh(1_S - 1_S'). The old conjecture's "if" direction is a theorem.
* **T2 (generic ell).** The leading coefficient c_j: I^j/I^(j+1) -> K, c(2^t x_T) = (prod over odd U in T of ell(sum U))^(2^t), has distinct leading monomials, so it is injective. Gaps are exactly powers of 2 and the "only if" holds. Checked exhaustively at n = 4 (partitions identical), on random cubes, and symbolically for n <= 6 (`n6_walsh_check.py`). A special ell could only add members through K-valued coincidences; the real labels have dim(V cap zV) = 0 for every subfield generator z (`n6_subfield_check.py`), and no two W share a top for any ell. Run 4 corrects "none is structural" at f = 0 (Krylov triple, small).
* **T3 (which classes).** Write A = 16 * (Fourier of 1_S). T1 on the dual gives A in I(V*)^4, so R = {chi: coefficient odd/16} is a word of RM(n-4, n): |R| >= 16 with equality iff R is a 4-flat. Since 9/16 forces 0 in R, the forced mass is >= 15/256 of 63/256, leaving at most 12 characters at +-1/8. Dimensions 2 and 3 are impossible (signed counts over z would be non-integers). R = W^perp is exactly the top L_W^3 X^(3*2^(n-3)). Every other R has |R| >= 24 (Kasami-Tokura weights) and budget <= 10, below the 12 that rank 4 costs in T4, so rank <= 3 is expected; rough counts stay near 2^56. Finer residues (odd/32) add forced mass. This paragraph's last two statements are estimates, not proofs.
* **T4 (the class for R = W^perp).** w_eta(z) = 8 E_y[1_{S_z} chi_eta] lies in Lambda (integer combinations of z-characters), and 8*phi lies in 8 delta_q + Lambda. There are 37 z-profile orbits (`n6_profiles.py`). Odd profiles die by parity (sum b^2 = #odd etas mod 2, while their budgets are even); the bent profile {2:6, 6:10} has all w even since 2 eps' w lies in Lambda. So all w are even, each S_z is empty, full, a hyperplane, a codim-2 flat or complement, or a two-flat selector (no rank-4 quadric fibres), at most 6 etas occur, and **y-rank <= 4**. Rank 4 occurs only for AAA (etas m_i, m_i + r) and AAB, both on the profile {0:1, 4:12, 8:3}; all other rows of the class have rank <= 3.
* **Exact counts.** M_all(ny) = sum_rho [ny, rho]_2 N_rho with N_0..N_4 = 11440, 14721280, 11988756480, 279283630080, 231211008000. N_4 = 560*2520*2^17 (AAA) + 560*3*840*2^15 (AAB). The class is closed under all translations, so exactly 7/16 avoids a fixed label. AAA alone gives 2^61.918 (= BitWonka's 420 rows + the 35 extra rows, exact match), AAA + AAB 2^62.240, everything 2^62.430. f = 6 (ny = 11): 2^66.347 (the record uses 2^65.705).
  Verification: per-profile exhaustive DFS at ny = 2, 3, 4 for all 34 even profiles (`n6_count.cpp`, input `n6_reps.txt`, logs `n6_ny*.log`, totals `n6_total.py`): the formula holds at every rank, rank 4 occurs only on the record's profile with 412876800 = N_4/560 members, and direct locators on 73 members of 22 profile/rank types in GF(2^16) show deg(V_S - top) <= D with a failing negative control (`n6_verify.py`). `n6_shapes.py` enumerates the 6-eta rank-4 shapes.
* **Next level up.** By T2, density above 9/16 needs gap 2^(n-3). At 5/8 the forced mass 7/64 of 15/64 leaves 2 characters at +-1/4, so one free functional; between 9/16 and 5/8 the same count leaves at most 3 characters, so at most two free functionals. That is about 2^(2n + c) members at most (rough), far below 2^64 for every f. This supersedes H1-H3 and N1.

**Consequence (no cofactor only; run 6 extends it to real-root cofactors).** For generic labels and words of degree exactly |S| (no cofactor): 9/16 is the top density with > 2^64 members, f = 6 is the largest fibre level that keeps > 2^64, so a_max = 9*2^17 + 63 = 1179711. **BitWonka's 106.24 is exactly optimal inside this framework.** The label 0 restriction cannot be softened: the core needs 126 of its 127 points outside fib(S), so one label must host them.

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
* Over the real K, T2's "only if" is about generic labels; the exact statement is the map Phi of run 7. The pigeonhole version still needs 2^128 members (N2).

## Theory from run 5 (`n7_*`; credit: quadric flats and the reserved set idea come from BitWonka's family and DKTZ's pole pair)

Notation: N = 2^n labels, D = N/2. A word T has P in its list on S iff T - P = V_S H, deg P <= D. The number of winners on the pole line equals the list size of T (Q' = T - V, gamma = V(alpha)), so the target is a list > 2^64 at agreement >= 1179712.
* **Dual form.** S <-> complement C, word <-> functional Lambda on polys of degree <= N/2 - 2; member iff Lambda(X^i V_C) = 0 for i <= g-2 (g = |S| - D). Distinct polynomials <-> distinct error supports. Kernel of the Hankel system: V_C = A Q1 + B Q2, deg Q1 + deg Q2 = N/2, and deg B is the cofactor degree. Any m < (N/2 - 1)/(g-1) members have a common word for free, so about 8 at 9/16.
* **Theorem A (n = 5, g = 2, rigorous for labels with m* <= 3).** Lemma (any point set, any field): a nonzero functional on polys of degree <= k vanishes on at most C(N-1, k-1) of the locators of k-subsets (induction on the point: either Lambda = eval_v or Pascal), equality for eval_v. Above a 12-set R the members are pairs {a,b} with l2 + (a+b) l1 + ab l0 = 0: a translation matching (<= 10 pairs) if l0 = Lambda(L_R) = 0, otherwise a Moebius involution with at most m* pairs; every polynomial with error support >= 2 is counted 91 times. If Lambda vanishes on all polys of degree <= 12 it is the same-top functional. Otherwise the list is <= (10*12/32 + m* * 20/32) C(32,12)/91 = 12406200 at m* = 2 (measured exactly on 3 random label sets: m* = 2), below the same-top 14732720. Local counting is useless at n = 6 (bound 2^-14 of all sets against 2^-27), the usual Johnson wall.
* **Repeated roots.** T1 holds for any integer g, so a multiset phi >= 0 has V_phi = T + O(X^D) with agreement |supp phi|, and H_S = prod (X - y)^(phi(y)-1) is a real-root cofactor. T2 still forces gap = power of 2, and mass = D + gap. So **agreement > 9N/16 needs mass >= 5N/8** and all differences have Fourier coefficients in (1/4)Z (gap N/8). Mass 5/8 with Boolean members is the old 5/8 level; the new part is overlaps Sum(phi-1)^+ = omega N with omega < 1/16.
* **Virtual additive roots give nothing (proved for pairs, generic V+ containing V).** Let phi live on V+ = V + E with 2^k | Walsh differences, gap 2^(k-1) = g + delta, delta virtual points. At a character chi of V let x_e be the Walsh coefficient of the difference on coset e. Then Sum_e psi(e) x_e = 0 mod 2^k for all psi in E*. Averaging over psi gives x_0 = 0 mod 2^(k-j) and, if x_0 = 2^(k-j') * odd, the virtual part has Sum |x_e| >= (2^j' - 1) 2^(k-j') because Sum_(e != 0) psi(e) x_e has mean 0 and is = -x_0 mod 2^k. So delta >= (2^j' - 1) 2^(k-j'-1) and g <= 2^(k-j'-1), which the V-part alone already achieves by T1. Non-additive H with deg H < g costs 64 bits per coefficient; deg H >= g is the Johnson regime, not excluded (list size beyond the Johnson radius is an open problem for RS codes, so no proof is expected here).
* **Mean 1/2 members (exact).** Boolean C with |C| = N/2 and Fourier in (1/4)Z are hyperplane cosets and rank 2 quadrics = F1 u F2, F1 = {f=0, g1=c1}, F2 = {f=1, g2=c2}: M_C(n) = 8 [n,2]_2 (2^(n-2) - 1). Exhaustive over all N/2-subsets: n = 4: 870, n = 5: 8742, both equal to the formula + 2(2^n - 1), and Krylov labels 1, x, ..., x^(n-1) add nothing (`n7_quadric_check.cpp`).
* **Shortened quadric family (new).** Fix any set B, |B| = N/8. T = X^(N/2) V_B, P_C = V_B (X^(N/2) - V_C), deg P_C = N/8 + 3N/8 = D, agreement |C u B| = 5N/8 - |C cap B|. No disjointness is needed, so all quadrics are members. Since |C cap B| + |Cbar cap B| = N/8, at most half of them have agreement > 9N/16, and for random B about half do, by a fluctuation of order sqrt(N) (`n7_quadric_check.cpp`: n = 5: 2324 of 8680, n = 6: 27667 of 78120, up to 40 of 64). Replayed with Newton interpolation and the pole line in GF(2^16) at n = 6, 7, 8 with distinct slopes and a failing negative control (`n7_replay.py`).
* **Why it does not beat the record.** M_C(21)/2 = 2^60.415 at f = 0 (exact M_C(21) = 3074447083519519400), 2^60.07 with the margin 64 that f = 0 requires; coarser f loses 3 bits per level. A flat B (coset of a fixed codim 3 U*) has 8 alternatives, so 8 M_C(21) = 2^64.415 members, but overlap exactly N/16 for generic C, so agreement exactly 9N/16 = 1179648, below the record. Run 6 makes this rigorous.
* **Exhaustive n = 5 (`n7_extremal5.cpp`).** 1048110 classes, a pigeonhole regime. Sizes 15736 (155 classes, flat B), 11223 (34720, non-flat 4-sets), then 11200, 9056, ... Krylov labels give the same. Lists are V-translation invariant for Boolean degree 2 words X^(N/2) L; at large n this adds only a constant.

## Theory from run 6 (`n9_*`; the record's class is BitWonka's, quadric flats and pole pair as credited above)

Setting: class = coset of the lattice {d: V -> Z, mean 0, Fourier in (1/4)Z}, generic labels (T2). Write phi = 1_B + h, |B| = N/8, h = 1/2 + (1/4) Sum a_chi chi, m = Sum a_chi^2, O = E[(phi-1)^+], so agreement = (5/8 - O) N and the target is O < 1/16. Let x, y, y3 be the densities of h = -1, 2, 3, W' the common kernel (codim r), t the number of W'-cosets with h = -1, d = n - r.
* **Moment identity (exact):** m/16 = 1/2 + 2 E[C(phi,2)] - mean_B(phi)/4. With phi_max <= (6+m)/4 it forces m <= 10. Integrality: odd-coefficient characters sum to 0, sign parity fixed, so m is even and the shapes are (1^m), (2), (2,1^4), (2,1^6). For (1^m), h = (2 + m - 2 wt)/4.
* **All patterns (`n9_types.cpp`, exhaustive up to GL_r).** Allowed by O >= y + 2 y3: Boolean (m,r) = (4,3); (6,5) t=1; (6,4) t=1; (8,6) t=5; (8,5) t=3; (8,4) t=2; (10,5) t=5 needs x = 5/32 > 1/8, impossible for |B| = N/8, and (2,1^6) likewise; (2,1^4) only as r = 3, E' = B flat. Everything else has y + 2 y3 >= 1/16 or a value h <= -2, both excluded. In particular rank-7 m = 8 has x = y = 1/16, which contains the 8 flat alternatives: this is the rigorous reason 8 M_C never exceeds 9N/16.
* **Boolean h:** overlaps of C and its complement sum to N/8, so at most one is above 9N/16: at most M_C/2 + 2^n - 1.
* **Non-Boolean h:** E' is t cosets of W' inside B. Tuple bound: #(W', E') <= |B|^(d+t) / (t! bases(d) 2^((t-1)d)); configurations 13888, 280, 256, 1344, 56, 21 for (6,5), (6,4), (8,6), (8,5), (8,4), r = 3 (`n9_bound.py`). Total at n = 21 with Boolean: **2^63.125**, n = 20: 2^60.125. Far from tight; run 8 gives 2^61.58 for non-flat B.
* **Census (`n9_census.cpp`, exact), members above 9N/16, as a fraction of M_C/2:** n = 8: random 0.85, flat 0.82, one swapped point 1.044. n = 9: 0.893, 0.424, 0.781. n = 10: 0.925, 0.215, 0.643. Random B has no non-Boolean member from n = 8. Flat B: 1792 + 1344 per flat E' of codim 5 and 4 [n-3,2]_2 such flats, plus lower terms: exact 2^(2n) growth, about 2^47 at n = 21. Nothing grows faster than 2^(3n), and M_C/2 is the only 2^(3n) term.
* **Validation.** `n9_brute.cpp` (all zero-sum sets, all signs, N <= 64) agrees by type at n = 5, 6; the sum of types equals the exhaustive n = 5 class sizes; `n9_replay.py` checks each type in GF(2^16) by the polynomial identity, n = 7, 8, with a failing control.
* **Consequence (generic labels, real-root cofactors).** f <= 6 needs |supp| > 9N'/16, so mass 5N'/8, bounded above (run 8 covers every class); f >= 7 needs |supp| >= 9N'/16 with M_all(ny <= 10) <= 2^63.62. So no family has > 2^64 members above agreement 1179711: **106.24 is optimal in the real-root framework**, up to triple roots (run 8).
* **Instance read in Lean this run.** `RelaxedRelationFor` also carries a linear constraint, so violation can come from (v, mu) instead of farness. Constraint-only lines give lists of RS[k], the pole gives RS[k+1], and they do not combine to RS[k+2]. If f2 has a term above the code degree, all winners with agreement above that degree lie in one K-line, at most 2^64 (rigorous, run 4). Extra rows add constraints only. One agreement set gives one winner unless the pair is jointly close there.

## Theory from run 7 (`n8_*`; the class and its count are BitWonka's family as classified in run 3)

Notation: j = n - 4, Y = subspace of D of codim r, f' = 21 - r in the real domain, t(Z) = max over lam != 1 of dim(V cap lam V).
* **Merge map (exact).** For g in I^j: P(g) = 1 + sum_s Phi_j(g)_s X^-(2^j - 2^(j-1-s)) mod X^-(2^j), s = 0..j-1. Phi_j: I^j/I^(j+1) -> K^j is F_2-linear. Generators: 2^t x_T, |T| = j - t, x_T = 1_H - 1_(H+u) (H = even sums of T, u in T), and Phi_j = ((L_H(u) a_s(H))^(2^t))_s with a_s the coefficients of L_H, a_0 = 1. Doubling embeds ker Phi_j in ker Phi_(j+1) (word: cylinder, weight doubles). Dually, I^j/I^(j+1) = words R of RM(n-j, n) with R(0) = 0, and 2^t x_T is the monomial prod_T chi_i. So the top of a class with Fourier in (1/16)Z is additive in its residue word, A(W^perp) = coefficient vector of L_W, and two such classes share a top iff R + R' is in ker Phi_(n-4). If Phi_(n-4) is injective, T2 holds exactly for those labels, with no genericity. Rigorous: distinct W never merge (run 3).
* **Forced kernel.** gens - 64 j: 0 up to n = 8, 61 at n = 9, 463 at n = 10, 15273 at n = 14. Every label set tested reaches exactly this for n = 9..12, so at the real size injectivity is impossible and the question is low weight: a class R' has |R'| <= 64 and budget (64 - |R'|)/4 characters at +-1/8 (main class 12, and rank 4 costs 12).
* **Composition.** For Y inside W, a_s(W) = const(Y) + a K-linear image of the coefficient vector of W/Y. So words supported on Y^perp (dim r) only see the r - 4 coordinates of the quotient labels L_Y(D). Words of weight < 32 span at most 8 dims (Kasami-Tokura), at most 12 with R_W. Expected number of random low-weight kernel words over all Y: about 2^-14, 2^-28, 2^-13, 2^-18, 2^-43 for r = 6..10 (rough), so only structure can produce one.
* **Chains.** Labels lam mu^i, any lam, mu: ker dim 1, 4, 15 at n = 6, 7, 8, same as Krylov. At n = 6: k = 2x2 + 2x3 + x0x5 + x1x3 + x2x3 + x2x4, a polynomial identity in mu (c_2 and p_3 cancel term by term, checked by hand), a bent word of weight 28. A chain must fill the label space: patterns (5,1), (4,2), (3,3), (4,1,1), (3,2,1), (2,2,2) at n = 6 and (4,4), (5,3) at n = 8 give 0, and a chain of 6 inside n = 7, 8 only gives the doubled word (weight 56, 112). So the need is a quotient L_Y(D) that is a full chain, not a sub-chain.
* **Exact class sizes at n = 6** (`n8_class6.cpp`, all 2^60 subsets by meet in the middle, about 2.5 min; `n8_class6.log`). Random labels: exactly 12032931760 = M_all(2), a direct check of T2-T4 over all subsets. Same for top-relation Z: f = 2 [1,4], f = 3 [1,12,6a]. Krylov labels: T_W also holds the class of R' = R_W + k. |R'| = 24, 28, 32, 36 for 56, 210, 280, 105 of the 651 W, adding 10165506560, 9279334912, 8424668928, 7601402880. 3000 sampled extras pass a direct top check and share one residue set. So a merge is a real effect at n = 6. At n = 14 a partner has budget <= 10, rank <= 3 (rough), so at most about 2^60 and probably much less: at least 10 and probably about 2^10 separate merges would be needed (estimate, partner classes not computed for n > 6).
* **Relations.** Exhaustive in BF64: f = 1: t <= 5 (lam = x^2), f = 2: t <= 3, f = 3: t <= 2, generic t = 1 (Carlitz: e_f(xu) = x^(2^f) e_f(u) + (x^(2^f)+x) D_(f-1) e_(f-1)(u), `n8_carlitz_check.py`). Real size: pairs (Z, lam) with dim >= t about 2^(162 - 36 t - t^2), against n - 3 = 11 for a relation on flats.
* **Kernel scans (`n8_scans.log`, `n8_rel.log`).** r = 6..8 at d <= 10 exhaustive and samples of d = 11 and of the real D: ker = forced, f' = 0 is the only hit, with one exception: Y = 0x6c P_f' (0x6c = lcm of the polys of degree 2), r = 8: ker 1 for every f', weight 58, min wt(R_W + k) = 50, so no large class (`n8_word58.py`). r = 9: information set decoding finds only structural low-weight words (`n8_isd9.py`).
* **Consequence.** No Z with a useful relation was found and none is expected: 2^63 extra members need many low-weight merges, each a coincidence of at least 128 bits or a full-chain quotient, and none exists for f' >= 1 in any domain scanned. Not a proof at d = 21: 2^92 Y at r = 6 are only sampled, and r >= 9 only by ISD.

## Theory from run 8 (`n10_*`; record class BitWonka's, quadric flats and pole pair as credited above)

Setting: class = coset of L = {d: V -> Z, mean 0, Fourier in (1/4)Z}, generic labels. Member phi >= 0, mean 5/8, O = E[(phi-1)^+] < 1/16. hat(phi) = r + a/4 with r the minimal residue (|r| <= 1/8, a function of the class) and a integer; g = 5/8 + sum r chi; V = sum r^2 = 7/64 + v; t = 8|r|.
* **Types.** 4g + T = 0 mod 4 with T = sum a chi, so g mod 1 = c0 + lambda/2, lambda = xor of the odd-a characters, a class invariant. V >= 7/64 always, with equality for 1/2 + 1_B, for 3/4 - 1_T (rep 1_W - 1_T, W codim 2, an odd number of odd a; these are the natural signed classes) and for lambda != 0 (T in a hyperplane); 15/64 for integer-valued g. So signed classes need not cost variance, as run 6 assumed; they die from nonnegativity: T random gives 0.108, 0.0003, 0 of M_C/2 at n = 7, 8, 9.
* **Budget (exact).** Sum over a != 0 of (a^2 + 8 r a) = 2 + 32 E[C(phi,2)] - 16 v. For phi <= 2: < 4 - 16 v, every term >= 0.
* **Local means (any phi).** For a subspace Pi of characters, y = sum_Pi hat(phi) chi is the mean of phi on cosets of Pi^perp, so y >= 0 and E[(y-1)^+] <= O. Exhaustive (`n10_patterns.py`): if the residues on Pi have sup norm <= 1/16, the a-part on Pi of full rank is rank 1: +-chi, +-2 chi; rank 2: +-chi +-chi'; rank 3: only 4 zero-sum characters with T = +-2; rank >= 4: nothing. Direct form: 3 independent a != 0 characters force sum over the 4 products |hat| >= 1/8 - sum |r_i|. So 3 free characters occur only as a quadric.
* **Reps.** phi = rho + 1_C, C = 1/2 + T_4/4. For phi <= 2: O = 1/16 + kappa + q, kappa = (1/4) sum eps_i r_i, q = E[C(rho,2)] = density(rho = -1) + density(rho = 2). So q < -kappa. (Any phi: O = |C cap {rho>=1}| + E[(rho-1)^+].) C and C^c are never both members, so at most M_C/2 per rep. **Lemma R:** rho1 != rho2 with q1 + q2 < 1/48 have m_d < 6, so rho1 - rho2 = 1_F - 1_F', F, F' parallel codim 3 flats; hence reps with q < 1/96 number 1 or at most 8, and more than 1 only near a flat. At q = 0: two Boolean reps are equal or parallel flats (n = 5 counts agree).
* **Count (`n10_bound.py`, n = 21).** A+ = opposing characters with t >= 1/5 (signs forced), A- = the rest, cost >= 4/5 each, so j = |A-| <= 4. The number of A+ with cost < U is bounded by an exponential moment using sum t^2 = 7 + 64 v. j <= 2: 2^49.8. j = 3: 2^58.8. j = 4, xor 0, T_4 = 0 mod 4: two of the other three products have t >= 1/5, 2^50.2. j = 4, xor 0, T_4 = 2 mod 4: reps with q < 1/96 give M_C/2 each; reps with q >= 1/96 need sum_4 |r_i| > 4 q, so at most V 2^(2n)/(6 q^2) quadrics by Cauchy, and reps are a code of distance 4: 2^58.9. j = 4, xor != 0: every triple needs a product with |r| >= 1/80, covers of the 4 triples are two complementary pairs (2 free, one sigma) or at most 1 free: 2^59.5. **Total at most 2^63.595 for a strictly flat-like class (two reps with q < 2^-8, 8 M_C/2 = 2^63.415), 2^61.58 for every other class; n = 20: 2^60.80.** Below 2^64 without using the margin of 64 positions f = 0 needs.
* **Checks.** `n10_check.cpp` tests the budget identity, j <= 4, the formula for O, q < -kappa and the triple inequality exactly on all members at n = 6, 8, 9: no violation. `n10_class.cpp` agrees with `n9_census` and `n9_brute` on totals and by type.
* **Census (`n10_census.log`), members above 9N/16 / (M_C/2).** n = 9 without Boolean rep: |P| = 1, 2, 4, 8 random 0.405, 0.180, 0.035, 0.0009; F + E - Q with |E| = N/64, N/32, N/16 random 0.008, 0.0003, 0; two signed points in two alternative cosets 0.412 (n = 8: 0.434; the quadric part tends to 1/4); T in a hyperplane 0.0001. Hill climbing over classes without Boolean rep: n = 8 best 0.659 (217 evaluations), n = 7 best 0.836, n = 6 best 1.34 (small n). Many structured signed reps turn out Boolean: rho = 1_F + 1_E - 1_Q with Q in one alternative coset is Boolean through that coset.
* **Not covered: phi >= 3.** The local means and M_C/2 per rep hold for any phi, and reps with a few points rho = 2 inside C stay in the main term. But j <= 4 and the budget for A+ use phi <= 2: the budget grows with E[C(rho,2)], and the exponential moment is then too weak (N+(3) about 2^26). Census at n = 9: phi = 3 is 2% of the largest signed family and at most 40% of families below 0.04 of M_C/2. Expected harmless, not proved.

## Queue

Exhausted: N5 (write FINAL) done in run 9, see FINAL above; every later run takes step 2 (see Scheduler). Not blocking: if the user attaches the DKTZ PDF, compare the second construction with the reconstruction and read the first construction's mechanism (49.4% at rate 1/4 on a 2^27 domain, probability above 2^-30).

## Run log

* 2026-11-03 (interactive): H0-H4, framework, queue. Script: `binary_upper_scan.py`.
* 2026-11-03 (scheduled, run 2): N2 failed rigorously (`n2_kappa.cpp`, `n2_toy_replay.py`, `n2_f7_numbers.py`, `qrows.txt` from LabelTable.lean). Found the f = 7 route; new queue top N6.
* 2026-11-04 (scheduled, run 3): N6 failed exactly (2^62.430 < 2^64 at f = 7). Walsh conjecture proved (T1, T2); class classified (T3, T4); framework optimality of 106.24. Scripts `n6_*`; removed the f = 7 route from the queue. New top N3.
* 2026-11-04 (scheduled, run 4): N3 failed. Second DKTZ construction reconstructed from the abstract and verified; K-limit; no second word beyond one flat (two independent replays); Krylov triple found, too small. PDF body not readable. Scripts `n3_*`. New top N7.
* 2026-11-05 (scheduled, run 5): N7: one-check case closed at n = 5 (Theorem A, m* = 2); random hyperplane sampling at n = 4 (g = 2: 504, then 190; g = 3: 16, then 9, identified as a translation orbit and a shortened hyperplane). Found the multiset mechanism and the shortened quadric family: agreement above 9N/16 with M_C(n)/2 members; at f = 0 short of 2^64 by a factor of 12. Virtual additive roots excluded. Replayed in GF(2^16) with interpolation and the pole line. No record. Scripts `n7_*`. New top N9.
* 2026-11-05 (scheduled, run 6): N9 failed: no class of mass 5N/8 reaches 2^64 above 9N/16 (bound 2^63.125 for every B, true size about 2^60.415). Pattern classification, tuple bound, exact census to n = 10, brute force at n = 5, 6, polynomial replay. Real-root framework closed apart from signed representatives. Read the Lean instance definition: nothing new from the constraint or the rows. Scripts `n9_*`. New top N8.
* 2026-11-06 (scheduled, run 7): N8 failed. Merge map Phi and additive tops; exact n = 6 class counts over all 2^60 subsets confirm T2-T4 and measure the Krylov merge; exhaustive relation and kernel scans; one real exception at r = 8 (weight 58, useless). Official repo checked: binary upper still 10624 at HEAD eb82d3b. Scripts `n8_*`. New top N10.
* 2026-11-06 (scheduled, run 8): N10 failed and the signed gap closed for phi <= 2. Class types, budget, local means, Lemma R, bound 2^63.595 for every class at n = 21; unbiased class evaluator, census at n = 7, 8, 9, hill climbing, exact checks. Official repo still at eb82d3b, binary upper 10624. Scripts `n10_*`. New top N5.
* 2026-11-07 (scheduled, run 9): N5: queue exhausted, FINAL written. Official record rechecked (main eb82d3b, binary upper 10624, no binary upper submission after 2026-10-23, live leaderboard not reachable). Headline numbers re-verified exactly (`final_check.py`). ChatGPT's lane B binary branches read: all negative. Disabling the scheduled task was refused; left to the user.
* 2026-11-07 (scheduled, runs 10+: post-FINAL rechecks, this line is updated in place). Run 10
  (2026-11-07 12:40 UTC): proximityprize.org read with the user's approval (no standings), better.codes
  blocked for the fetch tool; six lane B binary branches read, all negative. Run 11 (2026-11-08 00:39 UTC):
  no official branch or PR newer than 2026-10-29; five lane B slice searches, covered by N2
  (`r11_laneb_check.py`). Run 12 (2026-11-08 12:39 UTC): search API only; lane B pivot note read. Run 13
  (2026-11-09 00:34 UTC): lane B Gold-form gates replayed (`r13_laneb_gold_check.py`). Run 14 (2026-11-09
  12:39 UTC): two lane B upper gates (Gold row root bound, affine complement at 106.22) replayed
  (`r14_laneb_check.py`).
  Latest: run 15, 2026-11-10 00:34 UTC. Queue exhausted, so step 2 only. Official main still eb82d3b, binary
  upper 10624 / 917441 (blob ids match exactly), newest PR #611; web search gives nothing relevant. Three new
  lane B upper gates (106.24 source audit, 106.23 obligation, core degree budget) replayed, the last extended
  to every core size (`r15_laneb_check.py`, log); two other-track commits not replayed. `final_check.py` and
  the r11, r13, r14 replays reproduce their committed logs exactly. Disabling the task refused again. No
  notification (nothing changed).
