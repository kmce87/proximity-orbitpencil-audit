# Lane A: deployed-degree transport audit (2026-11-05 20:21 UTC)

## Falsifiable hypothesis
The existing domain transport theorem `exists_many_domain_bad_slopes_1118207` *by itself* certifies a deployed RS[D, 2^20] explaining witness of degree at most 1,048,575.

**Falsified at the theorem interface.** In `LeanPortDomainTransport4096.lean`, `WOnDomain` requires `c.natDegree ≤ 1048576`. Its `WOnDomain1118207` wrapper only strengthens support cardinality, not the explaining polynomial degree. Consequently the final `exists_many_domain_bad_slopes_1118207` statement alone proves an auxiliary RS[D,2^20+1] witness, not the deployed-degree witness.

The *input* `OrbitPencilLiftMcaComposition4096.SupportWiseBad` in `LeanPortMcaComposition4096.lean` DOES explicitly require `c.natDegree ≤ 1048575`. The `SupportWiseBad_to_domain_1118207` proof destructures `⟨S,c,hcard,hdeg,hmatch,hnot⟩`, then transports through `W_to_domain`, which discards the stronger bound in its output type. Thus the degree is available in the source but erased from the public domain theorem's proposition.

## Exact formal repair obligation
Define a deployed-domain predicate with `c.natDegree ≤ 1048575`, retain the *same support* and `¬∃ cf cg` with degrees ≤ 1048576 (stronger noncontainment), and prove transport directly from `SupportWiseBad` using `S.image indexEquiv`. The proof can reuse `Finset.card_image_of_injective _ indexEquiv.injective` and `indexEquiv_val`. Crucially retain `hdeg` rather than using `W_to_domain` as the sole interface.

Then prove `∃ alpha U0 Z, 2^59 < Z.card ∧ ∀ z ∈ Z, DeployedBadSlopeOnDomain1118207 ...` with a single fixed pair of received words. Only after that match the manuscript's domain and MCA probability definition. Do not infer degree ≤ k-1 from degree ≤ k by code inclusion.

## Replay / independent source pointers
- https://github.com/kmce87/proximity-orbitpencil-audit/blob/955b00897da44f8ab2d831ed62ad165ba6d2a592/LeanPortDomainTransport4096.lean
- https://github.com/kmce87/proximity-orbitpencil-audit/blob/955b00897da44f8ab2d831ed62ad165ba6d2a592/LeanPortMcaComposition4096.lean
- https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
- https://github.com/proximity-prize/proximity-prize/pull/38

This is a source-level counterexample to the *sufficiency of the theorem statement*, NOT a counterexample to the underlying mathematical construction. No new Lean compilation or external acceptance occurred. The original LIST inequality at 1,116,047 is unaffected.
