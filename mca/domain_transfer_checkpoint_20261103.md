# Lane A domain transfer checkpoint — 2026-11-03 09:30 UTC

## One falsifiable hypothesis
Can the previous abstract transfer be stated at the actual **polynomial-degree** level with a single fixed affine received line, parameter-dependent support, and finite distinct slope set, without using code inclusion to manufacture a smaller-degree explaining witness?

**Source-level outcome:** yes, as a proposed theorem in `mca/DomainPolynomialTransfer.lean`. **Kernel outcome:** untested: no Lean 4.34 executable or Actions confirmation in this run. A successful build is required before marking this formalised.

The theorem `deployed_fixed_line` assumes for each `z ∈ Z` a polynomial of `natDegree < k` explaining the same fixed functions `f + z*g` on `support z ⊆ D`. It assumes exclusion of simultaneous explanations of `f,g` by polynomials of degree < `k+1`. It concludes `Bad (RSFunctions D k) (support z) f g z` for each slope in `Z`. This makes no claim that such witnesses exist for the concrete OrbitPencil lift.

**Critical qualification:** `Bad` here is the local model definition (explained combination and non-simultaneous endpoint explanation); it is NOT yet proved definitionally equivalent to the original rs-mca numerator. No fixed-line count or >2^59 claim follows without a concrete injection into `Z` and the full domain equivalence.

## Replay
```bash
git checkout mca-domain-transfer-20261103-0930
# In a project pinned to Lean 4.34 and compatible Mathlib:
lake env lean mca/DomainPolynomialTransfer.lean
```
The file imports Mathlib and is otherwise standalone. The replay has **not** been executed successfully here.

## Inspected source history
- `15b7686e6514ac8fed67c37635413b75e5c84da5`: fetched and read `mca/DeployedSupportTransfer.lean`, an abstract transfer proposal; uncompiled.
- `8fd556d13ac53be4df92a44579e01365785452f1` and `bbbbc46025cbd09654e73457118ad3de4ca78b7e`: named in previous report but the requested path `mca/DeployedSupportTransfer.lean` was not present at these commits. This is not evidence the commits themselves are absent; their claimed audit contents were not rechecked this run.
- This branch descends from `15b7686`; no archive rewritten.

## Literature and attribution
- [Original official benchmark](https://github.com/proximity-prize/proximity-prize)
- [Public port of upper 116.13 candidate](https://github.com/zksecurity/proximity-prize-submissions-lean434)
- [rs-mca project and active scope](https://github.com/przchojecki/rs-mca)
- [rs-mca AGENTS.md](https://github.com/przchojecki/rs-mca/blob/main/agents.md): explicitly demands direct MCA numerator and a fixed received line. The published source discusses obstruction floors, so no novelty is asserted for the general idea of quotient fibres.

## Next exact blocker
1. Compile the standalone theorem on pinned Lean 4.34; inspect axiom closure.
2. Compare `Bad` with the **actual** rs-mca source definition, including whether endpoint noncontainment is conjunctive or disjunctive and whether line membership is support-restricted.
3. Instantiate the 4096-fibre construction with degree < 2^20 polynomial witnesses and exclusion against degree < 2^20+1; prove exact D and F_(p^6) equivalence and injective slope map.
4. Check original authorship and whether the specific lift was previously reported before opening an external issue.

Independent prize-qualifying verification: **NO**. No external report posted.
