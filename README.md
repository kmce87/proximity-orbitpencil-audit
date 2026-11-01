# Proximity Prize — OrbitPencil lift audit

Private, falsification-first research workspace for the KoalaBear n=2^21 OrbitPencil transfer.

## Verified milestone (2026-11-01 04:36 UTC)

**Three conditional Lean modules compiled successfully under Lean 4.34.0 with the pinned ArkLib/Mathlib dependency:**
- `LeanPortIndexedNoncontainment.lean`: polynomial root-count obstruction, indexed-support image-cardinality bridge, and rational quotient-direction bridge.
- `LeanPortNoncontainment.lean`: field-support polynomial obstruction.
- `LeanPortGeometry.lean`: 4096 × 512 index injection and power-projection identity.

First successful compiler run: [GitHub Actions #3](https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41273007323), source commit `3a929df61c07f753115bb251378ad5466c11265f`.
Simplified CI also passed: [GitHub Actions #4](https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41273446822), commit `7e8533d25c54776d4f3caa5ab353ea89e57b788f`.

**This is NOT a complete MCA refutation, NOT a Lean proof of >2^59 distinct slopes, NOT an official benchmark ProtocolClaim, and NOT independent-verifier acceptance.** The theorems assume nonzero polynomials, exact degrees, injective domain, and (for the quotient lemma) a supplied evaluation identity. Those assumptions are not yet constructed from the actual n=2^21 RS-MCA line. Lean compilation checks the declarations, but the transitive axiom closure has not yet been independently audited.

## Research and attribution

The construction is adapted from the existing, accepted 512-fibre [OrbitPencil.lean submission](https://github.com/proximity-prize/proximity-prize/pull/38), merged August 20, 2026. The submission commit credits co-author `erdkocak`; the submission was delivered through Yukon auto-research/Codex. We do not claim originality for the published rational-pencil method.

The earlier Python/GMP arithmetic and finite-field experiments are retained in a separate historical Git archive (not yet imported into this repository). The source candidates and CI here do not replace that full history.

The current official protected KoalaBear benchmark uses n=2^18, not this n=2^21 MCA research profile. The official benchmark also requires a different `ProtocolClaim` theorem and independent verifier acceptance.

## Replay

Open [Actions](https://github.com/kmce87/proximity-orbitpencil-audit/actions), select **Lean 4.34 candidate kernel gate**, and inspect the compiler job.

With Lean/Lake 4.34.0 and dependencies:
```sh
lake update
lake exe cache get
bash scripts/run_lean_434_gate.sh
```

## Next proof obligations

1. Audit `#print axioms` on the compiled lemmas and add a fail-closed admission gate.
2. Formalize the actual KoalaBear n=2^21 field/domain, received affine line, subset-family size, alpha selection, and distinct-slope injection.
3. Establish the exact support-wise MCA definition bridge before drafting an external issue.
4. Keep the original n=2^18 official benchmark and its `ProtocolClaimUpper` target separate.

**Prize-qualified independent verifier acceptance: NO.**
