# DRAFT ONLY — potential KoalaBear n=2^21 support-wise MCA obstruction from a 4096-fibre OrbitPencil lift

**Do not post externally until the source-to-definition and independent replay checks below have been completed.**

## Suggested external issue title

Potential KoalaBear n=2^21 support-wise MCA counterexample via 4096-fibre OrbitPencil lift (Lean 4.34 audit; request definition review)

## Suggested issue body

I would appreciate an independent review of a proposed obstruction to the adjacent KoalaBear MCA safe-side claim. This is **not** a claim to have solved the grand MCA prize or improved the official better.codes benchmark.

For the concrete field `KoalaBear.Ext6` of cardinality `2130706433^6`, the `2^21`-point multiplicative NTT domain, and Reed–Solomon degree bound `< 2^20`, a Lean 4.34 audit proves a local theorem:

`OrbitPencilLiftMcaComposition4096.exists_many_supportwise_bad_slopes`

It constructs a **single** received affine line and a set of **`2^59+1` distinct finite slopes**. For every slope, there exists a support of **at least 1,118,207 distinct domain indices** and an RS message agreeing with that line point on the support, while **no** degree-`<2^20` polynomial agrees with the fixed line direction on the same support. The direction noncontainment is stronger than the per-support noncontainment in the published `W_a(f,g)` witness: if the direction is not code-explained, then the point and direction cannot both be code-explained.

If this local theorem is identified with the intended `LD_sw(C,a)` / MCA bad-slope convention in this repository, the proposed safe-side budget

`B* = floor((2130706433^6)/2^128) = 274980728111395087`

at agreement `a0=1116048` is violated by monotonicity, since the witness already has `2^59+1 > B*` distinct bad slopes at `a=1118207 > a0`. **The ordinary LIST inequality at agreement 1116047 is a separate statement and is not refuted.**

**Audit evidence:** the exact source commit [`eb369bf7fc473ce8cc70c57766bc01cca6621411`](https://github.com/kmce87/proximity-orbitpencil-audit/commit/eb369bf7fc473ce8cc70c57766bc01cca6621411) passed the [Lean 4.34 GitHub Actions gate, run 41514095351](https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41514095351) on 2 November 2026, finishing at 20:02:37 UTC. The log reports 80 declarations audited and the final theorem's transitive axioms exactly `propext`, `Classical.choice`, `Quot.sound` (no `sorryAx`). Replay from that commit: `bash scripts/run_lean_434_gate.sh`. The repository is presently private; source access must be provided to independent reviewers before any public claim.

**Attribution:** this is an adaptation of the **previously accepted** 512-fibre rational-pencil / OrbitPencil construction, [official Proximity Prize PR #38](https://github.com/proximity-prize/proximity-prize/pull/38), merged via Yukon autoresearch and including `erdkocak` in the co-author credit. The rational-pencil technique is **not** claimed as new. Any novelty claim would require a separate literature and source review.

**Outstanding before certification/publication:**
1. Independently replay the exact commit and audit the field/domain/code identification and agreement support endpoint.
2. Review the intended definition of `W_a(f,g)`, its projection to distinct slopes, and the conversion from local `SupportWiseBad` to the paper's `epsilon_mca` normalization and endpoint conventions.
3. Confirm this 4096-fibre witness has not already been reported; request original authors' input and preserve attribution.
4. Do not confuse this n=`2^21` result with the official KoalaBear `n=2^18` ArkLib benchmark; no official `ProtocolClaim` or independent prize-verifier acceptance has been obtained.

Would the maintainers be willing to check whether the local support-wise predicate and claimed safe-bound normalization match the intended adjacent KoalaBear MCA statement?

---

Draft prepared 2026-11-02. **Not posted to przchojecki/rs-mca.** This is a review request, not a certified disproof.
