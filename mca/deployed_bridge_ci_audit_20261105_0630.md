# Deployed-domain bridge CI audit — 2026-11-05 06:30 UTC

## One falsifiable hypothesis
The repaired CI workflow at commit 56cf76baa3aff55eaeae481d6989c087e358f540 executes and successfully compiles LeanPortDeployedDomainBridge4096.lean, rather than failing before Lean.

## Direct evidence and replay
GitHub Actions run https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41972714158 was queried through the GitHub API. It reports status completed, conclusion success, head SHA 56cf76baa3aff55eaeae481d6989c087e358f540, updated 2026-11-05T05:21:20Z. Its jobs API reports success for both 'Bootstrap pinned Lean and Mathlib' and 'Compile deployed RS degree bridge (Lean 4.34)'.

Replay from the pinned commit:
```sh
git checkout 56cf76baa3aff55eaeae481d6989c087e358f540
bash scripts/run_lean_434_gate.sh
lake env lean LeanPortDeployedDomainBridge4096.lean
```
The workflow source also runs these commands. Independently inspect the workflow logs to establish printed axiom dependencies; a successful job alone does not prove the absence of custom axioms in transitive imports.

## Source checked
LeanPortDeployedDomainBridge4096.lean defines DeployedBad with explanation natDegree <= 1048575 and noncontainment against polynomials with natDegree <= 1048576, agreement >=1118207, and an existential fixed alpha/U0 plus finite set Z with card > 2^59. The proof uses the original SupportWiseBad polynomial rather than recovering it from RS[D,k+1]. It imports LeanPortDomainTransport4096 and prints axioms of both bridge theorems.

## Limits
This is a local Lean compilation result, not an independent verifier's acceptance of the external MCA manuscript statement. External field/domain and quantifier equivalence, manuscript definition comparison, full imported-axiom review, and novelty/publication check remain open. The source header still says 'NOT yet kernel-checked'; this is stale after successful CI and should be corrected in a separate source change if appropriate. Ordinary LIST at a=1116047 is not addressed. Lane B is untouched.

## References
- https://github.com/proximity-prize/proximity-prize/pull/38
- https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
- https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41972714158

Independently verified prize-qualifying result: NO.
