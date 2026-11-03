# MCA Lane A — 2026-11-03 11:19 UTC — dependency falsification and repair

## One falsifiable hypothesis

**H:** The prior `mca/FiniteSupportCertificate.lean` can be compiled standalone as checked in, with no extra repository modules.

**Result: FALSIFIED by source inspection.** Its first lines are `import Mathlib` and `import Mca.DomainPolynomialTransfer`, but the earlier `mca/DomainPolynomialTransfer.lean` itself imports only Mathlib and **uses** `McaDeployedTransfer.Explains`, `Bad`, and `bad_of_asymmetric_witness` without importing `mca/DeployedSupportTransfer.lean`. The prior files also lack a demonstrated module layout for `Mca.*` imports. Therefore the previous source proposals are not self-contained; no successful Lean compilation should be inferred.

## Repair

New `mca/SelfContainedFiniteCertificate.lean` imports only Mathlib and contains all of the local definitions and proofs in one namespace. It explicitly separates:

1. `p.natDegree < k` (deployed explaining polynomial);
2. exclusion of simultaneous explanations in auxiliary `RS[D,k+1]`;
3. `support z ⊆ D` and `|support z| ≥ a`;
4. one fixed `f,g`, with slope-dependent supports/witnesses;
5. `2^59 < Z.card`, where `Z : Finset F` represents distinct slopes.

The result is **conditional** on (1)-(5). It does not construct KoalaBear parameters or prove any of the five premises. It also uses a **local** `Bad` definition, not an independently checked equivalence to the external MCA formalism.

## Replay

In a Lean 4.34 project with a compatible Mathlib dependency:

```bash
lake env lean mca/SelfContainedFiniteCertificate.lean
```

This compilation was **not executed** in this run (no local Lean/lake installation). Until a successful CI log is inspected, mark the new file **source-only, not Lean-kernel checked**.

## Source-to-manuscript check

The upstream [M2 line-decoding/MCA bridge](https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md) defines `LD_sw(C,a)` by maximizing over a **single fixed pair** `f,g`, counting **distinct** slopes for which a possibly slope-dependent support `S ⊆ D` has `|S| ≥ a`, a punctured-code explanation of `f+zg`, and no simultaneous explanation of `f,g`. The local abstract predicate follows this shape but the finite-field and code identification remain unproved. The [manuscript](https://github.com/przchojecki/rs-mca/blob/main/experimental/grande_finale.tex) must still be audited at the precise KoalaBear MCA claim.

## Cumulative evidence checked this run

Fetched `mca/FiniteSupportCertificate.lean` at `d2a231564ececfde5c1737e782016e6549a1fc04`, `mca/DomainPolynomialTransfer.lean` at `ee32bd8363841392020b93bc985fe5428efbcbb0`, and `mca/DeployedSupportTransfer.lean` at `15b7686e6514ac8fed67c37635413b75e5c84da5`. Fetched the upstream bridge and manuscript. No claim that other historical commits were rechecked here.

**Verification classification:** (i) >2^59 bad slopes at n=2^21: CLAIMED, not independently established here. (ii) Dependency defect and upstream bridge: SOURCE-CHECKED. (iii) Earlier 93-declaration local-model Lean 4.34 gate: PREVIOUSLY REPORTED, not reverified this run; new file NOT compiled. (iv) Independent verifier acceptance: NO. Independently verified prize-qualifying result: **NO**.

## Next precise blocker

Obtain a Lean 4.34 + Mathlib build of the self-contained transfer and inspect the actual CI log; then supply the concrete KoalaBear `D,f,g,Z,support,witness` with certified field equivalence, degree, support size, augmented exclusion, and injective slope count. Avoid treating the abstract conditional lemma as a numerical counterexample. No external issue/PR posted.
