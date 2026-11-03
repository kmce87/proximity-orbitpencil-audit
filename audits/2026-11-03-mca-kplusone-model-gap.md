# 2026-11-03 01:08 UTC — external MCA code-dimension mismatch audit

## One falsifiable hypothesis
The local Lean witness for RS message degree < 2^20 transfers unchanged to the **exact** KoalaBear MCA code defined in rs-mca.

**Result: NOT YET PROVED. A specific model mismatch was found.**

## Source evidence
- Local `LeanPortDomainTransport4096.lean` defines `WOnDomain` using `c.natDegree ≤ 1048575`, and excludes simultaneous explanations with `cf.natDegree ≤ 1048575` and `cg.natDegree ≤ 1048575`.
- Local `LeanPortDirectionNoncode4096.lean` and `LeanPortIndexedNoncontainment.lean` exclude only direction polynomials with `q.natDegree ≤ 1048575`.
- External `przchojecki/rs-mca/experimental/grande_finale.tex` states **K=2^20+1 on the MCA route**, K=2^20 on the list route (active frontier, n=2^21). The MCA code may therefore allow polynomials of degree ≤ 1048576, a strictly larger class.
- External `experimental/notes/m2/m2_line_decoding_mca_bridge.md` defines support-wise MCA with the same support and simultaneous noncontainment, and states eps_mca=LD_sw/|F|. Its RS code must be matched exactly.

## Consequence
Noncontainment against degree ≤ 1048575 does NOT automatically imply noncontainment against degree ≤ 1048576. The existing local 93-declaration theorem is correct for its own stated code, but its use as a disproof of the external MCA conjecture requires the stronger noncontainment theorem. This is an important missing proof obligation, not a refutation of the construction.

## Precise next test
1. Prove `quotient_direction_not_codeword_on_indices` with `hqdeg : q.natDegree ≤ 1048576`. The existing root-count method should extend: `natDegree ((X^4096-C α)*q+R) ≤ 1052672 < 1118207` (and also <1116048); the nonzero/degree contradiction is unchanged.
2. Replace the local `WOnDomain` predicate with the external MCA degree allowance for both explaining polynomials; keep the line-point witness of degree ≤1048575 (sufficient for the larger code).
3. Kernel-check a single fixed line and >2^59 distinct slopes under the strengthened predicate; rerun the 4.34 transitive axiom gate and confirm no new axioms.
4. Verify the external manuscript's exact `K` convention directly from the code definition, not just the frontier table. Check domain, field, line quantifiers, and support endpoint.
5. Only then request independent review or post the cautious external issue.

## Status
No new Lean theorem claimed. No official benchmark score claimed. Original rational-pencil technique is from accepted official OrbitPencil PR #38 (Yukon/Codex submission, contributors including erdkocak). The ordinary LIST inequality is separate.
