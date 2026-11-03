# MCA Lane A — finite-support audit (2026-11-03 10:24 UTC)

## Falsifiable hypothesis and result

**Hypothesis:** the previously committed `deployed_fixed_line` theorem, by itself, certifies that a fixed received line has >2^59 support-wise MCA-bad slopes at agreement a=1,118,207.

**FALSIFIED as a sufficiency claim.** It establishes a local `Bad` proposition for every member of an assumed finite slope set but has **no support-cardinality lower bound**, **no numerical lower bound on the slope-set cardinality**, and **no proof that the concrete KoalaBear lift provides the hypotheses**. It also does not identify the local predicate with the external MCA numerator. The abstract degree transfer remains useful but is not the claimed numerical certificate.

## Independent external source comparison

Fetched and read on 2026-11-03:
- https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md
- https://github.com/przchojecki/rs-mca/blob/main/experimental/grande_finale.tex

The bridge defines support-wise noncontained slopes by (1) a support S subset D of **size at least a**, (2) explanation of (f+zg)|S by a codeword, and (3) failure of simultaneous explanations of f and g on the same S. It defines LD_sw as a **maximum over fixed f,g** of the **number of distinct z**, and asserts equality to eps_mca times |F|. Thus the local `Bad` definition matches the bridge's per-support logical clauses if `RSFunctions D k` represents the punctured code, but does not include the cardinality or counting quantifiers. This is a source-level alignment, not a formal theorem identifying the actual manuscript definitions.

The original source notes exact-size support reduction only when a >= k+1; here 1,118,207 > 1,048,576, so that precondition would hold if the other concrete assumptions do.

## Exact source change

Added `mca/FiniteSupportCertificate.lean` in commit `eddf491574bac4bb80883fcd6fae3f454c3be06f`. The proposed `finite_support_certificate` theorem adds `Finset` supports, `a <= support.card`, fixed f/g and degree < k witnesses. The proposed `many_distinct_local_bad_slopes` theorem adds the **separate assumption** `2^59 < Z.card` and proves the local filtered count equals the set size. Neither theorem constructs Z or proves its cardinality. **NOT COMPILED OR KERNEL CHECKED**; the import path may require adaptation to the repo's Lean project structure.

Replay (in a Lean 4.34 project with Mathlib and the existing transfer file mapped to `Mca.DomainPolynomialTransfer`):
```sh
lake env lean mca/FiniteSupportCertificate.lean
```
Do not claim this replay succeeded without actual Actions logs.

## Remaining proof obligations, in order

1. Compile the earlier domain transfer and new finite-support wrapper under Lean 4.34; check axioms.
2. Construct one fixed f,g and explicit finite Z from the 4096-point fibre lift, prove Z.card > 2^59 by injection rather than raw parameter count.
3. Prove all supports have >= 1,118,207 points in the **same** domain D, with deployed witness degree < 2^20 and auxiliary noncontainment against degree < 2^20+1.
4. Establish field/domain equivalence with F_(2130706433^6), source-to-manuscript predicate identification and originality/author-credit review.
5. Only then consider an author-crediting external report. None posted here.

## Verification matrix

(i) Claim: concrete 4096-fibre lift gives >2^59 distinct MCA-bad slopes — **unproved**.
(ii) Independently source-checked: bridge's support, fixed-line, and slope-count definitions, plus the missing conditions in the prior local theorem.
(iii) Lean-kernel checked: earlier reported 93-declaration local gate at c7a517c; **not this new wrapper**.
(iv) Independently accepted prize-qualifying result: **NO**.

Earlier checked in this run: source at `ee32bd8363841392020b93bc985fe5428efbcbb0` and checkpoint at `020bbe36dc4c55fb1de5cd37e14b8d5c743d4040`. This run does not assert a merged history or revalidate the separate audit branches `8fd556d` and `bbbbc46`. Historical archives unchanged.
