# MCA Lane A — generator-order CI verification (2026-11-05 01:47 UTC)

Hypothesis: the dedicated Lean 4.34 workflow for the four explicit KoalaBear generator-power obligations succeeds at the pinned commit.

Outcome: CONFIRMED by GitHub Actions metadata, not by an external mathematical verifier.

Source: https://raw.githubusercontent.com/kmce87/proximity-orbitpencil-audit/266ead0a1742855312211af2edaa6ef96b92c629/LeanPortGeneratorOrderCertificate4096.lean
Workflow: https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41942864959
Job: https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41942864959/job/126967746431

Run 41942864959: completed/success, 2026-11-05 00:45:55 UTC, head 266ead0a1742855312211af2edaa6ef96b92c629. Job 126967746431: completed/success; step 'Compile explicit generator order obligations' completed/success at 00:45:51 UTC.

The four compiled theorems prove omega21^2097152=1, no earlier positive power equals one, and both properties for baseToSextic omega21. This implies exact order 2097152 in the local field and its image; no standalone orderOf equality is declared in this file. The theorem proofs use CompPoly primitive.pow_eq_one, primitive.pow_inj, and baseToSextic.injective.

Replay: checkout 266ead0a1742855312211af2edaa6ef96b92c629; inspect .github/workflows/mca-generator-order-434.yml; run the pinned setup then lake env lean LeanPortGeneratorOrderCertificate4096.lean. Compare Actions run and job metadata above. Do not conflate workflow success with external verification or manuscript-domain equivalence.

Outstanding: establish sextic F_(2130706433^6) and D=H identification against the published MCA model, deployed RS[D,2^20] code equivalence and fixed-line distinct-slope construction in the external formalism. Ordinary LIST a=1116047 unaffected. No upstream report posted. Independent prize-qualifying result: NO.

Prior art: https://github.com/proximity-prize/proximity-prize/pull/38 ; manuscript https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex . No new originality conclusion.
