# MCA Lane A — challenge-set quantifier audit (2026-11-03 14:22 UTC)

**One falsifiable hypothesis:** Does the previously committed `BridgeQuantifiers.lean` bound the *challenge-restricted* numerator `B^MCA_{C,Gamma}(a)` of the current rs-mca Grande Finale manuscript, for arbitrary `Gamma`, without proving its counted slopes lie in `Gamma`?

**Outcome: NO.** The local `LocalNumerator` filters `Finset.univ` (all field slopes). The Grande Finale source at blob `6b21d6ea937a8a9f85fc7ade6032d73efd4c7222` explicitly invokes `B^MCA_{C,Gamma}(a)` and defines a sparse numerator using `gamma in Gamma`. The upstream M2 bridge at blob `8886762e0d99ffc3f891532779d7b7063ea86d32` uses `LD_sw(C,a)` over `z in F`. These are different quantifications unless `Gamma=F` or an additional inclusion/equivalence theorem is supplied.

This does **not** show that the proposed KoalaBear lift fails: the concrete challenge set `Gamma` and its relationship to the proposed distinct slope family have NOT been established in this run. In particular, the field-wide lower bound can remain valid even if a challenge-restricted lower bound is not yet certified.

## Proposed repair

`ChallengeRestrictedNumerator.lean` explicitly filters `Gamma` and requires `Z subset Gamma` in `certified_subset_lower_bound`. This is an abstract conditional bridge only; it neither constructs `Z` nor proves `Z.card>2^59`, field/domain equivalence, deployed degree <k, or noncontainment.

A direct finite-set falsification diagnostic: let `F={0,1,2}`, `Gamma={0}`, and an abstract bad predicate be true on `{1,2}`. The all-field bad count is 2, while the restricted bad count is 0. No all-field lower bound alone can force the restricted bound. This is a set-theoretic diagnostic, not a Reed-Solomon counterexample.

## Source links and replay

- Local preceding file: https://github.com/kmce87/proximity-orbitpencil-audit/blob/9ecfd556812c1899bbe0379c5fc167e47e7f54ea/mca/BridgeQuantifiers.lean
- Original M2 bridge: https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md
- Grande Finale manuscript: https://github.com/przchojecki/rs-mca/blob/main/experimental/grande_finale.tex
- Replay (requires Lean 4.34 + compatible Mathlib): `lake env lean mca/ChallengeRestrictedNumerator.lean`

No Lean/Lake binary was available in the execution container; no kernel compilation is claimed. The previously reported 93-declaration gate pertains to the LOCAL model, not this file. The original OrbitPencil authorship, KoalaBear field/domain, fibre lift, exact support and distinct slope count remain to be independently certified. No external issue/PR or independent acceptance is claimed.

**Next blocker:** Extract the actual `Gamma` used by the KoalaBear MCA claim from the authoritative CAP25 definition and check whether the claimed slope injection lands in `Gamma`. If `Gamma=F`, prove and record that equality; otherwise construct an explicit eligible subfamily with >2^59 distinct slopes. Separately compile this proposed Lean theorem and complete the deployed-code witness instantiation.

**Prize-qualifying independently verified result: NO.**
