# Lane A — 2026-11-03 12:15 UTC: LD_sw quantifier audit

## One falsifiable hypothesis

**H:** The existing local finite-support certificate alone already proves a lower bound on the actual source-defined `LD_sw(RS[D,k],a)` numerator.

**Result: FALSIFIED as a complete certification claim.** The source at commit `8728d329020ca4736e965883706832119ad75d82` concludes `2^59 < Z.card` and a local `Bad` predicate for each member of `Z`; it never defines `LD_sw` or proves its numerator is at least `Z.card`. Moreover, its `hcount` premise is assumed rather than constructed. This is a missing **formal bridge**, not a counterexample to the intended mathematics.

## Source-checked upstream definition

Fetched `przchojecki/rs-mca/experimental/notes/m2/m2_line_decoding_mca_bridge.md` on 2026-11-03. It defines `LD_sw(C,a)` as the maximum, over a **single fixed** `f,g`, of the number of distinct `z` admitting `S subset D` with `|S|>=a`, an explaining codeword for `f+zg`, and no simultaneous explanations of `f,g` on `S`. The note states `eps_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/|F|`.

The new `mca/BridgeQuantifiers.lean` makes the finite-field *local* numerator a `Finset.univ.filter`, and proposes the direct inclusion/cardinality theorem `Z.card <= LocalNumerator ...`. It explicitly leaves the max-over-lines and equality to the external source as a separate semantic identification; no concrete KoalaBear field is constructed. The proof uses only finite-set inclusion and is **source-only, not compiled**.

## Replay

```sh
lake env lean mca/BridgeQuantifiers.lean
```

Run under Lean 4.34 with compatible Mathlib. Do not mark kernel-checked without inspecting a successful CI log and axioms.

## Exact remaining certificate inputs

- An actual `F_(2130706433^6)` representation, domain `D` with `|D|=2^21`, and deployed `RS[D,2^20]`, with source/manuscript equivalence.
- A single fixed pair `f,g`, a concrete finite set `Z` with `|Z|>2^59`, and an injectivity proof for the slope parametrization.
- For each `z in Z`, a concrete `S_z subset D` of at least `1118207` elements, a polynomial explaining `f+zg` of degree **<2^20**, and noncontainment against the auxiliary `RS[D,2^20+1]`.
- A proof identifying the local numerator with the upstream support-wise MCA numerator, with agreement/radius conversion and quantifier order.
- Independent review of the original OrbitPencil attribution and of whether this exact lift has already been reported.

## Inspected cumulative history (not a blanket claim about all commits)

Fetched `mca/SelfContainedFiniteCertificate.lean` and its audit at `8728d329020ca4736e965883706832119ad75d82`, and `mca/DomainPolynomialTransfer.lean` and `mca/FiniteSupportCertificate.lean` at the same ancestor. Fetched upstream M2 bridge and `experimental/grande_finale.tex` (author Przemek Chojecki, dated July 2026). The repo README attributes the accepted original 512-fibre OrbitPencil to the public Proximity Prize PR #38 and coauthor `erdkocak`; that attribution is README evidence, not an independent inspection of the merged PR this run. A GitHub combined-status read on `8728d329...` returned no individual statuses; this does **not** establish either CI success or failure.

## Verification tiers

(i) `>2^59` concrete KoalaBear bad slopes: **claimed, not constructed here**.

(ii) Upstream M2 definition, local source and missing formal numerator bridge: **source-checked**.

(iii) New `BridgeQuantifiers.lean`: **not compiled/kernel checked**. Earlier local 93-declaration gate is reported, not reverified here.

(iv) Independent verifier accepted: **NO**.

**Independently verified prize-qualifying result: NO.** No external issue/PR posted. The old first-safe and coset loops remain closed.
