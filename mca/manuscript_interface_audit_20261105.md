# Lane A: deployed MCA source-to-manuscript interface audit (2026-11-05 UTC)

## One falsifiable hypothesis
The deployed Lean predicate `DeployedBad` at commit 955b0089 uses a weaker explaining polynomial or weaker noncontainment quantifier than the published support-wise MCA definition in rs-mca CAP25 v13.2 (commit 4bea7abb).

**Outcome: falsified at the predicate-definition level.** The Lean predicate uses an explaining polynomial `c.natDegree ≤ 1048575` (the manuscript defines RS[F,D,k] by `deg p < k` with k=1048576), and forbids simultaneous explaining polynomials `cf,cg` even when their degrees are ≤1048576 (strictly *stronger* than forbidding them at degree <1048576). Both are on the *same support S*. The Lean theorem existentially fixes alpha,U0,Z before universally quantifying over slopes z in Z; it therefore has a fixed pair of received words. Finset Z gives distinct slopes. Support size is ≥1118207.

## Source citations for replay
- Lean deployed predicate and theorem: https://github.com/kmce87/proximity-orbitpencil-audit/blob/955b00897da44f8ab2d831ed62ad165ba6d2a592/LeanPortDeployedDomainBridge4096.lean
- Lean domain transport: https://github.com/kmce87/proximity-orbitpencil-audit/blob/955b00897da44f8ab2d831ed62ad165ba6d2a592/LeanPortDomainTransport4096.lean
- Manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex (Preliminaries, definition def:mca)
- Original OrbitPencil attribution: https://github.com/proximity-prize/proximity-prize/pull/38

## Exact unresolved proof obligations
1. Show `D = Set.range node6` is the precise order-2^21 subgroup/coset of the manuscript's deployed KoalaBear sextic domain, not merely a set of 2^21 distinct points. `node6_injective` alone does not prove this external identification.
2. Prove a named Lean theorem converting `DeployedBad` to a *separately defined* manuscript `MCABad` predicate for `RS[Sextic,D,1048576]`, with the integer-ball endpoint and the published field distribution.
3. Formalize the final probability comparison from `Z.card > 2^59` to `epsilon_mca > 2^-128` using the concrete sextic cardinality, without replacing the degree <k explaining witness with an auxiliary degree ≤k witness.
4. Verify original attack attribution and check upstream issues/PRs for prior disclosure before any external submission.

## Reproduction
Read the three exact linked source files; inspect `DeployedBad`, `exists_many_deployed_bad_slopes`, manuscript `RS` and `def:mca`. This is a source-level comparison only, not a newly kernel-checked theorem or independent acceptance. No historical files modified. Lane B untouched.
